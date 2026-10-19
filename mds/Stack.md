## Core
- Pure static HTML/CSS/JS — no framework, no build step, no package.json
- Hosting: Vercel (auto-deploys on push to master)
- Repo: github.com/hugo-drummond/alistair-drummond-architect
- Local path: ~/alistair-drummond-architect

## File structure
```
/
├── index.html              Homepage (3-image carousel)
├── projects.html           Project grid
├── gallery.html            Photo gallery
├── contact.html            Contact form + Google Maps
├── project-augustin.html
├── project-bellevue.html
├── project-cadenza.html
├── project-camps-bay.html
├── project-fernwood.html
├── project-hills-bettys-bay.html
├── project-mount-pleasant.html
├── project-simpson-tyler.html
├── project-tulleken.html
├── project-upper-kloof.html
├── project-van-lienden.html
├── project-van-reenen.html
├── style.css               Homepage styles
├── projects.css            Projects grid styles
├── project.css             Shared project page styles (all 12 pages)
├── gallery.css             Gallery page styles
├── contact.css             Contact page styles
├── script.js               Burger menu + homepage slideshow
├── images/
│   ├── augustin/
│   ├── bellevue/
│   ├── cadenza/
│   ├── camps-bay/
│   ├── fernwood/
│   ├── gallery/
│   ├── hills-bettys-bay/
│   ├── mount-pleasant/
│   ├── simpson-tyler/
│   ├── tulleken/
│   ├── upper-kloof/
│   ├── van-lienden/
│   └── van-reenen/
├── vercel.json             Cache headers + CSP
├── robots.txt
├── sitemap.xml
└── mds/                    Claude context files
```

## Gallery system (project pages)
Each project page has:
- `.about-section` (About label + `<p>` paragraphs) above the gallery — leave it out if there is no copy
- `desktopSlides` array — each entry is 1 or 2 image paths
- `mobileSlides` array — each entry is always 1 image path
- View is locked at page load: `innerWidth <= 768` → `view-mobile` class on `<html>` + mobile scroll strip built; otherwise `view-desktop` + slider started
- CSS keys off those classes, not a width media query, so rotating a phone or resizing never swaps the gallery. Don't reintroduce live switching
- Only the chosen gallery's images load (phones skip desktop slides)
- `applyOrientation()` detects portrait images and adds `portrait-slide` / `portrait-pair` classes
- CSS in `project.css` handles focused gallery layout: flex, `object-fit: contain`, natural dimensions

## Conventions
- Wide composite images (two photos side-by-side in one file) go as a solo slide entry: `['images/x/slide-n.jpg']`
- Separate paired images go as: `['images/x/left.jpg', 'images/x/right.jpg']`
- Mobile images are named `mob-[prefix]-[n].jpg`
- New slide images named: `slide-[n].jpg` or `slide-[n]-left.jpg` / `slide-[n]-right.jpg`

## Deployment
- Push master → Vercel auto-deploys (~30s)
- Always use: `/usr/bin/git push origin master`
- Local preview: `python3 -m http.server 8080` from project root
