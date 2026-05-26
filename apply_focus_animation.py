import re, os

base = '/Users/hugodrummond/alistair-drummond-architect'

# ── Complex pattern (10 files) ─────────────────────────────────────────────
complex_files = [
    'project-bellevue.html',
    'project-cadenza.html',
    'project-camps-bay.html',
    'project-fernwood.html',
    'project-hills-bettys-bay.html',
    'project-mount-pleasant.html',
    'project-simpson-tyler.html',
    'project-upper-kloof.html',
    'project-van-lienden.html',
    'project-van-reenen.html',
]

new_complex = (
    'let preFocusRect = null;\n'
    '    function applyOrientation() { if (imgA.complete && imgA.naturalWidth > 0) { section.classList.toggle("portrait-slide", imgA.naturalHeight > imgA.naturalWidth); } else { imgA.onload = () => section.classList.toggle("portrait-slide", imgA.naturalHeight > imgA.naturalWidth); } }\n'
    '    function enterFocusAfterOrient() {\n'
    '      preFocusRect = section.getBoundingClientRect();\n'
    '      const doFocus = () => {\n'
    '        applyOrientation();\n'
    '        const vw = window.innerWidth, vh = window.innerHeight, r = preFocusRect;\n'
    '        section.classList.add("focused"); document.body.classList.add("gallery-focus");\n'
    "        section.style.transition = 'none';\n"
    '        section.style.clipPath = `inset(${r.top}px ${vw - r.right}px ${vh - r.bottom}px ${r.left}px)`;\n'
    '        section.offsetHeight;\n'
    "        section.style.transition = 'clip-path 0.4s cubic-bezier(0.4,0,0.2,1)';\n"
    "        section.style.clipPath = 'inset(0px 0px 0px 0px)';\n"
    '      };\n'
    '      if (imgA.complete && imgA.naturalWidth > 0) { setTimeout(doFocus, 250); }\n'
    '      else { imgA.onload = () => setTimeout(doFocus, 250); }\n'
    '    }\n'
    '    function exitFocus() {\n'
    "      if (!preFocusRect) { section.classList.remove('focused'); document.body.classList.remove('gallery-focus'); return; }\n"
    '      const vw = window.innerWidth, vh = window.innerHeight, r = preFocusRect;\n'
    "      section.style.transition = 'clip-path 0.4s cubic-bezier(0.4,0,0.2,1)';\n"
    '      section.style.clipPath = `inset(${r.top}px ${vw - r.right}px ${vh - r.bottom}px ${r.left}px)`;\n'
    '      setTimeout(() => {\n'
    "        section.classList.remove('focused'); document.body.classList.remove('gallery-focus');\n"
    "        section.style.clipPath = ''; section.style.transition = ''; preFocusRect = null;\n"
    '      }, 400);\n'
    '    }'
)

pat_complex = re.compile(
    r'function applyOrientation\(\).*?function exitFocus\(\)\s*\{[^}]*\}',
    re.DOTALL
)

for fname in complex_files:
    path = os.path.join(base, fname)
    with open(path) as f:
        content = f.read()
    new_content, n = pat_complex.subn(new_complex, content, count=1)
    if n == 0:
        print(f'NO MATCH: {fname}')
    else:
        with open(path, 'w') as f:
            f.write(new_content)
        print(f'Updated (complex): {fname}')

# ── Simple pattern (project-augustin.html) ────────────────────────────────
new_simple = (
    'let preFocusRect = null;\n'
    '    function enterFocus() {\n'
    '      preFocusRect = section.getBoundingClientRect();\n'
    '      const vw = window.innerWidth, vh = window.innerHeight;\n'
    "      section.classList.add('focused');\n"
    "      document.body.classList.add('gallery-focus');\n"
    "      section.style.transition = 'none';\n"
    '      section.style.clipPath = `inset(${preFocusRect.top}px ${vw - preFocusRect.right}px ${vh - preFocusRect.bottom}px ${preFocusRect.left}px)`;\n'
    '      section.offsetHeight;\n'
    "      section.style.transition = 'clip-path 0.4s cubic-bezier(0.4,0,0.2,1)';\n"
    "      section.style.clipPath = 'inset(0px 0px 0px 0px)';\n"
    '    }\n'
    '    function exitFocus() {\n'
    "      if (!preFocusRect) { section.classList.remove('focused'); document.body.classList.remove('gallery-focus'); return; }\n"
    '      const vw = window.innerWidth, vh = window.innerHeight, r = preFocusRect;\n'
    "      section.style.transition = 'clip-path 0.4s cubic-bezier(0.4,0,0.2,1)';\n"
    '      section.style.clipPath = `inset(${r.top}px ${vw - r.right}px ${vh - r.bottom}px ${r.left}px)`;\n'
    '      setTimeout(() => {\n'
    "        section.classList.remove('focused'); document.body.classList.remove('gallery-focus');\n"
    "        section.style.clipPath = ''; section.style.transition = ''; preFocusRect = null;\n"
    '      }, 400);\n'
    '    }'
)

pat_simple = re.compile(
    r'function enterFocus\(\)\s*\{[^}]*\}\s*function exitFocus\(\)\s*\{[^}]*\}',
    re.DOTALL
)

aug_path = os.path.join(base, 'project-augustin.html')
with open(aug_path) as f:
    content = f.read()
new_content, n = pat_simple.subn(new_simple, content, count=1)
if n == 0:
    print('NO MATCH: project-augustin.html')
else:
    with open(aug_path, 'w') as f:
        f.write(new_content)
    print('Updated (simple): project-augustin.html')
