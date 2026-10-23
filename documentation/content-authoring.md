# Writing content

## Add a post
Create a markdown file in `content/posts/`. The file name (without `.md`) becomes the URL slug, for example `2026-11-01-my-post.md` is served at `/blog/2026-11-01-my-post/`.

```markdown
---
title: My new post
date: 2026-11-01
tags: [python, tooling]
excerpt: One or two sentences shown on cards and in search results.
draft: false
---

Post body in markdown.
```

## Front matter

| Field | Required | Notes |
| --- | --- | --- |
| `title` | No | Defaults to the file name in title case |
| `date` | No | `YYYY-MM-DD`. Defaults to the file's modified date |
| `tags` | No | A list, or a comma-separated string. Each tag gets a `/tags/<slug>/` page |
| `excerpt` | No | Defaults to the first 160 characters of the post |
| `draft` | No | `true` hides the post from every page, the sitemap and search |

## Markdown features
- Fenced code blocks with a language are highlighted, for example ` ```python `. Always add the language; automatic detection is off.
- Tables, footnotes and definition lists (the `extra` extension).
- Headings get anchor ids (the `toc` extension).
- Wide tables and long code lines scroll inside their own box on mobile.

## Images
Put images in `static/images/` and reference them with an absolute path:

```markdown
![Alt text](/static/images/diagram.png)
```

## About page
Edit `content/about.md`. Front matter fields:

| Field | Notes |
| --- | --- |
| `title` | Page heading |
| `image` | Portrait path, for example `/static/images/me.jpg`. Omit it to hide the photo |
| `image_alt` | Alt text for the portrait |

The photo sits to the left of the text from 640px wide and above it on phones. A square image works best, since it is cropped to a square. Replace the placeholder `static/images/profile.svg` with your photo.

## Preview
Run `python app.py` and open http://127.0.0.1:5001. Changes to markdown files appear on refresh.

## Resume page
Edit `content/resume.md`; it is served at `/resume/` and linked in the header. Headings, lists and tables render as in posts. To offer a download, put the file in `static/files/` and set `pdf: /static/files/resume.pdf` in the front matter; a Download PDF button then appears.
