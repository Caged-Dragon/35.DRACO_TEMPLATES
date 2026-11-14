# Caged Dragon Sign-in Design Studio

A static, Vercel-ready UI showcase containing 20 independently styled sign-in concepts. Each template is plain HTML, CSS, and vanilla JavaScript in its own folder.

## Project structure

- `index.html`, `site.css`, `site.js`: the responsive template gallery and preview modal.
- `templates/<slug>/`: standalone template source (`index.html`, `styles.css`, `script.js`, `README.md`).
- `downloads/<slug>.zip`: individual ZIP for each template, linked from its gallery card.
- `templates.json`: metadata for search, filtering, and the gallery.
- `vercel.json`: static hosting headers and route behavior.

## Run locally

Run `python -m http.server 8080` from this directory, then open `http://localhost:8080`. Serving over HTTP preserves the same relative asset behavior used on Vercel.

## Deploy to Vercel

Import the project root into Vercel. Use the **Other** framework preset, leave the build command empty, and set the output directory to `.`. No install command or environment variables are needed.

## Template contents

Every design is self-contained and uses semantic HTML5, its own responsive CSS, accessible form labels, keyboard-visible focus states, password visibility control, and reduced-motion support. No framework, external image, or remote font is required.

## Important

These forms are UI demonstrations only. They do not authenticate, submit credentials, or send passwords to a server. Connect them to a separately implemented and secured authentication service before production use.
