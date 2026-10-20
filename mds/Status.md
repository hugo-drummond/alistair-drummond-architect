# Status

Last updated: 20 Oct 2026

## Live
- Website: alistairdrummondarchitect.co.za (alistair-drummond-architect.vercel.app)
- GitHub: hugo-drummond/alistair-drummond-architect
- 12 project pages, all with desktop + mobile galleries
- SEO implemented (meta, schema, OG, sitemap, robots.txt)
- Performance optimised (image compression, lazy loading, Vercel cache headers)
- Clip-path focus animation on all project galleries

## Recently completed
- 20 Oct 2026: staging branch + preview URL set up; project page titles now uppercase, weight 300, 28.8px, letter-spacing 0.36em; "Featured Images" heading removed from all project pages; Tulleken → "Tulleken, Betty's Bay", Fernwood, Newlands → "Starke, Newlands" (URLs unchanged)
- Tulleken project page added (12th project), About copy added Oct 2026
- Gallery view locked at page load: phone or desktop gallery picked once, stays put on rotate/resize; phones no longer download hidden slider images
- Gallery layout: flex + object-fit: contain — all images shown at natural dimensions, no cropping
- Portrait-pair detection: JS auto-detects portrait image pairs, applies taller container
- Bulk slide image updates across: augustin, bellevue, camps-bay, cadenza, fernwood, hills-bettys-bay, simpson-tyler

## In progress
- Ongoing slide image replacements (client reviewing locally before each push)

## Backlog
- Remaining slide image updates on other projects
- Bellevue slide 2 — currently uses portrait images, may need further layout refinement
- Contact form backend (currently no submission handler)
- Google Analytics / tracking

## Notes
- Auto-commit hook fires after every Claude response — all changes are auto-committed locally
- Staging link for Alistair: see Stack.md → Deployment
- Always review locally before pushing: `python3 -m http.server 8080`
- Desktop source images live in ~/Desktop/[Project Name]/ folders
