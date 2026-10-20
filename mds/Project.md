Setup: Claude Code single source of truth. Read at session start.

What: Portfolio website for Alistair Drummond, Cape Town residential architect. Showcases 12 completed projects with image galleries, project descriptions, and contact details.

Audience: Prospective clients, property developers, referral networks in Cape Town.

Pages: Homepage (slideshow) | Projects grid | Gallery | Contact | 12 project detail pages.

Entity: Alistair Drummond Architect. Contact via site contact form. Site owned and managed by Hugo Drummond.

Live URL: alistairdrummondarchitect.co.za (alistair-drummond-architect.vercel.app)
GitHub: hugo-drummond/alistair-drummond-architect
Staging: `staging` branch → https://alistair-drummond-architec-git-5e7550-cifade7739-5613s-projects.vercel.app (Vercel login, or add the protection-bypass query string for Alistair — see Stack.md)
Local path: ~/alistair-drummond-architect

Hard Rules:
- Static site only. No frameworks, no build tools, no npm.
- Mobile and desktop must both work after any change.
- Never edit mobileSlides when only desktopSlides changes are requested.
- Gallery view (phone vs desktop) is locked at page load; it must not switch on rotate/resize.
- Never push to master until the client has reviewed changes locally or on staging, unless Hugo says to push straight to live.
- Image edits are desktop-only unless explicitly told otherwise.
- All new images go in the relevant project subfolder under images/.
- Use /usr/bin/git push, not git push (homebrew curl conflict).
