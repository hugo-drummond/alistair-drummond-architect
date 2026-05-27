# Filing Conventions

## Project root
`~/alistair-drummond-architect/`

## Image folders
All images live under `images/[project-slug]/`:

| Folder | Project |
|--------|---------|
| images/augustin/ | Augustin, Tamboerskloof |
| images/bellevue/ | Bellevue Road, Oranjezicht |
| images/cadenza/ | Cadenza, Fernwood |
| images/camps-bay/ | The Drive, Camps Bay |
| images/fernwood/ | Fernwood, Newlands |
| images/gallery/ | Curated gallery page images |
| images/hills-bettys-bay/ | Netherby & Hill, Betty's Bay |
| images/mount-pleasant/ | Mount Pleasant |
| images/simpson-tyler/ | Simpson Tyler, Betty's Bay |
| images/upper-kloof/ | Upper Kloof Street |
| images/van-lienden/ | Van Lienden, Constantia |
| images/van-reenen/ | Van Reenen Street, Newlands |

## Naming convention for new slide images
`slide-[n].jpg` — wide composite (one file, two photos side by side)
`slide-[n]-left.jpg` / `slide-[n]-right.jpg` — separate paired images

Mobile images: `mob-[prefix]-[n].jpg` (e.g. mob-aug-1.jpg)

## Desktop source files (client-supplied)
Client drops source images into `~/Desktop/[Project Name]/`
Copy to the relevant `images/[slug]/` folder before referencing in HTML.
Never reference images from ~/Desktop directly.

## Context files
`~/alistair-drummond-architect/mds/` — all Claude context docs live here.
