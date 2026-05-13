# National Humane Society — Redesign Preview

A static, multi-page click-through prototype of the redesigned site. **Not connected to WordPress yet.** This exists so the team can review and iterate on layout, copy, and the mission/sweepstakes rebalance (audit Section 2.4) *before* committing to a custom block theme.

## How to view it

**Easy:** Double-click `index.html` and click around. Everything works from `file://`.

**Better (recommended for stakeholders):** Run a tiny local server so URLs look clean and a couple of preconnect/font hints behave properly.

```powershell
cd preview
python -m http.server 8080
# then open http://localhost:8080
```

Or in VS Code: install the **Live Server** extension, right-click `index.html`, "Open with Live Server."

## What's built

25 pages, mapped to the proposed sitemap from the audit (Section 1.2):

| Group | Pages |
|---|---|
| Home | `index.html` |
| Our Mission | `about.html`, `programs.html`, `impact.html`, `shelter-partners.html`, `financial-transparency.html` |
| Sweepstakes | `sweepstakes.html` (hub), `sweepstakes-detail.html` (single-prize template), `raffle-plus.html`, `how-it-works.html`, `faq.html`, `rules.html`, `previous-winners.html` |
| Get Involved | `donate.html`, `monthly-giving.html`, `wills-estates.html`, `volunteer.html`, `corporate-partners.html` |
| Resources | `blog.html`, `blog-post.html`, `videos.html`, `pet-care-cats.html`, `pet-care-dogs.html`, `pet-care-hurricane.html` |
| Contact | `contact.html` |

## How the audit's top-10 priorities are addressed

| Audit priority | Where it shows up |
|---|---|
| 1. Fix duplicate "Previous Winners" nav link | Sitemap rebuilt — single, correct entry under Sweepstakes dropdown |
| 2. Remove COVID-19 section | Not present anywhere |
| 3. Eliminate triple-repeated hero | Single, outcome-anchored hero on `index.html` |
| 4. Add trust signals package | Trust strip on home + dedicated `financial-transparency.html` + footer trust grid |
| 5. Rebalance sweepstakes/mission ratio | Mission pillars front-and-center on home; sweepstakes is one well-designed section |
| 6. Replace generic Donate buttons with inline widget | `donate-widget` component on home + `donate.html` + `monthly-giving.html` |
| 7. Build missing content categories | Stories, shelter-partner directory, volunteer signup, newsletter capture, financial transparency, leadership |
| 8. Restructure IA to 5-item nav, split `/animal-info` into 3 pages | Done — `pet-care-cats.html`, `pet-care-dogs.html`, `pet-care-hurricane.html` are separate pages |
| 9. Original rescue-animal photography | Placeholder regions clearly labeled "Original rescue-animal photography goes here" — needs commissioning before launch |
| 10. WordPress block theme | This preview is the spec for that theme |

## Brand spec (from current site CSS)

These tokens live in `assets/css/styles.css` as CSS custom properties and will port directly to `theme.json` when we build the WordPress theme.

- **Fonts** — Paytone One (display), Barlow (body), Gayathri (eyebrows). All Google Fonts.
- **Colors** — `#181733` deep navy, `#fa5853` coral (CTA), `#fbff00` yellow (accent), `#fbf7f2` cream, `#f4f8fb` mist, `#5d6c7b` text-gray.

## Placeholder data

Every number, name, partner, board member, and rating is a clearly-marked placeholder (`[1,234]`, `[Name Placeholder]`, `XX-XXXXXXX`). The current live site has no organization-specific impact figures published, which is itself a finding (audit Section 2.5). Real numbers, real names, real shelter partners, and a real EIN need to come from the org before any of this goes live.

## Editing & re-generating

All page content is in `build.py` — one file, one source of truth for header/footer/nav so we don't repeat the current site's "Previous Winners listed twice" problem. To change the nav, edit the `NAV` list at the top of `build.py` and run `python build.py`.

```
preview/
├── build.py             ← edit content here
├── README.md
├── *.html               ← generated, do not hand-edit
└── assets/
    ├── css/styles.css   ← design tokens + components
    ├── js/nav.js        ← mobile menu + donate-widget interactions
    └── img/             ← (placeholder — drop real photography here later)
```

## Next step: porting to WordPress

When this preview is approved:

1. **Spin up a fresh single-site Local install** (not multisite — multisite adds complexity that this org doesn't need).
2. **Build a custom block theme.** The CSS variables in `styles.css` map 1:1 to `theme.json` color/typography presets. Each section in `build.py` becomes either a block pattern (registered in PHP) or a reusable `core/group` block.
3. **Plugins:** GiveWP (donations + Stripe), Gravity Forms (sweepstakes entries with state/age validation), Rank Math (SEO), and a GTM plugin (or direct theme injection) to preserve the existing GTM container `GTM-PK62TNB5`.
4. **Custom Post Type** for sweepstakes prizes — so the eight separately-built prize pages on the current site collapse into one CMS-driven template (audit Section 3.2).
5. **Migration:** export Webflow CMS content, map blog posts to WP posts, build a 301-redirect map for every existing URL, deploy GTM, then DNS cutover with a 30-day Webflow fallback (audit Section 5.3).
6. **Push to production hosting.** WP Engine or Kinsta is the audit's recommendation. Push from Local using each host's deployment tooling — both have one-click migrate-from-Local flows.

The static preview is a *design spec*, not a literal precursor — we don't push these HTML files to a host. The HTML defines the look; the WordPress theme implements it with editable blocks underneath.
