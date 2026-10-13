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

34 pages, laid out on the proposed sitemap from the audit (Section 1.2) and filled with the content of the live site as of 2026-10-08. File names match the live URL paths wherever a live page exists, so the redirect map is mostly one-to-one.

| Group | Pages |
|---|---|
| Home | `index.html` |
| Our Mission | `about.html`, `animal-programs.html`, `donations-helping-animals.html`, `impact.html`*, `financial-transparency.html`* |
| Sweepstakes | `sweepstakes.html` and `raffle-plus.html` (the two entry pages), eight prize pages from one template (`new-porsche-sweepstakes.html`, `1965-porsche-sweepstakes.html`, `new-corvette-sweepstakes.html`, `classic-corvette-sweepstakes.html`, `tesla-sweepstakes.html`, `ev-sweepstakes.html`, `lucid.html`, `cadillac-sweepstakes.html`), `how-it-works.html`†, `faq.html`, `sweepstakes-rules.html`, `previous-winners.html` |
| Get Involved | `donate.html`, `monthly-giving.html`*, `wills-estates.html`, `volunteer.html`*, `corporate-partners.html`* |
| Resources | `blog.html`, `blog-post.html`, `videos-and-more.html`, `pet-tips.html`, `cats-and-dogs.html`, `foods-to-avoid.html`, `hurricanes-and-your-pets.html`, `delaware-residents.html` |
| Contact | `contact.html` |

\* **Proposed** — an audit recommendation with no counterpart on the live site. Placeholder content, flagged with a yellow banner and a "Proposed" tag in the nav.
† **New** — not on the live site, but written only from facts in the live Rules and FAQ.

### How the sweepstakes actually works

Each drawing has one winner, who chooses the prize. A Sweepstakes ticket wins one car or $50,000; a Raffle Plus ticket wins two cars, or $100,000, or one car and $50,000. The prize pages describe the cars on offer — they are not separate sweepstakes.

Drawings are held every six months, so the date moves twice a year. It is written in exactly one place — `DRAWING_DATE` in `content.py` — and the hero, entry forms, Rules and FAQ all read it from there.

On the two entry pages the ticket bundles and prizes are selectable cards rather than dropdowns, with a summary panel that follows the selection. The Raffle Plus form enforces the prize rule (any two cars, or one car and $50,000, or $100,000 on its own).

### "For client review" notes

Dashed coral boxes on some pages mark places where the live site contradicts itself, is out of date, or has content worth a decision (a stale drawing date in the FAQ, a Louisiana-specific hurricane guide, article titles with nothing behind them). They are preview-only: remove each `review_note(...)` call in `build.py` once the client has answered.

### Card details

The live forms collect card number, expiry and CVV in plain text fields. The preview deliberately does not reproduce those fields; it shows a "Secure card payment" placeholder where the payment processor's hosted field will go.

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

Prices, dates, rules, prize specs, winners, the tax ID and contact details are real and come from the live site. Bracketed placeholders (`[1,234]`, `[78]%`) and "placeholder" rating badges mark audit proposals that need real numbers from the org before they could go live. They appear on the "Proposed" pages, on the home page (stat band, trust strip, impact section) and in the footer badge row; the home page newsletter signup is also a proposal. The live site publishes no organization-specific impact figures, which is itself a finding (audit Section 2.5).

## Editing & re-generating

Two files, each with one job:

- `build.py` — header, footer, nav and page layout. One source of truth for navigation, so we don't repeat the current site's "Previous Winners listed twice" problem. To change the nav, edit the `NAV` list at the top.
- `content.py` — the facts and long-form copy carried over from the live site: prices, drawing date, prize specs, rules, FAQ, winners, stories, directories. If the client changes a price or a rule, change it here.

Then run `python build.py`. It rewrites every page, deletes generated pages that are no longer in `PAGES`, and exits non-zero if any internal link or local image is missing.

```
preview/
├── build.py             ← layout, nav, pages
├── content.py           ← facts and copy from the live site
├── README.md
├── *.html               ← generated, do not hand-edit
└── assets/
    ├── css/styles.css   ← design tokens + components
    ├── js/nav.js        ← mobile menu + donate-widget interactions
    └── img/             ← photos pulled from the live site
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
