# Deploying to Cloudflare Pages

## Deploying with GitHub Actions (manual)
The workflow [.github/workflows/deploy.yml](../.github/workflows/deploy.yml) builds the site and uploads `build/` to the `devsecopslog` Pages project (a Direct Upload project). It only runs when started by hand; pushes do not deploy.

### One-time setup
Add these repository secrets in GitHub under Settings > Secrets and variables > Actions:

| Secret | Where to get it |
| --- | --- |
| `CLOUDFLARE_API_TOKEN` | Cloudflare > My Profile > API Tokens. Use a custom token with Account > Cloudflare Pages > Edit |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare > Workers & Pages overview |

If the public URL changes (for example a custom domain), update `SITE_URL` in the workflow.

### Running a deploy
1. In GitHub open the Actions tab and select **Build and deploy to Cloudflare Pages**.
2. Click **Run workflow**, choose the `main` branch and confirm.
3. The workflow installs dependencies, runs `python build.py` and runs `wrangler pages deploy build`.
4. Check the result at https://devsecopslog.pages.dev.

The repository root must be this folder (`tech-blog-personal`). If it is a parent repository, move the workflow there and add `working-directory: tech-blog-personal` to the steps.

## Settings for Git-connected Pages projects
These apply only if you use a Pages project connected to the git repository instead of the workflow above. Direct Upload projects cannot be switched to git integration.


| Setting | Value |
| --- | --- |
| Root directory | `tech-blog-personal` (if the repository holds several projects) |
| Build command | `pip install -r requirements.txt && python build.py` |
| Build output directory | `build` |

Environment variables:

| Variable | Value |
| --- | --- |
| `PYTHON_VERSION` | A supported Python version, for example `3.12` |
| `SITE_URL` | The public URL, for example `https://yourblog.pages.dev`. Used in `sitemap.xml` |

## Local build

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python build.py
python -m http.server -d build 8000
```

Open http://localhost:8000 and check the pages, search and the theme toggle before pushing.

## What gets deployed
`build/` is generated and ignored by git. It contains the HTML pages, `static/`, `search-index.json`, `sitemap.xml`, `404.html` and `_headers`.

## Headers
`build.py` writes `_headers` with `nosniff`, `Referrer-Policy` and `X-Frame-Options` for all pages, and a one-day cache for `/static/*`. Static files are not fingerprinted, so keep the cache short. Edit the `HEADERS` string in `build.py` to change them.

## Troubleshooting
- **Build fails with `Unexpected status '404 NOT FOUND'`**: a linked file is missing, for example `static/css/pygments.css`. Run `python scripts/generate_pygments_css.py`.
- **A new post is missing**: check that it is not `draft: true` and that its file ends in `.md`.
- **Wrong URLs in the sitemap**: set `SITE_URL` in the Pages environment variables.
- **Old CSS after a deploy**: static files are cached for a day; hard-refresh or lower `max-age`.
