# Development log

## 2026-10-23 - Initial build
- Planned the site and recorded decisions in [decisions.md](decisions.md).
- Created the Flask app (`app.py`) and the static build script (`build.py`).
- Added templates, mobile-first CSS, theme toggle, navigation script and search script.
- Added three sample posts and a starter about page.
- Generated `static/css/pygments.css` with `scripts/generate_pygments_css.py`.
- Ran `python build.py` successfully: 22 pages including `404.html`, `search-index.json` and `sitemap.xml`.
- Wrote documentation under `documentation/`.
- Not yet done: visual check on real devices and the first Cloudflare Pages deploy.
