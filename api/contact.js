// Contact form handler. Verifies reCAPTCHA, rate-limits by IP, sends via SES.
// Zero npm dependencies — Node built-ins only, so the site keeps its no-build-step rule.

import crypto from 'node:crypto';

const REGION = process.env.SES_REGION || 'eu-west-1';
const FROM = process.env.SES_FROM;
const TO = process.env.SES_TO;
const AK = process.env.AWS_ACCESS_KEY_ID;
const SK = process.env.AWS_SECRET_ACCESS_KEY;
const RECAPTCHA_SECRET = process.env.RECAPTCHA_SECRET;
const UPSTASH_URL = process.env.UPSTASH_REDIS_REST_URL;
const UPSTASH_TOKEN = process.env.UPSTASH_REDIS_REST_TOKEN;

const RATE_LIMIT = 3;
const WINDOW_SECONDS = 3600;

const sha256 = (v) => crypto.createHash('sha256').update(v, 'utf8').digest('hex');
const hmac = (key, v) => crypto.createHmac('sha256', key).update(v, 'utf8').digest();

// AWS Signature V4. Hand-rolled to avoid pulling in the AWS SDK.
function signedSesRequest(body) {
  const host = `email.${REGION}.amazonaws.com`;
  const path = '/v2/email/outbound-emails';
  const now = new Date();
  const amzDate = now.toISOString().replace(/[:-]|\.\d{3}/g, '');
  const dateStamp = amzDate.slice(0, 8);
  const payloadHash = sha256(body);

  const canonicalHeaders =
    `content-type:application/json\nhost:${host}\nx-amz-date:${amzDate}\n`;
  const signedHeaders = 'content-type;host;x-amz-date';
  const canonicalRequest = [
    'POST', path, '', canonicalHeaders, signedHeaders, payloadHash,
  ].join('\n');

  const scope = `${dateStamp}/${REGION}/ses/aws4_request`;
  const stringToSign = [
    'AWS4-HMAC-SHA256', amzDate, scope, sha256(canonicalRequest),
  ].join('\n');

  const signature = hmac(
    hmac(hmac(hmac(hmac(`AWS4${SK}`, dateStamp), REGION), 'ses'), 'aws4_request'),
    stringToSign
  ).toString('hex');

  return {
    url: `https://${host}${path}`,
    headers: {
      'Content-Type': 'application/json',
      'X-Amz-Date': amzDate,
      Authorization:
        `AWS4-HMAC-SHA256 Credential=${AK}/${scope}, ` +
        `SignedHeaders=${signedHeaders}, Signature=${signature}`,
    },
  };
}

// Returns true when the caller is over the limit. Fails open: if Upstash is
// unset or unreachable the form still works, and reCAPTCHA remains the guard.
async function isRateLimited(ip) {
  if (!UPSTASH_URL || !UPSTASH_TOKEN) return false;
  try {
    const key = `ada:contact:${ip}`;
    const res = await fetch(`${UPSTASH_URL}/pipeline`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${UPSTASH_TOKEN}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify([
        ['INCR', key],
        ['EXPIRE', key, String(WINDOW_SECONDS), 'NX'],
      ]),
    });
    if (!res.ok) return false;
    const [incr] = await res.json();
    return Number(incr.result) > RATE_LIMIT;
  } catch {
    return false;
  }
}

async function recaptchaOk(token, ip) {
  if (!RECAPTCHA_SECRET) return true; // not configured yet
  if (!token) return false;
  const res = await fetch('https://www.google.com/recaptcha/api/siteverify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      secret: RECAPTCHA_SECRET,
      response: token,
      remoteip: ip,
    }),
  });
  const data = await res.json();
  return data.success === true;
}

const esc = (s) =>
  String(s ?? '').replace(/[&<>"]/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])
  );

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  if (!FROM || !TO || !AK || !SK) {
    console.error('contact: SES env vars missing');
    return res.status(500).json({ error: 'Form is not configured yet.' });
  }

  const ip =
    (req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
  const { name, email, phone, 'phone-code': code, message, website, token } =
    req.body || {};

  // Honeypot — real visitors never see this field.
  if (website) return res.status(200).json({ ok: true });

  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email are required.' });
  }
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return res.status(400).json({ error: 'That email address looks wrong.' });
  }

  if (!(await recaptchaOk(token, ip))) {
    return res.status(400).json({ error: 'Please complete the captcha.' });
  }
  if (await isRateLimited(ip)) {
    return res
      .status(429)
      .json({ error: 'Too many messages. Please try again in an hour.' });
  }

  const phoneFull = phone ? `${code || ''} ${phone}`.trim() : '—';
  const html =
    `<p><strong>Name:</strong> ${esc(name)}</p>` +
    `<p><strong>Email:</strong> ${esc(email)}</p>` +
    `<p><strong>Phone:</strong> ${esc(phoneFull)}</p>` +
    `<p><strong>Message:</strong><br>${esc(message).replace(/\n/g, '<br>')}</p>`;

  const body = JSON.stringify({
    FromEmailAddress: FROM,
    Destination: { ToAddresses: [TO] },
    ReplyToAddresses: [email],
    Content: {
      Simple: {
        Subject: { Data: `Website enquiry from ${name}`, Charset: 'UTF-8' },
        Body: { Html: { Data: html, Charset: 'UTF-8' } },
      },
    },
  });

  try {
    const { url, headers } = signedSesRequest(body);
    const sesRes = await fetch(url, { method: 'POST', headers, body });
    if (!sesRes.ok) {
      console.error('SES error', sesRes.status, await sesRes.text());
      return res.status(502).json({ error: 'Could not send. Please email us directly.' });
    }
    // Log the MessageId — without it a message can't be traced once SES accepts it.
    const { MessageId } = await sesRes.json().catch(() => ({}));
    console.log('SES accepted', { MessageId, to: TO, from: FROM });
    return res.status(200).json({ ok: true, id: MessageId });
  } catch (err) {
    console.error('SES request failed', err);
    return res.status(502).json({ error: 'Could not send. Please email us directly.' });
  }
}
