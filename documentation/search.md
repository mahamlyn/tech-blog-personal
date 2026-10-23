# Search

Search runs entirely in the browser because Cloudflare Pages has no server to query.

## How it works
1. At build time `/search-index.json` is generated from all published posts.
2. The header search icon links to `/search/`. On that page `static/js/search.js` fetches the index on the first search, then filters as you type (120 ms debounce).
3. The query is kept in the URL as `?q=term`, so searches can be shared and reloaded.

## Index format

```json
[
  {
    "title": "Post title",
    "url": "/blog/post-slug/",
    "date": "2026-10-20",
    "tags": ["ansible"],
    "excerpt": "Short summary",
    "body": "Plain text of the whole post"
  }
]
```

## Matching and ranking
- The query is split on whitespace and lower-cased. Every term must match somewhere in the post (AND).
- Each term scores: title 10, tags 6, excerpt 3, plus the number of body occurrences (capped at 5).
- Results are sorted by total score, then newest first.
- The snippet is the text around the first matching term. Matches are wrapped in `<mark>` using DOM nodes, so post text is never inserted as HTML.

## Limits and upgrades
Matching is substring-based and has no typo tolerance or stemming. The index contains full post bodies, so it grows with the blog. If it becomes large (hundreds of posts), swap the scoring code for MiniSearch or Lunr, or index only titles, tags and excerpts.
