# CagedDragon Showcase — Repair Notes

## Preview repair
- Gallery Quick View now displays the actual template HTML in an iframe rather than a static screenshot.
- The modal passes the current saved colorway to the live preview with a `palette` query parameter.
- Closing Quick View unloads the iframe to avoid leaving hidden active pages behind.

## Colorway repair
- Removed the previous approach that mutated the Tailwind configuration after it had begun compiling styles.
- Added direct CSS overrides for semantic utility classes detected on each template page.
- Handles base color utilities and common state/pseudo variants including hover, focus, group-hover, peer-checked, selection, and placeholder.
- Color values are held in CSS custom properties, so switching between 20 themes updates already-rendered interfaces immediately.
- The selector continues to remember the chosen colorway in local storage.

## Scope
All 60 exported template HTML files retain their original structure and images. Each has the same 20-palette selector.
