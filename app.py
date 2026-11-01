from __future__ import annotations

import html
import os
import re
from datetime import date, datetime
from pathlib import Path
from xml.sax.saxutils import escape

import markdown
import yaml
from flask import Flask, Response, abort, jsonify, render_template, url_for

BASE_DIR = Path(__file__).resolve().parent
CONTENT_DIR = BASE_DIR / "content"
POSTS_DIR = CONTENT_DIR / "posts"

SITE = {
    "name": "devsecops.log",
    "tagline": "Exploring AI, automation, infrastructure and everything I learn along the way.",
    "url": os.environ.get("SITE_URL", "https://example.pages.dev").rstrip("/"),
}

MD_EXTENSIONS = ["extra", "fenced_code", "codehilite", "toc", "sane_lists"]
MD_CONFIG = {"codehilite": {"guess_lang": False, "css_class": "codehilite"}}
WORDS_PER_MINUTE = 200

app = Flask(__name__)

_cache: dict = {"signature": None, "posts": []}


def load_markdown_file(path: Path):
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return yaml.safe_load(parts[1]) or {}, parts[2].strip()
    return {}, text


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _to_date(value, fallback_path: Path) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value.strip())
        except ValueError:
            pass
    return datetime.fromtimestamp(fallback_path.stat().st_mtime).date()


def _to_tags(value) -> list[str]:
    if not value:
        return []
    if isinstance(value, str):
        value = value.split(",")
    return [str(tag).strip() for tag in value if str(tag).strip()]


def _plain_text(rendered_html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", rendered_html)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def _build_post(path: Path) -> dict:
    meta, body = load_markdown_file(path)
    converter = markdown.Markdown(extensions=MD_EXTENSIONS, extension_configs=MD_CONFIG)
    content = converter.convert(body)
    plain = _plain_text(content)
    tags = _to_tags(meta.get("tags"))
    excerpt = str(meta.get("excerpt") or "").strip()
    if not excerpt:
        excerpt = plain[:160].rstrip() + ("..." if len(plain) > 160 else "")
    return {
        "slug": path.stem,
        "title": str(meta.get("title") or path.stem.replace("-", " ").title()),
        "date": _to_date(meta.get("date"), path),
        "tags": [{"name": tag, "slug": slugify(tag)} for tag in tags],
        "excerpt": excerpt,
        "content": content,
        "plain": plain,
        "reading_time": max(1, round(len(plain.split()) / WORDS_PER_MINUTE)),
        "draft": bool(meta.get("draft", False)),
    }


def load_posts() -> list[dict]:
    paths = sorted(POSTS_DIR.glob("*.md"))
    signature = tuple((p.name, p.stat().st_mtime_ns) for p in paths)
    if signature != _cache["signature"]:
        posts = [_build_post(p) for p in paths]
        posts = [p for p in posts if not p["draft"]]
        posts.sort(key=lambda p: (p["date"], p["title"]), reverse=True)
        _cache.update(signature=signature, posts=posts)
    return _cache["posts"]


def all_tags() -> list[dict]:
    tags: dict[str, dict] = {}
    for post in load_posts():
        for tag in post["tags"]:
            entry = tags.setdefault(tag["slug"], {**tag, "count": 0})
            entry["count"] += 1
    return sorted(tags.values(), key=lambda t: t["name"].lower())


def load_page(filename: str, default_title: str) -> dict:
    path = CONTENT_DIR / filename
    if not path.exists():
        return {"title": default_title, "html": "<p>Nothing here yet.</p>", "image": None, "image_alt": "", "pdf": None}
    meta, body = load_markdown_file(path)
    html_body = markdown.markdown(body, extensions=MD_EXTENSIONS, extension_configs=MD_CONFIG)
    return {
        "title": str(meta.get("title") or default_title),
        "html": html_body,
        "image": meta.get("image"),
        "image_alt": str(meta.get("image_alt") or "Portrait"),
        "pdf": meta.get("pdf"),
    }


@app.context_processor
def inject_globals():
    return {"site": SITE, "now": datetime.now()}


@app.route("/")
def index():
    return render_template("index.html", posts=load_posts()[:6])


@app.route("/blog/")
def blog_index():
    return render_template("blog.html", posts=load_posts(), tags=all_tags())


@app.route("/blog/<slug>/")
def post(slug):
    posts = load_posts()
    for i, item in enumerate(posts):
        if item["slug"] == slug:
            newer = posts[i - 1] if i > 0 else None
            older = posts[i + 1] if i + 1 < len(posts) else None
            return render_template("post.html", post=item, newer=newer, older=older)
    abort(404)


@app.route("/tags/<slug>/")
def tag(slug):
    tags = {t["slug"]: t for t in all_tags()}
    if slug not in tags:
        abort(404)
    posts = [p for p in load_posts() if any(t["slug"] == slug for t in p["tags"])]
    return render_template("tag.html", tag=tags[slug], posts=posts)


@app.route("/about/")
def about():
    return render_template("about.html", about=load_page("about.md", "About me"))


@app.route("/resume/")
def resume():
    return render_template("resume.html", page=load_page("resume.md", "Resume"))


@app.route("/search/")
def search():
    return render_template("search.html")


@app.route("/search-index.json")
def search_index():
    entries = [
        {
            "title": p["title"],
            "url": url_for("post", slug=p["slug"]),
            "date": p["date"].isoformat(),
            "tags": [t["name"] for t in p["tags"]],
            "excerpt": p["excerpt"],
            "body": p["plain"],
        }
        for p in load_posts()
    ]
    return jsonify(entries)


@app.route("/sitemap.xml")
def sitemap():
    paths = [url_for(e) for e in ("index", "blog_index", "about", "resume", "search")]
    paths += [url_for("post", slug=p["slug"]) for p in load_posts()]
    paths += [url_for("tag", slug=t["slug"]) for t in all_tags()]
    urls = "".join(f"<url><loc>{escape(SITE['url'] + p)}</loc></url>" for p in paths)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    )
    return Response(xml, mimetype="text/xml")


# Served with 200 so the freezer can write it; Cloudflare Pages uses 404.html automatically.
@app.route("/404.html")
def not_found_page():
    return render_template("404.html")


@app.errorhandler(404)
def handle_404(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=int(os.environ.get("PORT", 5001)))
