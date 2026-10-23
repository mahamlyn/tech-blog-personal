# Theming and mobile

## Light and dark theme
- Colours are CSS variables in `static/css/styles.css`. `:root` and `[data-theme="dark"]` define the dark palette (default); `[data-theme="light"]` overrides it.
- The `data-theme` attribute lives on `<html>`. An inline script in `<head>` (in `base.html`) applies the saved choice before first paint to avoid a flash.
- `static/js/site.js` handles the toggle button: it flips the attribute, updates the `theme-color` meta tag and stores the choice in `localStorage` under `theme`.
- First visits are always dark; the OS colour scheme is ignored.

To change the look, edit the variables at the top of `styles.css` (`--accent`, `--bg`, `--surface` and so on).

## Code highlighting
`static/css/pygments.css` is generated and holds two scoped stylesheets: `github-dark` under `[data-theme="dark"]` and `default` under `[data-theme="light"]`. Regenerate it after changing styles:

```powershell
python scripts/generate_pygments_css.py
```

## Fonts
No web fonts are loaded. Body text uses the system sans-serif stack; headings, navigation and code use the system monospace stack.

## Mobile rules
The CSS is mobile-first and widens with `min-width` media queries.

| Breakpoint | Change |
| --- | --- |
| below 640px | One-column cards, hamburger menu |
| 640px | Two-column cards, side-by-side post navigation |
| 720px | Inline navigation, hamburger hidden |
| 1024px | Three-column cards |

Other rules:
- The viewport meta tag includes `viewport-fit=cover`, and the header and footer respect safe-area insets.
- Every button and nav link is at least 44px tall.
- The search input uses 16px text so iOS does not zoom on focus.
- Code blocks and tables scroll horizontally inside their own box; inline code wraps; images are capped at 100% width.
- The menu button toggles `data-nav-open` on the header, and Escape closes it. Without JavaScript the navigation stays visible.
- Nothing depends on hover. Animation is disabled under `prefers-reduced-motion`.

## Testing on mobile
In browser dev tools, check 360px, 390px and 768px widths on the home, blog, post, tag, about and search pages. There should be no horizontal page scroll. Run a Lighthouse mobile audit after deploying.
