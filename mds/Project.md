Setup: Claude Code single source of truth. Read at session start.

What: Portfolio website for Alistair Drummond, Cape Town residential architect. Showcases 11 completed projects with image galleries, project descriptions, and contact details.

Audience: Prospective clients, property developers, referral networks in Cape Town.

Pages: Homepage (slideshow) | Projects grid | Gallery | Contact | 11 project detail pages.

Entity: Alistair Drummond Architect. Contact via site contact form. Site owned and managed by Hugo Drummond.

Live URL: alistair-drummond-architect.vercel.app
GitHub: hugo-drummond/alistair-drummond-architect
Local path: ~/alistair-drummond-architect

Hard Rules:
- Static site only. No frameworks, no build tools, no npm.
- Mobile and desktop must both work after any change.
- Never edit mobileSlides when only desktopSlides changes are requested.
- Never push until the client has reviewed changes locally.
- Image edits are desktop-only unless explicitly told otherwise.
- All new images go in the relevant project subfolder under images/.
- Use /usr/bin/git push, not git push (homebrew curl conflict).
