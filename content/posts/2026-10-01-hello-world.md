---
title: Hello, world - why this blog exists
date: 2026-10-01
tags: [meta, writing]
excerpt: A short note on why I'm keeping a plain-markdown blog and how it's put together.
---

I wanted a place to write things down that I would otherwise forget. This blog is a small Flask app that turns markdown files into a static site.

## The setup

- Posts are markdown files with a little YAML at the top.
- The site is built to plain HTML and hosted on Cloudflare Pages.
- Search runs in the browser against a JSON index.

## Why markdown

Markdown keeps writing friction low. A new post is one file:

```markdown
---
title: My new post
date: 2026-10-23
tags: [example]
---

Write here.
```

If something here turns out to be useful to you, great. If not, it will at least be useful to future me.
