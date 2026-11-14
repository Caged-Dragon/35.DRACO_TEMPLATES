# CagedDragon Template Showcase

A static portfolio-style catalogue built from the uploaded Stitch AI authentication template export.

## Included
- `index.html` — responsive CagedDragon template gallery.
- `catalog.json` — catalogue metadata for all 60 designs.
- `templates/` — the original Stitch HTML export for every design, plus its `screen.png` preview.

## Run locally
Open `index.html` in a modern browser. For the most reliable local preview of the original HTML designs, serve this folder with a simple static server, for example:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

The main gallery is self-contained apart from Google Fonts. Original Stitch previews may load Tailwind CSS and fonts from their original CDNs, so an internet connection is recommended when opening an individual live preview.

## Before publishing
The “Prepare a project inquiry” button copies a starter inquiry to the visitor's clipboard. It does not send data to a server. Add your preferred email or WhatsApp contact link if you want visitors to send enquiries directly. The gallery itself works without a backend.

You can publish the whole folder as a static site on Vercel, Netlify, GitHub Pages, or any static web host.

## Source note
The template screenshots and HTML are preserved from the Stitch export supplied in this conversation. The showcase layout, catalogue filters, search, modal preview, and CagedDragon branding were added for this portfolio website.
