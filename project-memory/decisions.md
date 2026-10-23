# Decisions

## 2026-10-23

| Decision | Reason |
| --- | --- |
| Flask for development, Frozen-Flask to build | Matches the existing art website project; Cloudflare Pages only hosts static files. |
| Output is static HTML in `build/` | Cloudflare Pages cannot run a Flask server. |
| Search runs in the browser over `search-index.json` | No server available; a blog this size needs no search library. |
| Tag filtering uses `/tags/<tag>/` pages | Query strings cannot be pre-rendered by the freezer. |
| Posts are markdown files with YAML front matter in `content/posts/` | Same pattern as the art website; easy to write and review in git. |
| Dark theme by default with a light/dark toggle | Requested. Choice is saved in `localStorage`; the OS preference is ignored. |
| Theme implemented with CSS variables and `data-theme` on `<html>` | An inline script sets it before paint, so there is no flash. |
| Two Pygments themes (`github-dark`, `default`) scoped per theme | Code highlighting follows the active theme. |
| Mobile-first CSS, no web fonts | Fast on mobile networks; system and monospace font stacks give the techy look. |
| Header search is a link to `/search/`, not an inline form | Keeps the mobile header compact and avoids duplicate inputs. |
| `README.md` stays minimal; detail lives in `documentation/` | Requested. |
| Out of scope for now: comments, admin UI, RSS | Keep the site simple. |
