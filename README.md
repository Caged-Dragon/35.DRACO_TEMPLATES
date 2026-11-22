# CagedDragon Template Showcase

A static design portfolio of **700 sign-in and access templates**: the 60 original Stitch AI designs plus **640 new templates** (32 layouts × 20 industries).

## What's included
- `index.html` — responsive CagedDragon gallery with search, filters, sorting, and **interactive Quick View** previews.
- `catalog.json` — catalogue metadata for all 700 designs.
- `templates/` — HTML and screenshot for every design, each with the 20-colorway selector.
- `tools/` — the generator and screenshot scripts used to create templates 061–700 (see below).
- **14,000 live design variations** — 700 templates × 20 color themes.

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

## How the repaired colorway selector works
Open any design with **Quick view** or **Live preview**. Click the floating **CagedDragon Colorways** control in the lower-right corner and choose one of the 20 palettes. The selected theme immediately updates the page's semantic background, surface, text, primary, secondary, tertiary, border, outline, and related utility colors. Theme switching uses direct CSS overrides based on the actual semantic classes in each page; it does not rely on Tailwind regenerating its stylesheet at runtime. Your chosen palette is saved in the browser and can be changed at any time. A theme can also be passed into a preview URL using `?palette=dragon-amethyst` (or another palette ID).

The original layout, typography, and screenshots remain intact. Hard-coded artwork, raster imagery, and one-off arbitrary color values may retain their source colors by design.

## Run locally
Use a local static server for the gallery and embedded Quick View. This avoids browser restrictions that can affect local-file iframes. From this folder, run:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

The original Stitch exports use Tailwind CDN and Google Fonts, so an internet connection is recommended for individual live previews.

## Before publishing
The “Prepare a project inquiry” button copies a starter inquiry to the visitor's clipboard; it does not send data to a server. Add your business email, WhatsApp link, or lead form backend before making the site public.

You can publish the whole folder as a static site on Vercel, Netlify, GitHub Pages, or another static host.

## Source note
The screenshots and original HTML structure are preserved from the supplied Stitch export. The gallery, CagedDragon identity, interactive previews, repaired colorway selector, and 20 semantic theme palettes were added for this portfolio website.

## Templates 061–700 (generated set)
These 640 templates are plain HTML and CSS with no Tailwind dependency. They read the same `--cd-*` colorway variables as the originals, so the 20-theme selector and the `?palette=` URL parameter work identically.

- **32 layouts** (the last 9 are returning-or-new, cover header card, workspace finder, account chooser, PIN pad, admin console, testimonial split, inline strip and new-device check): centered card, left/right brand panel, glass orbs, top-nav hero, vertical rail, terminal console, editorial masthead, bento grid, stacked layers, diagonal split, hero overlay, airy underline, step-by-step wizard, magic link, phone code (OTP), passkey first, QR sign-in, social only, two-step verify, reset password, create account and mobile bottom sheet.
- **20 industries**: insurance, music streaming, legal, HR, smart home, nonprofit, agritech, news & publishing, plus analytics SaaS, fintech, healthcare, education, e-commerce, travel, gaming, real estate, food & dining, fitness, creative studio and logistics.
- Each combination also varies typography, corner radius, border weight, shadow and background pattern, and ships with its own showcase colorway.
- Brand names such as "Quillbase" and "Carelane" are placeholders. Rename them to the client's brand.
- Working behaviour included: password show/hide, six-box code entry with paste support, multi-step wizard, and responsive layouts down to phone width.

### Adding more
```bash
pip install playwright && python -m playwright install chromium
python tools/generate_templates.py . new_entries.json 701   # third argument = first template number
python tools/render_screenshots.py "$PWD" new_entries.json
```
Add layouts to `LAYOUTS` or industries to `INDUSTRIES` in `tools/generate_templates.py`, set `NL0` and `NI0` in `main()` to the current layout and industry counts (so existing templates are not regenerated), then merge the entries into `catalog.json` and the `templates` array in `index.html`. The generator is deterministic for a given set of lists and start number.

Note: the generated templates load fonts from Google Fonts. Screenshots made offline use fallback fonts, so regenerate them with internet access if you want exact typography in the gallery thumbnails.

## Advanced features in every template
All 700 templates load one shared script, `assets/cd-auth-enhance.js`, which upgrades the forms without changing any design:

- **Inline validation** with accessible messages (`aria-invalid`, `aria-describedby`, `role="alert"`): email format, required fields, minimum password length on sign-up, workspace and domain formats, terms checkbox, and complete one-time codes.
- **Loading and result states**: a spinner on the submit button while the request runs, a screen-reader announcement, and a toast with the result.
- **Passwords**: live strength meter on sign-up screens, a Caps Lock warning, and show/hide buttons that report their state (`aria-pressed`).
- **One-time codes and PINs**: auto-submit when the last digit is entered, a 30-second resend countdown, and keyboard entry on the PIN pad.
- **Accessibility**: correct `autocomplete`, `inputmode` and labels, visible keyboard focus, a "Skip to sign-in" link, and full `prefers-reduced-motion` support.
- **Step wizards** validate the current step before moving on.

### Connecting a real backend
The templates run in demo mode by default (a success toast appears after a short delay). To connect your own authentication, listen for the `cd:submit` event, call `preventDefault()`, and report the outcome with `done()`:

```js
document.addEventListener('cd:submit', async (e) => {
  e.preventDefault();                                   // take over from the demo
  try {
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(e.detail.values),            // { email, password } | { code } | { pin } ...
    });
    e.detail.done(res.ok, res.ok ? 'Signed in' : 'Check your details and try again');
  } catch {
    e.detail.done(false, 'Network error, please try again');
  }
});
```
`e.detail` contains `form`, `values` and `done(ok, message)`. The same event fires for sign-in, sign-up, magic link, reset, code and PIN screens.

Note: the 60 original Stitch templates keep their own page scripts; the shared script adds validation and states on top, and some of them ship with pre-filled demo credentials.
