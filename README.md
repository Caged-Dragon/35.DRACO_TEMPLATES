# Caged Dragon Sign-in Design Studio

A static storefront-style gallery for 20 distinct sign-in UI concepts. Built with plain HTML, CSS and JavaScript. No framework, database, API, authentication provider, build step or external runtime dependency is required.

## Project structure

- `index.html`, `site.css`, `site.js` — responsive gallery storefront with category filters, search and live preview modal
- `templates/<template-name>/` — each template is an independent folder containing `index.html`, `styles.css`, `script.js` and `README.md`
- `downloads/<template-name>.zip` — ready-to-download archive for each individual design
- `templates.json` — gallery catalogue
- `vercel.json` — static Vercel configuration and basic response headers

## Run locally

Open `index.html` directly, or run a static server from this directory. For example:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`. The gallery fetches `templates.json`, so use a local HTTP server rather than opening the gallery as a `file://` URL. Each template's `index.html` can be opened directly.

## Deploy to Vercel

Import this folder/repository into Vercel and select **Other** as the framework preset. Leave the Build Command and Output Directory empty (or use `.` as the output directory). There is no build step. Deploy.

## UI-only notice

All sign-in pages are front-end design demos. The submit action performs local input checks and displays a demo message only. It does not submit, store, transmit or authenticate credentials. Before production authentication, connect the form to a secure server-side endpoint, implement server validation and CSRF protections, and never store plaintext passwords. Password recovery and account creation are clearly marked as integration placeholders.

## Accessibility and responsiveness

The templates use semantic labels, keyboard-visible focus, accessible password visibility controls, status announcements, touch-friendly inputs, responsive breakpoints and `prefers-reduced-motion` overrides.
