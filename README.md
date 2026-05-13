# National Humane Society — Redesign

Two-phase rebuild of [nationalhumanesociety.org](https://nationalhumanesociety.org), driven by a written strategic audit (`National_Humane_Society_Website_Audit.docx`, gitignored).

## Repo layout

```
.
├── preview/                ← static HTML prototype (this is what Vercel deploys)
│   ├── build.py            ← source of truth — regenerates the 25 HTML pages
│   ├── *.html              ← generated; do not hand-edit
│   ├── README.md           ← preview-specific docs
│   └── assets/
│       ├── css/styles.css
│       ├── js/nav.js
│       ├── img/            ← real photos pulled from the live Webflow site
│       └── video/          ← hero background video (mission .mp4 + .webm)
├── vercel.json             ← tells Vercel to serve from preview/
├── .gitignore
└── README.md
```

## Phase 1 — Static preview (current)

A click-through prototype that demos the redesign before any WordPress code is written. Stakeholders review here; iteration is fast because it's just HTML.

Run locally:
```bash
cd preview
python -m http.server 8080
# open http://localhost:8080
```

Regenerate after editing `preview/build.py`:
```bash
cd preview
python build.py
```

## Phase 2 — WordPress block theme (next)

When the preview is approved, the design becomes the spec for a custom WordPress block theme. The CSS variables in `preview/assets/css/styles.css` port directly to `theme.json`; each section in `build.py` becomes a block pattern.

The WP build lives in a **separate repository** (Vercel can't host PHP). Production target is WP Engine or Kinsta.

## Deploying to Vercel

This repo is configured for static deployment of the `preview/` directory.

1. Push this repo to GitHub.
2. Visit [vercel.com/new](https://vercel.com/new), import the repo.
3. Vercel auto-detects `vercel.json`; no further config needed.
4. Every `git push` to the default branch redeploys.

You get a `*.vercel.app` URL to share. Custom domain optional.
