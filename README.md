# CagedDragon Template Showcase

A static portfolio catalogue built from the 60 original Stitch AI authentication designs supplied in this conversation.

## What's included
- `index.html` — responsive CagedDragon gallery with search, filters, sorting, and quick views.
- `catalog.json` — catalogue metadata for all 60 designs.
- `templates/` — original Stitch HTML and screenshot for every design, enhanced with an interactive 20-colorway selector.
- **1,200 live design variations** — 60 templates × 20 color themes.

## The 20 color themes
1. Dragon Amethyst
2. Imperial Gold
3. Oceanic Blue
4. Arctic Azure
5. Emerald Forest
6. Botanical Sage
7. Ruby Velvet
8. Rose Quartz
9. Solar Ember
10. Peach Sunrise
11. Cyber Cyan
12. Glacier Mint
13. Midnight Sapphire
14. Lavender Haze
15. Obsidian Copper
16. Sandstone Bronze
17. Neon Orchid
18. Cherry Blossom
19. Graphite Monochrome
20. Porcelain & Ink

Open any template's Live preview and use the floating CagedDragon Colorways panel in the lower-right corner to switch palettes. The selected colorway is remembered in the browser and can be changed at any time. Each color theme updates the page's semantic background, surface, text, primary, secondary, tertiary, and outline tokens while preserving the original layout and typography. The gallery thumbnail screenshots remain the original Stitch images; open a live HTML preview to switch themes. Decorative artwork or image assets embedded in an original design may retain their source colors.

## Run locally
Open `index.html` in a modern browser. For the most reliable loading of the individual templates, run a local static server from this folder:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

The original Stitch exports use Tailwind CDN and Google Fonts, so an internet connection is recommended for individual live previews.

## Before publishing
The “Prepare a project inquiry” button copies a starter inquiry to the visitor's clipboard; it does not send data to a server. Add your business email, WhatsApp link, or lead form backend before making the site public.

You can publish the whole folder as a static site on Vercel, Netlify, GitHub Pages, or another static host.

## Source note
The screenshots and original HTML structure are preserved from the supplied Stitch export. The gallery, CagedDragon identity, colorway selector, and 20 semantic theme palettes were added for this portfolio website.
