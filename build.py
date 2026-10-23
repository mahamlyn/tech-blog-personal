from __future__ import annotations

from pathlib import Path

from flask_frozen import Freezer

from app import all_tags, app, load_posts

BUILD_DIR = Path(__file__).resolve().parent / "build"

HEADERS = """/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: DENY

/static/*
  Cache-Control: public, max-age=86400
"""

app.config.update(
    FREEZER_DESTINATION=str(BUILD_DIR),
    FREEZER_REMOVE_EXTRA_FILES=True,
)

freezer = Freezer(app)


# Generator names must match the endpoint names they feed.
@freezer.register_generator
def post():
    for item in load_posts():
        yield {"slug": item["slug"]}


@freezer.register_generator
def tag():
    for item in all_tags():
        yield {"slug": item["slug"]}


if __name__ == "__main__":
    urls = freezer.freeze()
    (BUILD_DIR / "_headers").write_text(HEADERS, encoding="utf-8")
    print(f"Built {len(list(urls))} pages into {BUILD_DIR}")
