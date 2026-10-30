"""
National Humane Society — preview site generator.

Single source of truth for header/footer/nav and page layout. The facts and
long-form copy carried over from the live site live in content.py. Run
`python build.py` to (re)generate every .html file in this directory.

Each page has a status:
  "live"     — has a counterpart on the current site; copy comes from it.
  "new"      — not on the current site, but written only from facts that are.
  "proposed" — not on the current site; placeholder content for discussion.
"new" and "proposed" pages get a banner so nobody mistakes them for live copy.

When we port to a production stack, the LAYOUT here becomes the header and
footer templates, and each PAGE entry becomes a page template.
"""

import html
import json
import re
import sys
from pathlib import Path

import urllib.parse

import content as C

OUT_DIR = Path(__file__).parent

# ---------------------------------------------------------------------------
# Navigation structure (proposed sitemap, audit Section 1.2)
# (label, href, status) — status marks pages that are not on the live site.
# ---------------------------------------------------------------------------
NAV = [
    ("Our Mission", "about.html", [
        ("About", "about.html", "live"),
        ("Animal Programs", "animal-programs.html", "live"),
        ("Donations Helping Animals", "donations-helping-animals.html", "live"),
        ("Impact &amp; Outcomes", "impact.html", "proposed"),
        ("Financial Transparency", "financial-transparency.html", "proposed"),
    ]),
    ("Sweepstakes", "sweepstakes.html", [
        ("Sweepstakes", "sweepstakes.html", "live"),
        ("Raffle Plus", "raffle-plus.html", "live"),
        ("How It Works", "how-it-works.html", "new"),
        ("FAQ", "faq.html", "live"),
        ("Rules", "sweepstakes-rules.html", "live"),
        ("Previous Winners", "previous-winners.html", "live"),
    ]),
    ("Get Involved", "donate.html", [
        ("Donate", "donate.html", "live"),
        ("Monthly Giving", "monthly-giving.html", "proposed"),
        ("Volunteer", "volunteer.html", "proposed"),
        ("Corporate Partners", "corporate-partners.html", "proposed"),
    ]),
    ("Wills &amp; Estates", "wills-estates.html", []),
    ("Resources", "blog.html", [
        ("Educational Messages", "blog.html", "live"),
        ("Videos &amp; More", "videos-and-more.html", "live"),
        ("Pet Tips", "pet-tips.html", "live"),
        ("Cats &amp; Dogs", "cats-and-dogs.html", "live"),
        ("Hurricanes &amp; Your Pets", "hurricanes-and-your-pets.html", "live"),
        ("Delaware Residents", "delaware-residents.html", "live"),
    ]),
    ("Contact", "contact.html", []),
]

STATUS_TAG = {"new": "New", "proposed": "Proposed"}

# Hidden at CJ's request (2026-10-13 and 2026-10-15) until NHS supplies real
# figures and ratings: the home page stat band, trust strip and impact
# section, and the footer badge row. Every number and rating in them is an
# audit placeholder, not NHS data. The markup is kept unchanged; set this to
# True to bring all four back.
SHOW_PLACEHOLDER_STATS = False


def tel(number):
    return "tel:" + number.replace(" ", "-")


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
def nav_tag(status):
    if status in STATUS_TAG:
        return f' <span class="nav-tag">{STATUS_TAG[status]}</span>'
    return ""


def render_nav():
    items = []
    for label, href, children in NAV:
        if children:
            kids = "\n".join(
                f'        <a href="{c_href}">{c_label}{nav_tag(c_status)}</a>'
                for c_label, c_href, c_status in children
            )
            items.append(f"""    <div class="nav-item">
      <a class="nav-link" href="{href}">{label} ▾</a>
      <div class="nav-dropdown">
{kids}
      </div>
    </div>""")
        else:
            items.append(f'    <div class="nav-item"><a class="nav-link" href="{href}">{label}</a></div>')
    return "\n".join(items)


def render_header():
    return f"""<header class="site-header">
  <div class="container header-inner">
    <a href="index.html" class="brand" aria-label="National Humane Society — Home">
      <img src="assets/img/logo.png" alt="National Humane Society" class="brand-logo" width="186" height="55">
    </a>
    <nav class="nav-primary" aria-label="Primary">
{render_nav()}
    </nav>
    <div class="header-cta">
      <a class="btn btn-primary btn-donate" href="donate.html"><span class="donate-heart" aria-hidden="true">♥</span>Donate</a>
      <button class="menu-toggle" aria-label="Toggle menu">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M4 7h16M4 12h16M4 17h16"/>
        </svg>
      </button>
    </div>
  </div>
</header>"""


def render_footer():
    columns = []
    for label, _href, children in NAV:
        if not children:
            continue
        links = "\n".join(
            f'          <li><a href="{c_href}">{c_label}{nav_tag(c_status)}</a></li>'
            for c_label, c_href, c_status in children
        )
        columns.append(f"""      <div>
        <h4>{label}</h4>
        <ul>
{links}
        </ul>
      </div>""")
    social = "\n".join(
        f'          <a href="{url}" target="_blank" rel="noopener">{name}</a>'
        for name, url in C.SOCIAL
    )
    address = "<br>".join(C.ADDRESS_LINES[1:])
    # Top-level links with no dropdown get no column above, so they go in the bottom row.
    standalone = " · ".join(
        f'<a href="{href}">{label}</a>' for label, href, children in NAV if not children
    )
    trust = f"""    <div class="footer-trust">
      <div class="badge"><strong>Charity Navigator</strong>Rating placeholder</div>
      <div class="badge"><strong>Candid / GuideStar</strong>Seal placeholder</div>
      <div class="badge"><strong>BBB Wise Giving</strong>Accreditation placeholder</div>
    </div>
""" if SHOW_PLACEHOLDER_STATS else ""
    return f"""<footer class="site-footer">
  <div class="container">
{trust}    <div class="footer-grid">
      <div>
        <div class="footer-brand">National Humane Society</div>
        <p style="font-size:.9rem; color:rgba(255,255,255,.7)">A 501(c)(3) non-profit, tax-exempt charity dedicated to improving the lives of rescue animals across America.</p>
        <p style="font-size:.85rem; margin-top:1rem">
          Order Line: <a href="{tel(C.ORDER_LINE)}">{C.ORDER_LINE}</a><br>
          Customer Service: <a href="{tel(C.CUSTOMER_SERVICE)}">{C.CUSTOMER_SERVICE}</a><br>
          <a href="mailto:{C.EMAIL}">{C.EMAIL}</a>
        </p>
        <p style="font-size:.85rem">{address}</p>
        <div class="footer-social">
{social}
        </div>
      </div>
{chr(10).join(columns)}
    </div>
    <div class="footer-bottom">
      <div class="footer-copy">© 2026 National Humane Society. All rights reserved.</div>
      <div class="footer-links">501(c)(3) tax-exempt charity · {standalone}</div>
      <div class="footer-credit">Made with <span role="img" aria-label="love">❤️</span> by <a href="https://www.bruddasindustries.com/" target="_blank" rel="noopener">Brudda's Industries</a></div>
    </div>
  </div>
</footer>"""


def status_banner(status):
    if status == "proposed":
        return """<div class="status-banner is-proposed"><div class="container"><strong>Proposed addition.</strong> This page is not on the current site. Its content is placeholder for discussion and has not been confirmed by NHS.</div></div>"""
    if status == "new":
        return """<div class="status-banner is-new"><div class="container"><strong>New page.</strong> Not on the current site, but written only from facts in the current Rules and FAQ.</div></div>"""
    return ""


def review_note(html):
    """Preview-only callout for things the client should confirm or decide."""
    return f'<aside class="review-note"><strong>For client review</strong>{html}</aside>'


# Extra scripts for single pages. The Previous Winners confetti (CJ,
# 2026-10-19) plays on every load for now; set SHOW_WINNERS_CONFETTI to False
# to turn it off.
SHOW_WINNERS_CONFETTI = True
PAGE_SCRIPTS = {
    "previous-winners.html": ["assets/js/confetti.js"] if SHOW_WINNERS_CONFETTI else [],
    # turns the featured-post blockquote into Instagram's own post embed
    "videos-and-more.html": ["https://www.instagram.com/embed.js"],
}

# Section backgrounds that are not white (see styles.css)
COLOURED_SECTIONS = {"section-soft", "section-cream", "section-navy"}


def page(title, slug, body, status="live", description=None):
    """Returns the full html string for a single page."""
    desc = description or f"{title} — National Humane Society"
    body_class = "is-home" if slug == "index.html" else "is-interior"
    extra_scripts = "".join(f'<script src="{src}" async></script>\n' if src.startswith("http") else f'<script src="{src}"></script>\n'
                            for src in PAGE_SCRIPTS.get(slug, []))
    # A page that ends on a coloured section runs straight into the footer,
    # with no white gap between them.
    last_section = re.findall(r'<section class="([^"]*)"', body)
    if last_section and set(last_section[-1].split()) & COLOURED_SECTIONS:
        body_class += " ends-on-colour"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — National Humane Society</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title} — National Humane Society">
<meta property="og:description" content="{desc}">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700&family=Gayathri:wght@400;700&family=Paytone+One&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
</head>
<body class="{body_class}">
{render_header()}
<main>
{status_banner(status)}
{body}
</main>
{render_footer()}
<button class="preview-flag" id="previewFlag" aria-label="Preview build — hover and click X to dismiss" title="This is a preview build">
  <span class="preview-flag-icon" aria-hidden="true">&#x1F6A7;</span>
  <span class="preview-flag-close" aria-label="Dismiss preview indicator">&times;</span>
</button>
<script src="assets/js/nav.js"></script>
{extra_scripts}</body>
</html>
"""


# ---------------------------------------------------------------------------
# Reusable content blocks
# ---------------------------------------------------------------------------
# Header photos carried over from the current site (2026-10-20). Off for now:
# CJ preferred the plain headers. Set SHOW_PAGE_HEADER_IMAGES to True to put
# the photos back. Keyed by the page's breadcrumb label. Each page uses the photo the current site uses
# for it. Pages not listed keep the plain header. The Sweepstakes, Raffle Plus
# and car pages have their own navy header and are not affected.
# (file, alt text, crop position)
SHOW_PAGE_HEADER_IMAGES = False
PAGE_HEADER_IMAGES = {
    "About": ("header-dog-goggles.jpg", "A dog in goggles and a Hawaiian shirt", "30% 60%"),
    "Educational Messages": ("header-dog-goggles.jpg", "A dog in goggles and a Hawaiian shirt", "30% 60%"),
    "Videos &amp; More": ("header-dog-goggles.jpg", "A dog in goggles and a Hawaiian shirt", "30% 60%"),
    "Animal Programs": ("header-cats-leaping.jpg", "Two cats leaping for a feather toy", "50% 50%"),
    "Contact": ("header-cat-glasses.jpg", "A cat wearing glasses being petted", "20% 75%"),
    "Previous Winners": ("header-cat-glasses.jpg", "A cat wearing glasses being petted", "20% 75%"),
    "Donations Helping Animals": ("header-puppy-kennel.jpg", "A puppy with an orange bow being petted at a kennel", "40% 60%"),
    "FAQ": ("header-puppy-kennel.jpg", "A puppy with an orange bow being petted at a kennel", "40% 60%"),
    "Rules": ("header-puppy-kennel.jpg", "A puppy with an orange bow being petted at a kennel", "40% 60%"),
    "Wills &amp; Estates": ("header-dogs-kennel.jpg", "Dogs looking out from behind a kennel gate", "50% 40%"),
}


def page_hero(title, lead, breadcrumb_label, parent=None):
    crumb = '<a href="index.html">Home</a> &nbsp;/&nbsp; '
    if parent:
        crumb += f'<a href="{parent[1]}">{parent[0]}</a> &nbsp;/&nbsp; '
    lead_html = f'\n    <p class="lead">{lead}</p>' if lead else ""
    photo = PAGE_HEADER_IMAGES.get(breadcrumb_label) if SHOW_PAGE_HEADER_IMAGES else None
    if photo:
        src, alt, focus = photo
        return f"""
<section class="page-hero has-photo">
  <div class="container page-hero-grid">
    <div>
      <div class="breadcrumb">{crumb}{breadcrumb_label}</div>
      <h1>{title}</h1>{lead_html}
    </div>
    <div class="page-hero-photo"><img src="assets/img/{src}" alt="{alt}" style="object-position:{focus}" width="1200" height="800"></div>
  </div>
</section>
"""
    return f"""
<section class="page-hero">
  <div class="container">
    <div class="breadcrumb">{crumb}{breadcrumb_label}</div>
    <h1>{title}</h1>{lead_html}
  </div>
</section>
"""


def paragraphs(items):
    return "\n".join(f"      <p>{p}</p>" for p in items)


def bullet_list(items, cls="list-check"):
    lis = "\n".join(f"        <li>{i}</li>" for i in items)
    return f'      <ul class="{cls}">\n{lis}\n      </ul>'


def ticket_tiers(kind):
    """kind: 'sweepstakes' or 'raffle-plus' — picks the price column and the
    entry page. Each card links to that page's entry form with the bundle
    already selected (nav.js reads ?tickets=)."""
    page = "sweepstakes.html" if kind == "sweepstakes" else "raffle-plus.html"
    cards = []
    for bought, free, sweeps_price, plus_price, popular in C.TICKET_TIERS:
        price = sweeps_price if kind == "sweepstakes" else plus_price
        noun = "Ticket" if bought == 1 else "Tickets"
        badge = '<span class="tier-badge"><span aria-hidden="true">★</span> Most Popular</span>' if popular else ""
        cls = "tier-card is-popular" if popular else "tier-card"
        cards.append(f"""      <a class="{cls}" href="{page}?tickets={bought}#enter">
        {badge}
        <h3>Buy {bought} {noun}</h3>
        <p class="tier-free">Get {free} Free!</p>
        <p class="tier-price">${price}</p>
        <span class="tier-cta">Choose <span aria-hidden="true">→</span></span>
      </a>""")
    return '    <div class="tier-grid">\n' + "\n".join(cards) + "\n    </div>"


PAYMENT_BLOCK = """        <div class="payment-placeholder">
          <strong>Secure card payment</strong>
          <p>Preview only. In production the card number, expiry and security code are typed into a field hosted by the payment processor, so card details never pass through or get stored on this website.</p>
        </div>"""

PERSON_FIELDS = """        <div class="form-row"><label>Full name</label><input type="text" autocomplete="name" required></div>
        <div class="grid grid-2">
          <div class="form-row"><label>Phone number</label><input type="tel" autocomplete="tel" required></div>
          <div class="form-row"><label>Email address</label><input type="email" autocomplete="email" required></div>
        </div>
        <div class="form-row"><label>Street address</label><input type="text" autocomplete="street-address" required></div>
        <div class="grid grid-3">
          <div class="form-row"><label>City</label><input type="text" autocomplete="address-level2" required></div>
          <div class="form-row"><label>State</label><input type="text" autocomplete="address-level1" required></div>
          <div class="form-row"><label>Zip code</label><input type="text" inputmode="numeric" autocomplete="postal-code" required></div>
        </div>"""


def ticket_choices(kind):
    """Ticket bundles as selectable cards (radio inputs) for the entry form."""
    cards = []
    for bought, free, sweeps_price, plus_price, popular in C.TICKET_TIERS:
        price = sweeps_price if kind == "sweepstakes" else plus_price
        noun = "Ticket" if bought == 1 else "Tickets"
        badge = '<span class="choice-badge"><span aria-hidden="true">★</span> Most Popular</span>' if popular else ""
        cls = "choice-card ticket-choice is-popular" if popular else "choice-card ticket-choice"
        summary = f"{bought} {noun.lower()} + {free} free"
        cards.append(f"""            <label class="{cls}">
              <input type="radio" name="tickets" value="{bought}" data-price="{price}" data-label="{summary}" required>
              {badge}
              <span class="ticket-count">{bought} {noun}</span>
              <span class="ticket-free">+ {free} free</span>
              <span class="ticket-price">${price}</span>
            </label>""")
    return "\n".join(cards)


def prize_choice(label, image, input_type, kind="car"):
    if image:
        thumb = f"<span class=\"choice-thumb\" style=\"background-image:url('assets/img/{image}')\"></span>"
    else:
        amount = label.split(" ")[0].replace(".00", "")
        thumb = f'<span class="choice-thumb is-cash">{amount}</span>'
    required = " required" if input_type == "radio" else ""
    return f"""            <label class="choice-card prize-choice">
              <input type="{input_type}" name="prize" value="{label}" data-kind="{kind}"{required}>
              {thumb}
              <span class="choice-label">{label}</span>
            </label>"""


def entry_form(kind):
    """The live 'Secure Form' for Sweepstakes or Raffle Plus, minus raw card fields."""
    if kind == "sweepstakes":
        title = "Sweepstakes Secure Form"
        heading = "Enter the Sweepstakes."
        prize_legend = "Choose your prize"
        prize_help = "Select one car or $50,000.00."
        prizes = "\n".join(prize_choice(label, image, "radio")
                           for label, image in C.SWEEPSTAKES_PRIZE_OPTIONS)
    else:
        title = "Raffle Plus Secure Form"
        heading = "Enter Raffle Plus."
        prize_legend = "Choose your prizes"
        prize_help = 'Pick any two cars, $100,000.00, or one car and $50,000.00. <span class="prize-count" data-prize-count></span>'
        prizes = "\n".join(prize_choice(label, image, "checkbox", option_kind)
                           for label, image, option_kind in C.RAFFLE_PLUS_PRIZE_OPTIONS)
    sources = "".join(f"<option>{s}</option>" for s in C.AD_SOURCES)
    return f"""
<section class="section entry-section" id="enter">
  <div class="container">
    <div class="entry-head">
      <p class="eyebrow">{title}</p>
      <h2>{heading}</h2>
    </div>
    <form class="entry-form" data-entry onsubmit="event.preventDefault(); alert('Preview only — entries are not submitted.');">
      <div class="entry-steps">
        <fieldset class="entry-step">
          <legend><span class="step-num">1</span> Select number of tickets</legend>
          <div class="choice-grid choice-tickets">
{ticket_choices(kind)}
          </div>
        </fieldset>

        <fieldset class="entry-step">
          <legend><span class="step-num">2</span> {prize_legend}</legend>
          <p class="step-help">{prize_help}</p>
          <div class="choice-grid choice-prizes">
{prizes}
          </div>
        </fieldset>

        <fieldset class="entry-step">
          <legend><span class="step-num">3</span> Your information</legend>
          <div class="form-grid form-wide">
{PERSON_FIELDS}
            <div class="form-row"><label>Where did you see our ad? (select one)</label>
              <select><option value="">Select one...</option>{sources}</select>
            </div>
            <div class="form-row"><label>Comment</label><textarea rows="3"></textarea></div>
          </div>
        </fieldset>

        <fieldset class="entry-step">
          <legend><span class="step-num">4</span> Your payment information</legend>
{PAYMENT_BLOCK}
          <label class="check-item" style="margin-top:var(--space-4)"><input type="checkbox"> I want to automatically be entered into future raffles with this payment information.</label>
        </fieldset>
      </div>

      <aside class="entry-summary">
        <h3>Your entry</h3>
        <dl>
          <dt>Tickets</dt><dd data-sum="tickets">Not selected yet</dd>
          <dt>Prize</dt><dd data-sum="prize">Not selected yet</dd>
          <dt>Next drawing</dt><dd>{C.DRAWING_DATE}</dd>
        </dl>
        <div class="entry-total"><span>Total</span><strong data-sum="total">—</strong></div>
        <button type="submit" class="btn btn-primary btn-lg">Enter Now</button>
        <ul class="entry-assurances">
          <li>Ticket number(s) emailed within 48 hours</li>
          <li>No need to be present to win</li>
        </ul>
        <p class="form-footnote">Please remember to spay or neuter your pets. For any questions, please call us at <a href="{tel(C.CUSTOMER_SERVICE)}">{C.CUSTOMER_SERVICE}</a>.</p>
      </aside>
    </form>
  </div>
</section>
"""


def gallery(slides, count_label=None, autoplay=None, cls="prize-gallery"):
    """Swipeable photo strip; arrows and dots page through it (nav.js).
    slides: [(car name, image, link)]. autoplay: milliseconds between slides."""
    slides_html = "\n".join(
        f"""          <a class="prize-slide" href="{href}" style="background-image:url('assets/img/{image}')"{'' if i == 0 else ' tabindex="-1"'}>"""
        + (f'<span class="prize-slide-name">{name}</span>' if len(slides) > 1 else f'<span class="visually-hidden">{name}</span>')
        + "</a>"
        for i, (name, image, href) in enumerate(slides)
    )
    controls = ""
    if len(slides) > 1:
        dots = "".join(
            f'<button type="button" aria-label="Show {name}"{active}></button>'
            for i, (name, *_rest) in enumerate(slides)
            for active in [' class="is-active"' if i == 0 else ""]
        )
        count = f'\n        <span class="gallery-count">{count_label}</span>' if count_label else ""
        controls = f"""{count}
        <button class="gallery-btn gallery-prev" type="button" aria-label="Previous car">‹</button>
        <button class="gallery-btn gallery-next" type="button" aria-label="Next car">›</button>
        <div class="gallery-dots">{dots}</div>"""
    timer = f' data-autoplay="{autoplay}"' if autoplay else ""
    return f"""      <div class="{cls}" data-gallery{timer}>
        <div class="prize-slides">
{slides_html}
        </div>{controls}
      </div>"""


def prize_gallery(slug, cars):
    """Photo strip for one prize card: every car that prize page offers."""
    return gallery([(name, image, slug) for name, _note, image, _specs in cars],
                   count_label=f"{len(cars)} models")


def car_lineup_gallery(start=0):
    """Hero gallery on the entry pages: every car on the entry form, cycling
    on its own. start: which car shows first."""
    cars = C.CAR_PRIZES[start:] + C.CAR_PRIZES[:start]
    return gallery([(label, image, page) for label, image, page in cars],
                   count_label=f"{len(cars)} cars to choose from", autoplay=4500,
                   cls="prize-gallery sweeps-hero-gallery")


def cash_card(amount, title, text):
    """Cash prize card. Not a link (there is no cash prize page), but it keeps
    the card hover effects."""
    return f"""    <article class="prize-card prize-card-cash">
      <div class="cash-face">
        <span class="cash-note">Cash prize</span>
        <span class="cash-amount">{amount}</span>
      </div>
      <div class="prize-body">
        <h3>{title}</h3>
        <p>{text}</p>
      </div>
    </article>"""


SWEEPS_CASH = [cash_card("$50,000", "$50,000.00 Cash", "Take the cash instead of a car.")]
RAFFLE_CASH = [
    cash_card("$50,000", "$50,000.00 Cash", "Pair it with any one car."),
    cash_card("$100,000", "$100,000.00 Cash", "Take the whole prize in cash."),
]


def prize_cards(cash=SWEEPS_CASH, slugs=None, cash_row=False):
    """slugs: limit (and order) the cards, e.g. the shorter home page set.
    cash: the cash cards to add at the end.
    cash_row: on the entry pages, cars sit four across (eight cars, two even
    rows) and the cash cards get their own row underneath; the home page
    keeps everything in one three-across grid."""
    prizes = {p[0]: p for p in C.PRIZES}
    chosen = [prizes[s] for s in slugs] if slugs else C.PRIZES
    cards = []
    for slug, label, headline, sub, _tagline, _image, cars in chosen:
        if sub and sub != label:
            detail = sub
        elif len(cars) > 1:
            detail = ", ".join(car[0] for car in cars)
        else:
            detail = headline
        cards.append(f"""    <article class="prize-card">
{prize_gallery(slug, cars)}
      <div class="prize-body">
        <h3><a href="{slug}">{label}</a></h3>
        <p>{detail}</p>
      </div>
    </article>""")
    if cash_row:
        wide = [c.replace('class="prize-card prize-card-cash"', 'class="prize-card prize-card-cash is-wide"') for c in cash]
        return ('    <div class="grid prize-grid-4">\n' + "\n".join(cards) + "\n    </div>\n"
                '    <div class="cash-row">\n      <p class="eyebrow">Or take the cash</p>\n'
                '      <div class="cash-grid">\n' + "\n".join(wide) + "\n      </div>\n    </div>")
    cards.extend(cash)
    return '    <div class="grid grid-3">\n' + "\n".join(cards) + "\n    </div>"


def ticket(href, tag, title, detail, variant):
    """A call-to-action shaped like a raffle ticket: the "Enter now" stub is
    split off by a perforation. variant: 'ticket-yellow' or 'ticket-navy',
    plus 'ticket-hero' (sits on the video) or 'ticket-stacked' (tag above title)."""
    tag_html = f'<span class="ticket-tag">{tag}</span>\n        ' if tag else ""
    detail_html = f"<small>{detail}</small>" if detail else ""
    return f"""<a class="ticket {variant}" href="{href}">
      <span class="ticket-main">
        {tag_html}<span class="ticket-text"><strong>{title}</strong>{detail_html}</span>
      </span>
      <span class="ticket-stub">Enter now <span class="ticket-arrow" aria-hidden="true">→</span></span>
    </a>"""


_ONE_TICKET = C.TICKET_TIERS[0]  # (tickets, free, sweepstakes $, raffle plus $, popular)
# Used on Previous Winners, whose section heading already gives the drawing
# date, so the tickets leave it out (CJ, 2026-10-19).
SWEEPS_CTA = f"""    <div class="cta-pair">
    {ticket("raffle-plus.html", "Raffle Plus", "Win two cars or $100,000",
            f"Tickets from ${_ONE_TICKET[3]}", "ticket-yellow ticket-stacked")}
    {ticket("sweepstakes.html", "Sweepstakes", "Win one car or $50,000",
            f"Tickets from ${_ONE_TICKET[2]}", "ticket-navy ticket-stacked")}
    </div>"""

# Prize pages list Sweepstakes before Raffle Plus everywhere (hero buttons,
# per-car buttons, ticket switch), so their ticket pair follows the same order;
# it stacks Sweepstakes first on small screens too. Other pages keep SWEEPS_CTA.
SWEEPS_CTA_SWEEPS_FIRST = f"""    <div class="cta-pair">
    {ticket("sweepstakes.html", "Sweepstakes", "Win one car or $50,000",
            f"Tickets from ${_ONE_TICKET[2]} · Drawing {C.DRAWING_DATE}", "ticket-navy ticket-stacked")}
    {ticket("raffle-plus.html", "Raffle Plus", "Win two cars or $100,000",
            f"Tickets from ${_ONE_TICKET[3]} · Drawing {C.DRAWING_DATE}", "ticket-yellow ticket-stacked")}
    </div>"""

# Hidden on 2026-10-19 at CJ's request: the Enter now ticket pair at the bottom
# of the car pages. The hero and every car already link to both entry forms,
# so it was one set of buttons too many. The ticket switch and price cards
# above it stay. Set this to True to bring the pair back.
SHOW_PRIZE_PAGE_TICKET_PAIR = False
PRIZE_PAGE_TICKET_PAIR = f"""    <div style="margin-top:var(--space-7)">
{SWEEPS_CTA_SWEEPS_FIRST}
    </div>"""


# Colours for winners with no photo, in turn (the Educational Messages palette)
WINNER_TILE_COLOURS = ["navy", "coral", "teal", "blue", "orange"]


def winners_wall(winners=None):
    """Winner cards (the Previous Winners page, and the row on the entry, FAQ
    and Rules pages). Winners with no photo get a colour-coded paw-print tile
    with their initials."""
    cards, blank = [], 0
    for name, state, image in (C.WINNERS if winners is None else winners):
        if image:
            pic = f"""<div class="winner-pic"><img src="assets/img/{image}" alt="{name}, {state}" loading="lazy" decoding="async"></div>"""
        else:
            initials = "".join(part[0] for part in name.split()[:2]).upper()
            colour = WINNER_TILE_COLOURS[blank % len(WINNER_TILE_COLOURS)]
            blank += 1
            pic = f"""<div class="winner-pic winner-blank is-{colour}" aria-hidden="true"><span class="winner-initials">{initials}</span></div>"""
        cards.append(f"""      <article class="winner-tile">
        {pic}
        <div class="winner-info"><h3>{name}</h3><span class="winner-state">{state}</span></div>
      </article>""")
    return '    <div class="winner-wall">\n' + "\n".join(cards) + "\n    </div>"


def winners_strip():
    return f"""
<section class="section section-soft">
  <div class="container">
    <div class="section-head">
      <h2>Previous Winners</h2>
      <a class="btn btn-secondary" href="previous-winners.html">See all winners →</a>
    </div>
{winners_wall([w for w in C.WINNERS if w[2]][:8])}
  </div>
</section>
"""


def donate_amount_buttons(default=25):
    """Monthly and one-time share every preset except the largest."""
    shared = [a for a in C.DONATE_MONTHLY if a in C.DONATE_ONE_TIME]
    top_monthly = [a for a in C.DONATE_MONTHLY if a not in shared][0]
    top_one_time = [a for a in C.DONATE_ONE_TIME if a not in shared][0]
    buttons = []
    for amount in shared:
        active = " is-active" if amount == default else ""
        buttons.append(f'        <button type="button" class="amount-btn{active}" data-amount="{amount}">${amount}</button>')
    buttons.append(f'        <button type="button" class="amount-btn" data-amount="{top_monthly}" data-monthly="{top_monthly}" data-one-time="{top_one_time}">${top_monthly}</button>')
    buttons.append('        <button type="button" class="amount-btn" data-amount="other">Other</button>')
    return "\n".join(buttons)


DONATE_TOGGLE = """      <div class="donate-toggle">
        <button type="button" class="is-active" data-mode="monthly">Monthly</button>
        <button type="button" data-mode="one-time">One-time</button>
      </div>"""


# The live blog posts have no cover images, so each card gets a colour-coded
# header naming its category (C.BLOG_CATEGORIES).
BLOG_COLOUR = dict(C.BLOG_CATEGORIES)
CATEGORY_KEY = {name: name.lower().replace(" & ", "-").replace(" ", "-") for name, _c in C.BLOG_CATEGORIES}


def blog_cards(posts, filterable=False):
    """Article cards. filterable: tag each card with its category for the
    filter bar on the Educational Messages page."""
    cards = []
    for title, slug, category in posts:
        if slug == C.BLOG_SAMPLE_SLUG:
            href, target = "blog-post.html", ""
        else:
            href, target = f"{C.LIVE_SITE}/post/{slug}", ' target="_blank" rel="noopener"'
        tag = f' data-category="{CATEGORY_KEY[category]}"' if filterable else ""
        cards.append(f"""      <article class="post-card"{tag}>
        <div class="post-cover is-{BLOG_COLOUR[category]}" aria-hidden="true">
          <span class="post-cover-topic">{html.escape(category)}</span>
        </div>
        <div class="post-body">
          <h3><a href="{href}"{target}>{html.escape(title, quote=False)}</a></h3>
          <span class="post-more">Read article →</span>
        </div>
      </article>""")
    grid = ' data-post-grid' if filterable else ""
    return f'    <div class="grid grid-3"{grid}>\n' + "\n".join(cards) + "\n    </div>"


def blog_filter_bar():
    """Category chips with counts; nav.js filters the cards and pages them."""
    counts = {}
    for _t, _s, cat in C.BLOG_POSTS:
        counts[cat] = counts.get(cat, 0) + 1
    chips = [f'<button type="button" class="filter-chip is-active" data-filter="all" aria-pressed="true">All <span>{len(C.BLOG_POSTS)}</span></button>']
    for name, _colour in C.BLOG_CATEGORIES:
        chips.append(f'<button type="button" class="filter-chip" data-filter="{CATEGORY_KEY[name]}" aria-pressed="false">{html.escape(name)} <span>{counts.get(name, 0)}</span></button>')
    return '    <div class="filter-bar" role="toolbar" aria-label="Filter articles by category">\n      ' + "\n      ".join(chips) + "\n    </div>"


def story_excerpt(index, words=38):
    title, image, signature, paras = C.STORIES[index]
    text = " ".join(paras[0].split()[:words]) + "…"
    pic = f"style=\"background-image:url('assets/img/{image}')\"" if image else ""
    return f"""      <div class="story-card">
        <div class="story-image" {pic}></div>
        <div class="story-body">
          <blockquote>“{text}”</blockquote>
          <cite>{signature}</cite>
        </div>
      </div>"""


MISSION_PILLARS = [
    ("Rescuing and Protecting Animals in Need", "Providing lifesaving care, rehabilitation, and support to vulnerable animals, while working to ensure their long-term well-being and quality of life."),
    ("Advocating for Lasting Change", "Confronting cruelty at its root through research, policy reform, and systemic advocacy, especially where animals face the greatest and most entrenched harm."),
    ("Educating and Empowering Communities", "Helping people understand the issues animals face and encouraging responsible choices, including spaying and neutering, to prevent needless suffering and save lives."),
    ("Promoting Compassion and Respect", "Leading with respect and compassion as we work alongside our partners, supporters, and communities to build a more humane future for the animals."),
]


def pillars(grid="grid-4"):
    cards = "\n".join(f"""      <div class="pillar">
        <div class="pillar-num">{i:02d}</div>
        <h3>{title}</h3>
        <p>{text}</p>
      </div>""" for i, (title, text) in enumerate(MISSION_PILLARS, 1))
    return f'    <div class="grid {grid}">\n{cards}\n    </div>'


MAIL_ADDRESS = "<br>".join(C.ADDRESS_LINES)

# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

# --- HOMEPAGE ---------------------------------------------------------------
COVID_ITEMS = "\n".join(f"""        <div class="qa-card">
          <span class="qa-mark" aria-hidden="true">?</span>
          <div>
            <h3>{q}</h3>
            <p>{a}</p>
          </div>
        </div>""" for q, a in C.COVID_QA)

# Placeholder stat band + trust strip that sat under the hero; shown only when
# SHOW_PLACEHOLDER_STATS is True (see the top of this file).
HOME_PLACEHOLDER_BANDS = f"""<!-- Stat band — audit proposal; numbers are placeholders until NHS supplies them -->
<section class="hero-stat-band">
  <div class="container">
    <div class="hero-stat-strip">
      <div><span class="stat-num">[123]</span><span class="stat-label">Shelter partners supported</span></div>
      <div><span class="stat-num">[1,234]</span><span class="stat-label">Animals placed (2025)</span></div>
      <div><span class="stat-num">[1.2M]</span><span class="stat-label">Animals helped to date</span></div>
      <div><span class="stat-num">[$12M]</span><span class="stat-label">Granted to programs</span></div>
    </div>
  </div>
</section>

<!-- Trust strip — audit Section 3.4; ratings are placeholders -->
<section class="trust-strip">
  <div class="container trust-grid">
    <div class="trust-badge"><strong>Charity Navigator</strong>Rating placeholder</div>
    <div class="trust-badge"><strong>Candid Platinum</strong>Seal placeholder</div>
    <div class="trust-badge"><strong>BBB Wise Giving</strong>Accreditation placeholder</div>
  </div>
</section>
"""

HELP_CARDS = [
    # (title, text, button, href, colour, blob, icon) — copy, icons and colours from the current homepage
    ("Sweepstakes", "What is better than helping animals in need while winning some incredible prizes?",
     "Enter Now", "sweepstakes.html", "orange", "blob-1.png", "help-icon-dog.png"),
    ("Our Programs", "These animals need our help. Learn about the ways our organization helps our furry friends in need.",
     "Learn More", "animal-programs.html", "teal", "blob-2.png", "help-icon-cat.png"),
    ("Donate", "Your donations go a long way to help ensure these animals find a forever home, happy and healthy.",
     "Donate Now", "donate.html", "blue", "blob-3.png", "help-icon-clipboard.png"),
]
HELP_CARD_HTML = "\n".join(f"""      <div class="help-card is-{colour}">
        <div class="help-blob" style="background-image:url('assets/img/{blob}')"><img src="assets/img/{icon}" alt="" width="84" height="84"></div>
        <h3>{title}</h3>
        <p>{text}</p>
        <a class="help-btn" href="{href}">{button}</a>
      </div>""" for title, text, button, href, colour, blob, icon in HELP_CARDS)

LEARN_HOW_TO_HELP = f"""<!-- Learn How To Help (cards from the current homepage; it sits under the videos, as on the live page) -->
<section class="section section-soft help-section">
  <div class="container">
    <div class="text-center" style="max-width:680px; margin:0 auto var(--space-7)">
      <p class="eyebrow">Get involved</p>
      <h2>Learn How To Help</h2>
    </div>
    <div class="grid grid-3 help-grid">
{HELP_CARD_HTML}
    </div>
  </div>
</section>
"""


PAW_ICON = (
    '<svg class="paw-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<ellipse cx="12" cy="15.6" rx="5.2" ry="4.4"/>'
    '<ellipse cx="5.2" cy="9.6" rx="2.1" ry="2.7"/><ellipse cx="9.1" cy="5.8" rx="2.2" ry="2.9"/>'
    '<ellipse cx="14.9" cy="5.8" rx="2.2" ry="2.9"/><ellipse cx="18.8" cy="9.6" rx="2.1" ry="2.7"/></svg>'
)


def embed_loader(label="Loading video…", fallback=None):
    """Shown while a video or post loads: three paw prints bouncing in turn.
    nav.js fades it out when the embed is ready; if it takes over ~10 s the
    fallback link (href, text) appears. In a card it just sits behind the
    thumbnail, which covers it once loaded."""
    link = ""
    if fallback:
        href, text = fallback
        link = f'<a class="embed-loader-fallback" href="{href}" target="_blank" rel="noopener">{text}</a>'
    return (f'<div class="embed-loader" role="status"><span class="embed-loader-paws">{PAW_ICON * 3}</span>'
            f'<span class="embed-loader-text">{label}</span>{link}</div>')


def edu_video_carousel():
    """YouTube Shorts from the educational playlist. Each card links to the
    video and plays it in place when JavaScript is on (see nav.js)."""
    cards = "\n".join(f"""      <a class="short-card" href="https://www.youtube.com/shorts/{vid}" data-video="{vid}" target="_blank" rel="noopener">
        {embed_loader("Loading…")}
        <img src="https://i.ytimg.com/vi/{vid}/oar2.jpg" alt="" loading="lazy">
        <span class="short-play" aria-hidden="true"></span>
        <span class="short-title">{title}</span>
      </a>""" for vid, title in C.EDU_VIDEOS)
    return f"""<!-- Educational videos (YouTube playlist, as on the current homepage) -->
<section class="section edu-videos" data-carousel>
  <div class="container">
    <div class="section-head">
      <div>
        <p class="eyebrow">Educational videos</p>
        <h2>Meet Kapiolani</h2>
        <p class="lead">{C.EDU_PLAYLIST_INTRO}</p>
      </div>
      <div class="carousel-controls">
        <button class="carousel-btn" type="button" data-dir="-1" aria-label="Previous videos">←</button>
        <button class="carousel-btn" type="button" data-dir="1" aria-label="Next videos">→</button>
      </div>
    </div>
    <div class="short-track">
{cards}
    </div>
    <p class="edu-videos-more"><a href="{C.EDU_PLAYLIST_URL}" target="_blank" rel="noopener">Watch the whole playlist on YouTube →</a></p>
  </div>
</section>"""


# Prize cards in the home page's Raffle Plus section. CJ asked for six cards
# at most; with both Raffle Plus cash cards that leaves four cars (the ones
# with several models, so their photo strips show the most). The full set
# stays on the Sweepstakes and Raffle Plus pages.
HOME_PRIZES = [
    "new-porsche-sweepstakes.html",
    "new-corvette-sweepstakes.html",
    "ev-sweepstakes.html",
    "lucid.html",
]

# Impact section — audit proposal; the three figures are placeholders. Shown
# only when SHOW_PLACEHOLDER_STATS is True.
HOME_IMPACT_PLACEHOLDER = """
<!-- Impact — audit proposal; the three figures are placeholders -->
<section class="section section-navy">
  <div class="container">
    <div class="text-center" style="max-width:680px; margin:0 auto var(--space-7)">
      <p class="eyebrow">The problem</p>
      <h2>4 to 6 million animals are euthanized every year.</h2>
      <p class="lead" style="margin:0 auto">Through no fault of their own more than 7 million dogs and cats end up in shelters and breed rescues every year. Only one half of them will find a home.</p>
    </div>
    <div class="grid grid-3">
      <div class="stat-block coral"><span class="num">[1,234]</span><span class="label">Animals placed in homes (2025)</span></div>
      <div class="stat-block"><span class="num">[$1.2M]</span><span class="label">Granted to shelter partners</span></div>
      <div class="stat-block coral"><span class="num">[123]</span><span class="label">Active shelter partners</span></div>
    </div>
    <div class="text-center" style="margin-top:var(--space-6)">
      <a class="btn btn-yellow" href="impact.html">See full impact report →</a>
    </div>
  </div>
</section>
"""

HOME_BODY = f"""
<section class="hero-video">
  <video autoplay muted loop playsinline preload="metadata"
         poster="assets/video/humane-mission-poster.jpg">
    <source src="assets/video/humane-mission.webm" type="video/webm">
    <source src="assets/video/humane-mission.mp4" type="video/mp4">
  </video>
  <div class="container hero-content">
    <p class="eyebrow">A 501(c)(3) non-profit, tax-exempt charity</p>
    <h1>Working to end suffering for all animals.</h1>
    <p class="lead">Every year, an estimated 4 to 6 million animals are euthanized. Our goals: to assist with spay/neutering and veterinary care for those in need, and to help fund local shelters.</p>
    <div style="display:flex; gap:12px; flex-wrap:wrap; margin-top:var(--space-5)">
      <a class="btn btn-primary btn-lg btn-donate" href="donate.html"><span class="donate-heart" aria-hidden="true">♥</span>Donate Today</a>
      <a class="btn btn-ghost btn-lg" href="about.html">Our Mission</a>
    </div>
    {ticket("raffle-plus.html", "Raffle Plus", "Win two cars or $100,000", f"Drawing {C.DRAWING_DATE}", "ticket-yellow ticket-hero")}
  </div>
</section>

{HOME_PLACEHOLDER_BANDS if SHOW_PLACEHOLDER_STATS else ''}{edu_video_carousel()}

{LEARN_HOW_TO_HELP}

<!-- Mission pillars (verbatim from current /about page) -->
<section class="section">
  <div class="container">
    <div class="text-center" style="max-width:760px; margin:0 auto var(--space-7)">
      <p class="eyebrow">Our Mission</p>
      <h2>Every animal deserves love and safety.</h2>
      <p class="lead" style="margin:0 auto">The National Humane Society is dedicated to protecting animals from suffering and improving their lives through compassionate action, education, advocacy and policy change.</p>
    </div>
{pillars()}
  </div>
</section>

<!-- Raffle Plus — the home page's prize section (CJ, 2026-10-18). The
     Raffle Plus ticket is the featured one; the Sweepstakes keeps its own
     Enter now ticket beside it. -->
<section class="section section-soft">
  <div class="container">
    <div class="text-center" style="max-width:760px; margin:0 auto var(--space-6)">
      <p class="eyebrow">Raffle Plus · Drawing {C.DRAWING_DATE}</p>
      <h2>Drive home your dream cars while helping animals in need.</h2>
      <p class="lead" style="margin:0 auto">Choose prizes ranging from Porsche, Corvettes, Teslas, and more! Every entry supports our mission. It's a win-win!</p>
    </div>
    <div class="cta-pair">
    {ticket("raffle-plus.html", "Raffle Plus", "Win two cars or $100,000",
            f"Tickets from ${_ONE_TICKET[3]}", "ticket-yellow ticket-stacked ticket-featured")}
    {ticket("sweepstakes.html", "Sweepstakes", "Win one car or $50,000",
            f"Tickets from ${_ONE_TICKET[2]}", "ticket-navy ticket-stacked")}
    </div>
    <div style="margin-top:var(--space-7)">
{prize_cards(cash=RAFFLE_CASH, slugs=HOME_PRIZES)}
    </div>
    <div class="text-center" style="margin-top:var(--space-6)">
      <a class="btn btn-secondary" href="raffle-plus.html#prizes">See all prizes →</a>
    </div>
  </div>
</section>

<!-- Inline donate widget — audit Section 3.1 -->
<section class="section">
  <div class="container grid grid-2" style="align-items:center">
    <div>
      <p class="eyebrow">Donate</p>
      <h2>Every dollar can make a difference for an animal in need.</h2>
      <p>For over 25 years, the National Humane Society has worked tirelessly to put an end to animal abuse and neglect. We are one of the national leaders in the areas of rescue, adoption and welfare, and your tax-deductible donation will help fight cruelty and make a life-changing difference for animals across America.</p>
      <a class="btn btn-secondary" href="donate.html">Other ways to give →</a>
    </div>
    <div class="donate-widget" data-donate>
      <h3>Select gift amount</h3>
{DONATE_TOGGLE}
      <div class="amount-grid">
{donate_amount_buttons()}
      </div>
      <a class="btn btn-primary donate-cta" href="donate.html" style="width:100%; justify-content:center">Donate $25 monthly →</a>
    </div>
  </div>
</section>

<!-- About Us + Make A Difference (verbatim from the current homepage, with its photos) -->
<section class="section photo-panels">
  <div class="container">
    <div class="photo-panel">
      <div class="photo-panel-img" style="background-image:url('assets/img/home-about-dog.jpg')" role="img" aria-label="A small white dog in a red sweater giving a high five"></div>
      <div class="photo-panel-card">
      <p class="eyebrow">About Us</p>
      <p>The National Humane Society (The NHS) is a 501(c)(3) Non-Profit Tax Exempt Charity organization dedicated to improving the lives of rescue animals across America. We stand with shelters and humane societies around the country in the mission to find abandoned animals homes and to help rectify the over-population crisis of dogs and cats in the US.</p>
      <p>Through our efforts each year, and through the generous donations of our supporters, the National Humane Society aids and assists in funding individual shelters to give volunteers and the animals they serve a fighting chance of making a change. We actively support and engage with communities to improve perceptions of adopting animals, and to protect the animals in question. Our belief is that through education and conversation, we can be the change needed for animals around the country.</p>
      </div>
    </div>
    <div class="photo-panel is-flipped">
      <div class="photo-panel-img" style="background-image:url('assets/img/home-difference-cat.jpg')" role="img" aria-label="A tabby cat wearing a slice of bread around its face"></div>
      <div class="photo-panel-card">
      <p class="eyebrow">Make A Difference</p>
      <p>Your tax deductible contributions help us combat the animal abuse and animal overpopulation in the United States. The National Humane Society is the difference between living and dying. Your money is genuinely changing the lives of millions of cats and dogs in the United States.</p>
      <p>Through no fault of their own more than 7 million dogs and cats end up in shelters and breed rescues every year. Only one half of them will find a home. Donations to the National Humane Society go to shelters and breed rescues nationwide.</p>
      <a class="btn btn-primary" href="donations-helping-animals.html">See where donations go →</a>
      </div>
    </div>
  </div>
</section>

<!-- COVID-19 & Your Pets (verbatim from the current homepage; under Make A Difference, as on the live page) -->
<section class="section section-cream covid-section">
  <div class="container covid-grid">
    <div>
      <p class="eyebrow">Pet health</p>
      <h2>COVID-19 &amp; Your Pets</h2>
      <div class="qa-list">
{COVID_ITEMS}
      </div>
    </div>
    <div class="covid-photo">
      <img src="assets/img/home-covid-pet.jpg" alt="A small terrier wearing a nurse's cap and a toy stethoscope" width="570" height="618" loading="lazy">
    </div>
  </div>
</section>

<!-- Stories (excerpts from the current /donations-helping-animals page) -->
<section class="section">
  <div class="container">
    <div class="text-center" style="max-width:680px; margin:0 auto var(--space-6)">
      <p class="eyebrow">Donations helping animals</p>
      <h2>Some of the animals your generous donations have helped.</h2>
    </div>
    <div class="grid grid-3">
{story_excerpt(0)}
{story_excerpt(2)}
{story_excerpt(3)}
    </div>
    <div class="text-center" style="margin-top:var(--space-6)">
      <a class="btn btn-secondary" href="donations-helping-animals.html">Read their stories →</a>
    </div>
  </div>
</section>

<!-- Latest educational messages -->
<section class="section section-soft">
  <div class="container">
    <div class="section-head">
      <div>
        <p class="eyebrow">Resources</p>
        <h2>Educational Messages</h2>
      </div>
      <a class="btn btn-secondary" href="blog.html">All articles →</a>
    </div>
{blog_cards(C.BLOG_POSTS[:3])}
  </div>
</section>

{HOME_IMPACT_PLACEHOLDER if SHOW_PLACEHOLDER_STATS else ''}
"""

# --- ABOUT ------------------------------------------------------------------
ABOUT_BODY = page_hero(
    "Mission Statement",
    "The National Humane Society is dedicated to protecting animals from suffering and improving their lives through compassionate action, education, advocacy and policy change. We believe every animal deserves love and safety, and we work every day to make that belief a reality.",
    "About",
) + f"""
<section class="section">
  <div class="container">
    <p class="eyebrow text-center">Our Mission</p>
    <h2 class="text-center" style="margin-bottom:var(--space-7)">We carry out our mission by:</h2>
{pillars("grid-2")}
  </div>
</section>

<section class="section section-soft">
  <div class="container-narrow">
    <p class="lead">Together, we give animals a voice and work daily toward a world where animals are no longer abused or forgotten. Each year, spay and neuter programs help save millions of animals, yet far too many still lose their lives simply because there are not enough homes. Lasting change is only possible with the help of compassionate people who are willing to speak up and take action.</p>
  </div>
</section>

<section class="section section-cream">
  <div class="container">
    <div class="text-center" style="margin-bottom:var(--space-7)">
      <p class="eyebrow">Support our work</p>
      <h2>Ways to give</h2>
    </div>
    <div class="give-grid">
      <article class="give-card">
        <span class="give-icon" aria-hidden="true">✉</span>
        <h3>Contribute by mail</h3>
        <p>To contribute by mail, please send a personal check or money order made payable to the National Humane Society at:</p>
        <div class="envelope">
          <span class="envelope-stamp" aria-hidden="true">{PAW_ICON}</span>
          <span class="envelope-to">Mail to</span>
          <address>{MAIL_ADDRESS}</address>
        </div>
      </article>
      <article class="give-card give-card-online">
        <span class="give-icon" aria-hidden="true">♥</span>
        <p class="eyebrow">A 501(c)(3) tax-exempt charity</p>
        <h3>Donate online</h3>
        <p>Give once or monthly in a few minutes. Donations are <span class="nowrap">tax-deductible</span>.</p>
        <a class="btn btn-primary btn-lg btn-donate" href="donate.html"><span class="donate-heart" aria-hidden="true">♥</span>Donate online</a>
        <p class="give-more">Planning a gift in your will? <a href="wills-estates.html">Wills &amp; Estates →</a></p>
      </article>
    </div>
  </div>
</section>
"""

# --- DONATIONS HELPING ANIMALS ----------------------------------------------
GLOBE_ICON = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">'
    '<circle cx="12" cy="12" r="9.5"/><path d="M2.5 12h19"/><path d="M12 2.5c2.6 2.6 3.9 5.8 3.9 9.5s-1.3 6.9-3.9 9.5c-2.6-2.6-3.9-5.8-3.9-9.5s1.3-6.9 3.9-9.5z"/></svg>'
)


def site_link(url, label):
    """An organisation's website as a small reference-style link: globe,
    domain, arrow, coral underline. `label` is read out by screen readers."""
    domain = url.split("//", 1)[-1].split("/", 1)[0].removeprefix("www.")
    return (f'<a class="site-link" href="{url}" target="_blank" rel="noopener" aria-label="{label} (opens in a new tab)">'
            f'<span class="site-link-globe" aria-hidden="true">{GLOBE_ICON}</span>{domain}'
            f'<span class="site-link-arrow" aria-hidden="true">↗</span></a>')

# Stories longer than this many characters start collapsed with a
# "Read the full story" button (nav.js).
STORY_COLLAPSE_AT = 1200


def story_long(story, i=0):
    """A story card: photo (or a paw-print tile when there's none) beside the
    text, the name as a heading and the sign-off as a signature. Photo and
    text swap sides on alternate stories."""
    title, image, signature, paras = story
    extras = C.STORY_EXTRAS.get(title, {})
    photos = ([image] if image else []) + extras.get("photos", [])
    if len(photos) > 1:
        # several photos: a cycling photo strip (the same one the prize pages use)
        slides = "\n".join(
            f'          <div class="prize-slide" style="background-image:url(\'assets/img/{p}\')" role="img" aria-label="{title}, photo {n}"></div>'
            for n, p in enumerate(photos, 1))
        dots = "".join(f'<button type="button" aria-label="Show photo {n}"{active}></button>'
                       for n in range(1, len(photos) + 1)
                       for active in [' class="is-active"' if n == 1 else ""])
        pic = f"""<div class="prize-gallery story-gallery" data-gallery data-autoplay="4000">
        <div class="prize-slides">
{slides}
        </div>
        <span class="gallery-count">{len(photos)} photos</span>
        <button class="gallery-btn gallery-prev" type="button" aria-label="Previous photo">‹</button>
        <button class="gallery-btn gallery-next" type="button" aria-label="Next photo">›</button>
        <div class="gallery-dots">{dots}</div>
      </div>"""
    elif image:
        pic = f'<img src="assets/img/{image}" alt="{title}" loading="lazy">'
    else:
        colour = ["coral", "teal", "blue", "orange"][i % 4]
        pic = f'<div class="winner-blank is-{colour} story-blank" aria-hidden="true"><span class="winner-initials">{title}</span></div>'
    long = sum(len(p) for p in paras) > STORY_COLLAPSE_AT
    body = f"""        <div class="story-text{' is-collapsible' if long else ''}"{' data-collapsible' if long else ''}>
{paragraphs(paras)}
        </div>"""
    toggle = (f'\n        <button type="button" class="story-toggle" data-story-toggle aria-expanded="false">'
              f'Read {title}\'s full story <span aria-hidden="true">↓</span></button>') if long else ""
    flipped = " is-flipped" if i % 2 else ""
    website = ""
    if "website" in extras:
        website = "\n        <p class=\"story-site\">" + site_link(*extras["website"]) + "</p>"
    return f"""    <article class="story-card-long{flipped}">
      <div class="story-media">{pic}</div>
      <div class="story-content">
        <h3>{title}</h3>
{body}{toggle}
        <p class="story-sign"><span aria-hidden="true">{PAW_ICON}</span>{signature}</p>{website}
      </div>
    </article>"""


LOGO_ROW = "\n".join(
    f"""      <figure class="partner-card"><div class="partner-logo"><img src="assets/img/{img}" alt="{name} logo" loading="lazy"></div></figure>"""
    for img, name in C.PARTNER_LOGOS
)

DONATIONS_BODY = page_hero(
    "Donations Helping Animals",
    "These are the shelters and animal groups that we have recently given money to.",
    "Donations Helping Animals",
) + f"""
<section class="section">
  <div class="container">
    <p class="eyebrow text-center">Shelters &amp; rescues we've supported</p>
    <div class="partner-row">
{LOGO_ROW}
    </div>
  </div>
</section>

<section class="impact-band">
  <div class="container">
    <p class="impact-band-head">Without your help this would not be possible.</p>
    <p class="impact-band-text">These groups shelter, feed, provide veterinarian care and rescue animals from storms.</p>
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <div class="text-center" style="max-width:760px; margin:0 auto var(--space-7)">
      <p class="eyebrow">Their stories</p>
      <h2>Below are some of the recent animals your generous donations have helped.</h2>
      <a class="btn btn-primary btn-lg btn-donate" href="donate.html" style="margin-top:var(--space-4)"><span class="donate-heart" aria-hidden="true">♥</span>Donate Today</a>
    </div>
    {review_note("<p>Cupcake's letter is published on the current site alongside a photo of the family's credit statement. The photo is left out here, and the letter itself is a request for help rather than an outcome — worth deciding whether it stays.</p>")}
    <div class="story-list">
{chr(10).join(story_long(st, i) for i, st in enumerate(C.STORIES))}
    </div>
  </div>
</section>
"""

# --- SWEEPSTAKES + RAFFLE PLUS (entry pages) --------------------------------
# The live page's headline lineup disagreed with its entry form (Tesla Model S
# and 3, no Cadillac). CJ confirmed the entry form is right (2026-10-15), so
# the lineup now lists exactly the cars on the form (C.CAR_PRIZES).
CAR_LINEUP = """    <ul class="lineup">
      <li><strong>Porsche</strong> 911 Carrera Cabriolet, Taycan, Macan S, 1965 356C</li>
      <li><strong>Corvette</strong> Stingray, E-Ray, Classic 1967</li>
      <li><strong>Tesla</strong> Model Y</li>
      <li><strong>Rivian</strong> R1T, R1S</li>
      <li><strong>Lucid</strong> Gravity, Air</li>
      <li><strong>Cadillac</strong> Escalade</li>
    </ul>"""


def sweeps_hero(crumb, eyebrow, headline, lead, first_car, ticket_fact, gallery_html=None, actions=None, actions_html=None):
    """Navy hero for the entry pages and the prize pages, with the facts people
    ask about first. Entry pages show every prize car; prize pages pass their
    own gallery and their own buttons (actions_html: ticket buttons)."""
    actions = actions or [("Enter Now", "#enter", "btn-primary"), ("See the prizes", "#prizes", "btn-ghost")]
    buttons = actions_html or "\n".join(f'        <a class="btn {cls} btn-lg" href="{href}">{label}</a>' for label, href, cls in actions)
    return f"""
<section class="sweeps-hero">
  <div class="container sweeps-hero-grid">
    <div>
      <div class="breadcrumb">{crumb}</div>
      <p class="eyebrow">{eyebrow}</p>
      <h1>{headline}</h1>
      <p class="lead">{lead}</p>
      <div class="hero-actions">
{buttons}
      </div>
    </div>
{gallery_html or car_lineup_gallery(first_car)}
  </div>
  <div class="container">
    <div class="fact-strip">
      <div><span class="fact-label">Next drawing</span><span class="fact-value">{C.DRAWING_DATE}</span></div>
      <div><span class="fact-label">Tickets</span><span class="fact-value">{ticket_fact}</span></div>
      <div><span class="fact-label">To win</span><span class="fact-value">No need to be present</span></div>
      <div><span class="fact-label">Ticket numbers</span><span class="fact-value">Emailed within 48 hours</span></div>
    </div>
  </div>
</section>
"""


def upsell(eyebrow, text, label, href):
    return f"""
<section class="upsell-band">
  <div class="container upsell">
    <div>
      <p class="eyebrow">{eyebrow}</p>
      <p class="upsell-text">{text}</p>
    </div>
    <a class="btn btn-yellow" href="{href}">{label}</a>
  </div>
</section>
"""


SWEEPSTAKES_BODY = sweeps_hero(
    '<a href="index.html">Home</a> &nbsp;/&nbsp; Sweepstakes',
    "Sweepstakes",
    'Win a new car or <span class="hl">$50,000.00!</span>',
    "Choose prizes ranging from Porsche, Corvettes, Teslas, and more! Every entry supports our mission. It's a win-win!",
    0,  # starts on the Porsche 911
    f"From ${C.TICKET_TIERS[0][2]}",
) + f"""
<section class="section" id="prizes">
  <div class="container">
    <div class="section-head">
      <div>
        <p class="eyebrow">The prizes</p>
        <h2>One winner. Your choice of car — or $50,000.00.</h2>
      </div>
    </div>
{CAR_LINEUP}
{prize_cards(cash_row=True)}
  </div>
</section>
""" + upsell(
    "Raffle Plus",
    "Want two cars? A Raffle Plus ticket wins any two cars, $100,000.00, or one car and $50,000.00.",
    "See Raffle Plus →",
    "raffle-plus.html",
) + entry_form("sweepstakes") + winners_strip()

RAFFLE_BODY = sweeps_hero(
    '<a href="index.html">Home</a> &nbsp;/&nbsp; <a href="sweepstakes.html">Sweepstakes</a> &nbsp;/&nbsp; Raffle Plus',
    "Raffle Plus",
    'Win two new cars or <span class="hl">$100,000.00!</span>',
    "Pick any two cars, $100,000.00, or one car and $50,000.00. Every entry supports our mission.",
    4,  # starts on the Corvette
    f"From ${C.TICKET_TIERS[0][3]}",
) + f"""
<section class="section" id="prizes">
  <div class="container">
    <div class="section-head">
      <div>
        <p class="eyebrow">The prizes</p>
        <h2>One winner. Any two cars, one car and $50,000.00 — or $100,000.00.</h2>
      </div>
    </div>
{CAR_LINEUP}
{prize_cards(cash=RAFFLE_CASH, cash_row=True)}
  </div>
</section>
""" + upsell(
    "Sweepstakes",
    "Happy with one car? Sweepstakes tickets are $25.00 and win one car or $50,000.00.",
    "See Sweepstakes →",
    "sweepstakes.html",
) + entry_form("raffle-plus") + winners_strip()


# --- RAFFLE HOME PAGE (landing page; /raffle-home-page on the current site) --
# Laid out like the current page (CJ, 2026-10-29): the car video behind the
# two ways to enter and a button for each car, then the ticket offers (the
# price cards with the Raffle Plus / Sweepstakes switch, CJ's pick over the
# current page's yellow bar). Not in the menus: it is a landing page reached
# from links and ads. Raffle Plus comes first, as it does there.

# The current page's "Enter Our Sweepstakes!" pop-up. It opens a moment after
# the page loads, once per visit. Set this to False to turn it off.
SHOW_RAFFLE_POPUP = True

# The current page's car buttons, in its order, without its $50,000 Cash
# button (CJ, 2026-10-29): (label, prize page)
RAFFLE_HOME_CARS = [
    ("Porsche", "new-porsche-sweepstakes.html"),
    ("Corvette", "new-corvette-sweepstakes.html"),
    ("Tesla", "tesla-sweepstakes.html"),
    ("Rivian", "ev-sweepstakes.html"),
    ("Lucid", "lucid.html"),
    ("Cadillac", "cadillac-sweepstakes.html"),
    ("1965 Porsche", "1965-porsche-sweepstakes.html"),
    ("Classic Corvette", "classic-corvette-sweepstakes.html"),
]


def raffle_home_car_buttons():
    images = {p[0]: p[5] for p in C.PRIZES}
    links = []
    for label, page in RAFFLE_HOME_CARS:
        links.append(f'        <li><a class="rh-car" href="{page}"><img src="assets/img/{images[page]}" alt="" decoding="async">'
                     f'<span class="rh-car-name">{label}<span class="rh-car-arrow" aria-hidden="true">→</span></span></a></li>')
    return '      <ul class="rh-cars-list">\n' + "\n".join(links) + "\n      </ul>"


RAFFLE_HOME_POPUP = f"""
<div class="rh-popup" data-raffle-popup hidden>
  <div class="rh-popup-box" role="dialog" aria-modal="true" aria-labelledby="rh-popup-title">
    <button type="button" class="rh-popup-close" aria-label="Close">×</button>
    <p class="eyebrow">Enter today</p>
    <h2 id="rh-popup-title">Enter Our Sweepstakes!</h2>
    <p class="rh-popup-text">Enter today for a chance to win up to <strong>two new cars</strong> or <strong>$100,000</strong>.</p>
    <div class="rh-popup-logos">
      <img src="assets/img/logo-porsche.png" alt="Porsche">
      <img src="assets/img/logo-corvette.png" alt="Corvette">
      <img src="assets/img/logo-tesla.png" alt="Tesla">
    </div>
    <div class="rh-popup-actions">
      {ticket("raffle-plus.html#enter", None, "Raffle Plus", "Two cars or $100,000", "ticket-yellow ticket-compact")}
      {ticket("sweepstakes.html#enter", None, "Sweepstakes", "One car or $50,000", "ticket-navy ticket-compact")}
    </div>
  </div>
</div>
"""

RAFFLE_HOME_BODY = f"""
<section class="rh-hero">
  <video autoplay muted loop playsinline preload="metadata" poster="assets/video/cars-poster.jpg" aria-hidden="true">
    <source src="assets/video/cars.mp4" type="video/mp4">
  </video>
  <div class="container rh-hero-inner">
    <div class="breadcrumb"><a href="index.html">Home</a> &nbsp;/&nbsp; <a href="sweepstakes.html">Sweepstakes</a> &nbsp;/&nbsp; Enter Today</div>
    <div class="rh-grid">
      <div class="rh-enter">
        <p class="eyebrow">Sweepstakes &amp; Raffle Plus</p>
        <h1>Two ways to win</h1>
        <p class="lead">Pick a Porsche, Corvette, Tesla and more, or take the cash. Every entry supports our mission.</p>
        <div class="rh-tickets">
          {ticket("raffle-plus.html#enter", "Raffle Plus", "Win two cars or $100,000.00", f"Tickets from ${_ONE_TICKET[3]}", "ticket-yellow ticket-stacked")}
          {ticket("sweepstakes.html#enter", "Sweepstakes", "Win one car or $50,000.00", f"Tickets from ${_ONE_TICKET[2]}", "ticket-navy ticket-stacked")}
        </div>
      </div>
      <div class="rh-cars">
        <h2>Explore each car</h2>
{raffle_home_car_buttons()}
      </div>
    </div>
    <div class="fact-strip">
      <div><span class="fact-label">Next drawing</span><span class="fact-value">{C.DRAWING_DATE}</span></div>
      <div><span class="fact-label">Tickets</span><span class="fact-value">From ${_ONE_TICKET[2]} or ${_ONE_TICKET[3]} Raffle Plus</span></div>
      <div><span class="fact-label">To win</span><span class="fact-value">No need to be present</span></div>
      <div><span class="fact-label">Ticket numbers</span><span class="fact-value">Emailed within 48 hours</span></div>
    </div>
  </div>
</section>

<section class="section section-soft" id="tickets">
  <div class="container">
    <div class="text-center" style="max-width:760px; margin:0 auto var(--space-5)">
      <p class="eyebrow">Ticket offers</p>
      <h2>Buy more tickets, get more free</h2>
    </div>
    <div class="tier-switch" data-tier-switch>
      <div class="tier-toggle" role="tablist" aria-label="Ticket type">
        <button type="button" role="tab" aria-selected="true" data-tier="raffle-plus">Raffle Plus<small>Two cars or $100,000</small></button>
        <button type="button" role="tab" aria-selected="false" data-tier="sweepstakes">Sweepstakes<small>One car or $50,000</small></button>
      </div>
      <div data-tier-panel="raffle-plus">
{ticket_tiers("raffle-plus")}
      </div>
      <div data-tier-panel="sweepstakes" hidden>
{ticket_tiers("sweepstakes")}
      </div>
    </div>
  </div>
</section>

<section class="section section-cream tips-closing">
  <div class="container">
    <div class="tips-closing-card raffle-home-mission">
      <p class="eyebrow">Our mission</p>
      <h2>Every entry helps animals in need</h2>
      <p class="tips-closing-text">We are the nation's most effective animal protection &amp; animal welfare organization working to end suffering for all animals.</p>
      <p class="tips-closing-text">Every year, an estimated 4 to 6 million animals are euthanized. Our goals: spay/neutering, veterinary care for those in need and funding local shelters.</p>
      <a class="btn btn-primary btn-lg btn-donate" href="donate.html"><span class="donate-heart" aria-hidden="true">♥</span>Donate Today</a>
    </div>
  </div>
</section>
""" + (RAFFLE_HOME_POPUP if SHOW_RAFFLE_POPUP else "")


# --- PRIZE PAGES (one template, eight pages) --------------------------------
# Per-page notes for the client, shown under the prize page hero.
PRIZE_NOTES = {}


# Entry-form label for each car photo, so "Enter to win" can open the form
# with that car already picked (nav.js reads ?prize=).
FORM_LABEL_BY_IMAGE = {image: label for label, image, _page in C.CAR_PRIZES}


def car_sheet(i, name, year, image, specs):
    """One car on a prize page: big photo, specs as tiles, enter button.
    Photo and text swap sides on every other car."""
    tiles = "\n".join(f"""          <div class="spec-tile"><dt>{k}</dt><dd>{v}</dd></div>""" for k, v in specs)
    year_html = f'<span class="car-sheet-year">{year}</span>' if year else ""
    form_label = FORM_LABEL_BY_IMAGE.get(image)
    pick = f"?prize={urllib.parse.quote(form_label)}" if form_label else ""
    flipped = " is-flipped" if i % 2 else ""
    return f"""    <article class="car-sheet{flipped}" id="car-{i + 1}">
      <div class="car-sheet-photo">
        <img src="assets/img/{image}" alt="{name}" loading="lazy">
        {year_html}
      </div>
      <div class="car-sheet-body">
        <h3>{name}</h3>
        <dl class="spec-grid">
{tiles}
        </dl>
        <p class="car-sheet-win">Win this car with</p>
        <div class="car-sheet-actions">
          {ticket(f"sweepstakes.html{pick}#enter", None, "Sweepstakes", f"From ${C.TICKET_TIERS[0][2]}", "ticket-navy ticket-compact")}
          {ticket(f"raffle-plus.html{pick}#enter", None, "Raffle Plus", f"From ${C.TICKET_TIERS[0][3]}", "ticket-yellow ticket-compact")}
        </div>
      </div>
    </article>"""


def prize_body(prize):
    # The live pages' small taglines ("Accept No Substitute.", "Ultimate
    # Thrill") are dropped: only some pages had one (CJ, 2026-10-18).
    slug, label, headline, sub, _tagline, _image, cars = prize
    sheets = "\n".join(car_sheet(i, *car) for i, car in enumerate(cars))
    names = [car[0] for car in cars]
    # Either ticket wins these cars, so the copy and buttons offer both.
    both_ways = ("Win it with a Sweepstakes ticket, or with Raffle Plus pair it with "
                 "a second car or $50,000.00.")
    if len(names) > 1:
        choice = ", ".join(names[:-1]) + " or " + names[-1]
        lead = f"Choose the {choice}. {both_ways}"
        specs_heading = f"{len(names)} {label} models to choose from"
    else:
        lead = f"The {names[0]}. {both_ways}"
        specs_heading = "Specs at a glance"  # the car's name is right below
    title = headline
    if headline.startswith("Win a "):
        title = f'Win a <span class="hl">{headline[len("Win a "):]}</span>'
    hero_gallery = gallery([(name, image, f"#car-{i + 1}") for i, (name, _y, image, _s) in enumerate(cars)],
                           count_label=f"{len(cars)} models" if len(cars) > 1 else None,
                           autoplay=4500 if len(cars) > 1 else None,
                           cls="prize-gallery sweeps-hero-gallery")
    hero = sweeps_hero(
        f'<a href="index.html">Home</a> &nbsp;/&nbsp; <a href="sweepstakes.html">Sweepstakes</a> &nbsp;/&nbsp; {label}',
        "Sweepstakes &amp; Raffle Plus",
        title,
        lead,
        0,
        f"${C.TICKET_TIERS[0][2]} or ${C.TICKET_TIERS[0][3]} Raffle Plus",
        gallery_html=hero_gallery,
        actions_html=(
            "        " + ticket("sweepstakes.html#enter", None, "Sweepstakes", None, "ticket-navy ticket-compact ticket-lg") + "\n"
            "        " + ticket("raffle-plus.html#enter", None, "Raffle Plus", None, "ticket-yellow ticket-compact ticket-lg")
        ),
    )
    return hero + f"""
<section class="section" id="specs">
  <div class="container">
    <div class="section-head">
      <div>
        <p class="eyebrow">The specs</p>
        <h2>{specs_heading}</h2>
      </div>
    </div>
{PRIZE_NOTES.get(slug, "")}
    <div class="car-sheets">
{sheets}
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <div class="text-center" style="margin-bottom:var(--space-5)">
      <p class="eyebrow">Tickets</p>
      <h2>Pick your tickets</h2>
    </div>
    <div class="tier-switch" data-tier-switch>
      <div class="tier-toggle" role="tablist" aria-label="Ticket type">
        <button type="button" role="tab" aria-selected="true" data-tier="sweepstakes">Sweepstakes<small>One car or $50,000</small></button>
        <button type="button" role="tab" aria-selected="false" data-tier="raffle-plus">Raffle Plus<small>Two cars or $100,000</small></button>
      </div>
      <div data-tier-panel="sweepstakes">
{ticket_tiers("sweepstakes")}
      </div>
      <div data-tier-panel="raffle-plus" hidden>
{ticket_tiers("raffle-plus")}
      </div>
    </div>
{PRIZE_PAGE_TICKET_PAIR if SHOW_PRIZE_PAGE_TICKET_PAIR else ""}
  </div>
</section>
"""


# --- HOW IT WORKS (new page, from the current Rules and FAQ) ---------------
HOW_IT_WORKS_BODY = page_hero(
    "How the Sweepstakes Works",
    "One drawing, one winner, and the winner chooses the prize. Here is how it works, start to finish.",
    "How It Works",
    parent=("Sweepstakes", "sweepstakes.html"),
) + f"""
<section class="section">
  <div class="container-narrow prose">
    <h2>1. Choose your ticket.</h2>
    <p><a href="sweepstakes.html">Sweepstakes</a> tickets are $25.00. The winner has a choice of either any one car, or $50,000.00 cash.</p>
    <p>With a <a href="raffle-plus.html">Raffle Plus</a> ticket the winner has their choice of any two cars, or one car and the cash prize.</p>

    <h2>2. Order online, by phone or by mail.</h2>
    <p>Tickets can be paid for by credit card, money order or check. Place an order online, call our order line at <a href="{tel(C.ORDER_LINE)}">{C.ORDER_LINE}</a>, or send a check to {", ".join(C.ADDRESS_LINES[1:])}.</p>
    <p>You can also buy a ticket as a gift: simply use the other person's name and contact information when completing your purchase.</p>

    <h2>3. Get your ticket numbers.</h2>
    <p>Your ticket numbers will be emailed or mailed to you within 48 hours of your purchase.</p>

    <h2>4. The drawing.</h2>
    <p>The winning ticket will be drawn on {C.DRAWING_DATE}. You do not need to be present to win. The winner will receive a phone call directly from us immediately following the drawing; if we cannot reach the winner by phone, we will email them.</p>

    <h2>5. Claiming the prize.</h2>
    <p>The winner must claim the prize within 30 days. Payment of all applicable federal, state and local taxes, fees and surcharges, tags and registration fees are the responsibility of the winner, who must provide proof of insurance to take delivery. If the cash prize is selected it will be paid in 3 installments, 60 days apart.</p>

    <h2>No purchase is necessary.</h2>
    <p>Please send a self-addressed stamped envelope to NHS, {", ".join(C.ADDRESS_LINES[1:])}.</p>

    <p><a class="btn btn-secondary" href="sweepstakes-rules.html">Read the full Sweepstakes Rules →</a></p>
  </div>
</section>
"""

# --- FAQ --------------------------------------------------------------------
# FAQ questions grouped by topic (indexes into C.FAQ, which keeps the live
# order). Every question appears exactly once.
FAQ_GROUPS = [
    ("Buying tickets", [0, 1, 2, 3, 9]),
    ("The drawing", [7, 5, 4]),
    ("The prizes", [6, 10]),
    ("Where your money goes", [8]),
    ("Still have questions?", [11]),
]
assert sorted(i for _t, idx in FAQ_GROUPS for i in idx) == list(range(len(C.FAQ)))


def faq_accordion():
    """Questions as cards that open to show the answer; the first one starts open."""
    groups, n = [], 0
    for topic, indexes in FAQ_GROUPS:
        items = []
        for i in indexes:
            q, a = C.FAQ[i]
            n += 1
            opened = " open" if n == 1 else ""
            items.append(f"""        <details class="faq-card"{opened}>
          <summary><span class="faq-num">{n:02d}</span><span class="faq-q">{q}</span><span class="faq-icon" aria-hidden="true"></span></summary>
          <div class="faq-a"><div class="faq-a-inner">{a}</div></div>
        </details>""")
        groups.append(f"""      <div class="faq-group">
        <p class="eyebrow">{topic}</p>
{chr(10).join(items)}
      </div>""")
    return "\n".join(groups)

# The review notes that sat here were answered by CJ on 2026-10-18: the
# drawing date and Suburban Dr address used everywhere are correct, the 18+
# rule is now in the Rules too, and the 1,000-participant limit still holds.
FAQ_BODY = page_hero(
    "Frequently Asked Questions",
    "Everything you need to know about entering the Sweepstakes and Raffle Plus.",
    "FAQ",
    parent=("Sweepstakes", "sweepstakes.html"),
) + f"""
<section class="section">
  <div class="container faq-layout">
    <div class="faq-list">
{faq_accordion()}
    </div>
    <aside class="faq-help">
      <h3>Still have questions?</h3>
      <p>We will gladly clear up any questions you may have.</p>
      <ul class="faq-contacts">
        <li><span>Customer Service</span><a href="{tel(C.CUSTOMER_SERVICE)}">{C.CUSTOMER_SERVICE}</a></li>
        <li><span>Order Line</span><a href="{tel(C.ORDER_LINE)}">{C.ORDER_LINE}</a></li>
        <li><span>Email</span><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></li>
      </ul>
      <div class="faq-help-actions">
      {ticket("sweepstakes.html#enter", None, "Sweepstakes", None, "ticket-navy ticket-compact")}
      {ticket("raffle-plus.html#enter", None, "Raffle Plus", None, "ticket-yellow ticket-compact")}
      </div>
      <p class="faq-help-more"><a href="sweepstakes-rules.html">Read the full rules →</a></p>
    </aside>
  </div>
</section>
""" + winners_strip()

# --- RULES ------------------------------------------------------------------
RULES_ITEMS = "\n".join(f"""      <li class="rule-card"><span class="rule-num" aria-hidden="true">{i:02d}</span><p>{r}</p></li>"""
                        for i, r in enumerate(C.RULES, 1))

# Title and lead from CJ (2026-10-19); the rules themselves stay verbatim
# and in their published order.
RULES_BODY = page_hero(
    "Sweepstakes &amp; Raffle Rules",
    "Rules and regulations of the National Humane Society Sweepstakes and Raffle.",
    "Rules",
    parent=("Sweepstakes", "sweepstakes.html"),
) + f"""
<section class="section section-soft">
  <div class="container faq-layout">
    <ol class="rules-list">
{RULES_ITEMS}
    </ol>
    <aside class="faq-help rules-glance">
      <h3>At a glance</h3>
      <ul class="faq-contacts">
        <li><span>Next drawing</span><strong>{C.DRAWING_DATE}</strong></li>
        <li><span>Tickets</span><strong>From ${C.TICKET_TIERS[0][2]} · Raffle Plus from ${C.TICKET_TIERS[0][3]}</strong></li>
        <li><span>To enter</span><strong>18 or older</strong></li>
        <li><span>To win</span><strong>No need to be present</strong></li>
      </ul>
      <p>Questions about the rules? Call Customer Service at <a href="{tel(C.CUSTOMER_SERVICE)}">{C.CUSTOMER_SERVICE}</a>.</p>
      <div class="faq-help-actions">
      {ticket("sweepstakes.html#enter", None, "Sweepstakes", None, "ticket-navy ticket-compact")}
      {ticket("raffle-plus.html#enter", None, "Raffle Plus", None, "ticket-yellow ticket-compact")}
      </div>
      <p class="faq-help-more"><a href="faq.html">Read the FAQ →</a></p>
    </aside>
  </div>
</section>
""" + winners_strip()

# --- PREVIOUS WINNERS -------------------------------------------------------
WINNERS_BODY = page_hero(
    "Previous Winners",
    "Congratulations to the past winners of our Sweepstakes and Raffle Plus drawings.",
    "Previous Winners",
    parent=("Sweepstakes", "sweepstakes.html"),
) + f"""
<section class="section section-soft">
  <div class="container">
    <p class="eyebrow winners-count">{len(C.WINNERS)} winners and counting</p>
{winners_wall()}
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="text-center" style="max-width:640px; margin:0 auto var(--space-6)">
      <p class="eyebrow">Next drawing · {C.DRAWING_DATE}</p>
      <h2>Could you be next?</h2>
    </div>
{SWEEPS_CTA}
  </div>
</section>
"""

# --- DONATE -----------------------------------------------------------------
_DS = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
       'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">')
DONATE_ICONS = {k: _DS + v + "</svg>" for k, v in {
    "receipt": '<path d="M6 2.5h12v19l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6l8-3z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "copy": '<rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/>',
    "lock": '<rect x="4.5" y="10.5" width="15" height="10.5" rx="2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6l8.5 7 8.5-7"/>',
    "doc": '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6"/><path d="M8 13h8M8 17h5"/>',
    "ticket": '<path d="M3 8a2 2 0 0 0 2-2h14a2 2 0 0 0 2 2v2a2 2 0 0 0 0 4v2a2 2 0 0 0-2 2H5a2 2 0 0 0-2-2v-2a2 2 0 0 0 0-4z"/><path d="M14 6v12" stroke-dasharray="2 2.5"/>',
}.items()}
DONATE_FACTS = [("receipt", "Tax-deductible"), ("shield", "501(c)(3) nonprofit"), ("clock", "Over 25 years")]
DONATE_FACT_CHIPS = "\n".join(
    f'        <li><span aria-hidden="true">{DONATE_ICONS[icon]}</span>{label}</li>' for icon, label in DONATE_FACTS)
DONATE_MAIL_TO = ", ".join(C.ADDRESS_LINES)


def donate_step(n, title):
    return f'        <div class="donate-step"><span class="step-num donate-step-num" aria-hidden="true">{n}</span><h3>{title}</h3></div>'


DONATE_BODY = page_hero(
    "Donate Now",
    "Every dollar can make a difference for an animal in need.",
    "Donate",
) + f"""
<section class="section">
  <div class="container donate-layout">
    <div class="donate-intro">
      <figure class="donate-photo">
        <img src="assets/img/donate-hero.jpeg" alt="A dog looking out from a dark kennel doorway" loading="lazy">
      </figure>
      <p class="eyebrow">Why give</p>
      <h2>Help end animal abuse and neglect</h2>
      <p class="donate-lead">For over 25 years, the National Humane Society has worked tirelessly to put an end to animal abuse and neglect. We are one of the national leaders in the areas of rescue, adoption and welfare, and your tax-deductible donation will help fight cruelty and make a life-changing difference for animals across America.</p>
      <ul class="donate-facts">
{DONATE_FACT_CHIPS}
      </ul>
      <blockquote class="donate-thanks">
        <span class="donate-thanks-paw" aria-hidden="true">{PAW_ICON}</span>
        <p>Thank you for making the National Humane Society and the animals we serve a part of your life.</p>
      </blockquote>
    </div>
    <form class="donate-widget donate-form" data-donate onsubmit="event.preventDefault(); alert('Preview only — donations are not submitted.');">
{donate_step(1, "Choose your donation")}
{DONATE_TOGGLE}
      <div class="amount-grid">
{donate_amount_buttons()}
      </div>
      <div class="form-grid">
        <div class="form-row"><label>Other amount</label><input type="text" inputmode="decimal" placeholder="$ Other Amount"></div>
      </div>
{donate_step(2, "Your details")}
      <div class="form-grid">
{PERSON_FIELDS}
      </div>
{donate_step(3, "Payment")}
      <div class="form-grid">
        <div class="donate-secure">
          <span class="donate-secure-icon" aria-hidden="true">{DONATE_ICONS["lock"]}</span>
{PAYMENT_BLOCK}
        </div>
        <button type="submit" class="btn btn-primary btn-lg btn-donate donate-cta donate-submit"><span class="donate-heart" aria-hidden="true">♥</span><span class="donate-cta-label">Donate $25 monthly</span></button>
        <p class="form-footnote">Tax-deductible · 501(c)(3). Please remember to spay or neuter your pets. For any questions, please call us at <a href="{tel(C.CUSTOMER_SERVICE)}">{C.CUSTOMER_SERVICE}</a>.</p>
      </div>
    </form>
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <div class="text-center" style="max-width:760px; margin:0 auto var(--space-6)">
      <p class="eyebrow">More ways to help</p>
      <h2>Other ways to give</h2>
    </div>
    <div class="give-ways">
      <article class="give-way is-coral">
        <span class="give-way-icon" aria-hidden="true">{DONATE_ICONS["mail"]}</span>
        <h3>By mail</h3>
        <p>Send a personal check or money order made payable to the National Humane Society to:</p>
        <address class="give-way-address">{"<br>".join(C.ADDRESS_LINES[1:])}</address>
        <div class="give-way-actions"><button type="button" class="bequest-copy contact-copy" data-copy="{DONATE_MAIL_TO}" aria-label="Copy mailing address"><span aria-hidden="true">{DONATE_ICONS["copy"]}</span><span class="bequest-copy-label">Copy address</span></button></div>
      </article>
      <article class="give-way is-teal">
        <span class="give-way-icon" aria-hidden="true">{DONATE_ICONS["doc"]}</span>
        <h3>Wills &amp; estates</h3>
        <p>Assigning the National Humane Society in your will or trust is a helpful way for our organization to continue serving animals in need.</p>
        <div class="give-way-actions"><a class="give-way-link" href="wills-estates.html">Learn more <span class="give-way-arrow" aria-hidden="true">→</span></a></div>
      </article>
      <article class="give-way is-orange">
        <span class="give-way-icon" aria-hidden="true">{DONATE_ICONS["ticket"]}</span>
        <h3>Sweepstakes &amp; Raffle Plus</h3>
        <p>What is better than helping animals in need while winning some incredible prizes?</p>
        <div class="give-way-actions give-way-tickets">
        {ticket("sweepstakes.html#enter", None, "Sweepstakes", None, "ticket-navy ticket-compact")}
        {ticket("raffle-plus.html#enter", None, "Raffle Plus", None, "ticket-yellow ticket-compact")}
        </div>
      </article>
    </div>
  </div>
</section>
"""

# --- EDUCATIONAL MESSAGES (blog index) --------------------------------------
BLOG_BODY = page_hero(
    "Educational Messages",
    "Videos and articles on adoption, pet care, shelters, animal welfare, and more.",
    "Educational Messages",
) + edu_video_carousel() + f"""
<section class="section section-soft articles-section" id="articles" data-post-filter data-page-size="12">
  <div class="container">
    <div class="section-head">
      <div>
        <p class="eyebrow">Articles</p>
        <h2>Browse by topic</h2>
      </div>
    </div>
{blog_filter_bar()}
    {review_note("<p>All 81 articles from the current site are listed. Only <em>How Your $10 Monthly Donation Really Helps Shelter Animals</em> opens inside the preview, as the article template; the others open the current site until the posts are migrated in the WordPress build.</p>")}
{blog_cards(C.BLOG_POSTS, filterable=True)}
    <div class="text-center" style="margin-top:var(--space-6)">
      <button type="button" class="btn btn-secondary" data-show-more>Show more articles</button>
    </div>
  </div>
</section>
"""

_SAMPLE_CATEGORY = next(cat for _t, slug, cat in C.BLOG_POSTS if slug == C.BLOG_SAMPLE_SLUG)
RELATED_POSTS = [p for p in C.BLOG_POSTS if p[2] == _SAMPLE_CATEGORY and p[1] != C.BLOG_SAMPLE_SLUG][:3]

# --- BLOG POST (article template, using a real post) -----------------------
# The sample article, laid out with the styles every migrated post will get:
# a header in its category's colour, a larger opening paragraph, a "by the
# numbers" strip and pull quote (both taken from the article's own text), and
# the bold-led paragraphs as breakdown cards. The wording is unchanged.
BLOG_POST_BODY = f"""
<section class="article-hero post-cover is-{BLOG_COLOUR[_SAMPLE_CATEGORY]}">
  <div class="container-narrow">
    <div class="breadcrumb"><a href="index.html">Home</a> &nbsp;/&nbsp; <a href="blog.html">Educational Messages</a></div>
    <span class="article-chip">{html.escape(_SAMPLE_CATEGORY)}</span>
    <h1>How Your $10 Monthly Donation Really Helps Shelter Animals</h1>
    <p class="article-meta">National Humane Society &nbsp;·&nbsp; Educational Message</p>
  </div>
</section>

<section class="section article-section">
  <div class="container-narrow prose article">
    {review_note("<p>This article is copied from the current site as far as the first section, to show the article layout. Further down, the published post promises annual impact reports, personalized updates for monthly donors and the option to designate a gift to a specific fund — none of which the current site offers. Worth confirming before it is carried over.</p>")}
    <p class="article-lead">In 2025, an estimated 5.8 million dogs and cats entered U.S. shelters and rescues—a 2% decrease from the previous year, according to Shelter Animals Count's 2025 Annual Data Report. While that's encouraging progress, the numbers remain staggering: about 4.2 million animals were adopted (a modest 0.7% increase), but roughly 597,000 were euthanized, and 757,000 experienced non-live outcomes overall (a slight 1% decline). The national save rate holds steady at around 82%, with two out of three shelters achieving no-kill status (90%+ live release rate). These figures represent real animals facing uncertainty due to overcrowding, medical emergencies, economic surrenders, and limited shelter resources.</p>

    <div class="article-stats" aria-label="2025 shelter figures from the article">
      <div><strong>5.8M</strong><span>dogs and cats entered U.S. shelters</span></div>
      <div><strong>4.2M</strong><span>animals adopted</span></div>
      <div><strong>82%</strong><span>national save rate</span></div>
    </div>
    <p class="article-source">Source: Shelter Animals Count, 2025 Annual Data Report</p>

    <p>At the National Humane Society, we exist to change that trajectory. We raise donations to directly support animals in crisis—providing food, medical care, transport, and foster resources—while also assisting partner shelters nationwide with funding for supplies, low-cost clinics, emergency responses, and capacity-building programs. In an era of rising veterinary costs and ongoing intake pressures, consistent support makes the biggest difference.</p>

    <blockquote class="article-quote">Less than the cost of a streaming subscription or a couple of coffees, this amount delivers reliable funding that shelters can count on month after month.</blockquote>

    <p>That's why a small, recurring gift—like $10 per month—packs such powerful impact. Less than the cost of a streaming subscription or a couple of coffees, this amount delivers reliable funding that shelters can count on month after month. Below, we break it down transparently: where the money goes, real stories of animals helped, why monthly giving outperforms one-time donations in tough times, and how you can get involved.</p>

    <h2>Where Exactly Does Your $10 Monthly Donation Go? A Detailed Breakdown</h2>
    <p>Shelters face a wide range of expenses, from daily basics to life-saving interventions. The National Humane Society stretches every dollar through bulk purchasing, volunteer coordination, and partnerships with local rescues. Here's how a modest $10 monthly gift contributes in practical terms (based on national averages and our program data):</p>
    <div class="article-points">
      <div class="article-point">
        <span class="article-point-num" aria-hidden="true">01</span>
        <div>
          <h3>Nutrition and Daily Care</h3>
          <p>A medium-sized dog requires about 2–3 cups of quality dry food per day, costing roughly $10–$20 per week (depending on brand and portion). Your $10 covers a full week's worth of nutritious food for one medium dog or several cats/kittens. This prevents malnutrition, supports immune health during stressful shelter stays, and keeps animals adoptable longer.</p>
        </div>
      </div>
      <div class="article-point">
        <span class="article-point-num" aria-hidden="true">02</span>
        <div>
          <h3>Preventive Veterinary Care</h3>
          <p>Core vaccines, deworming, flea/tick prevention, and initial exams are essential to stop outbreaks and prepare animals for adoption. These basics cost $50–$150 per animal. Your recurring gift contributes toward preventive packages, reducing the risk of illness spreading in crowded facilities and lowering long-term medical burdens.</p>
        </div>
      </div>
    </div>

    <p class="article-continue"><a class="btn btn-secondary" href="{C.LIVE_SITE}/post/{C.BLOG_SAMPLE_SLUG}" target="_blank" rel="noopener">Continue reading on the current site →</a></p>

    <aside class="article-cta">
      <div>
        <p class="eyebrow">Monthly giving</p>
        <h3>Ready to make a reliable difference?</h3>
        <p>Your $10 monthly gift is a commitment to consistent hope for animals and shelters nationwide.</p>
      </div>
      <a class="btn btn-primary btn-lg btn-donate" href="donate.html"><span class="donate-heart" aria-hidden="true">♥</span>Donate today</a>
    </aside>
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <div class="section-head">
      <div>
        <p class="eyebrow">Keep reading</p>
        <h2>More on {html.escape(_SAMPLE_CATEGORY)}</h2>
      </div>
      <a class="btn btn-secondary" href="blog.html#articles">All articles →</a>
    </div>
{blog_cards(RELATED_POSTS)}
  </div>
</section>
"""

# --- VIDEOS & MORE ----------------------------------------------------------
# The Instagram glyph (simple outline version), used on the follow buttons
INSTAGRAM_ICON = (
    '<svg class="ig-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<rect x="2.5" y="2.5" width="19" height="19" rx="5.5" fill="none" stroke="currentColor" stroke-width="2"/>'
    '<circle cx="12" cy="12" r="4.3" fill="none" stroke="currentColor" stroke-width="2"/>'
    '<circle cx="17.4" cy="6.6" r="1.3" fill="currentColor"/></svg>'
)


def instagram_button(label=None, cls=""):
    """Follow button in Instagram's gradient with the Instagram glyph."""
    label = label or f"Follow @{C.INSTAGRAM_HANDLE}"
    return (f'<a class="btn btn-instagram {cls}" href="{C.SOCIAL[0][1]}" target="_blank" rel="noopener">'
            f'{INSTAGRAM_ICON}<span>{label}</span></a>')


def more_wall():
    """The "And More" wall: photos and vertical Vimeo videos in a masonry
    layout (CSS columns), in the live page's order."""
    items = []
    n_photo = n_video = 0
    for kind, value in C.VIDEOS_AND_MORE:
        if kind == "photo":
            n_photo += 1
            items.append(f"""      <figure class="more-item more-photo"><img src="assets/img/{value}" alt="National Humane Society on Instagram, photo {n_photo}" loading="lazy" decoding="async"></figure>""")
        else:
            n_video += 1
            items.append(f"""      <figure class="more-item more-video"><div class="more-video-frame" data-embed>{embed_loader(fallback=(f"https://vimeo.com/{value}", "Taking a while? Watch on Vimeo →"))}<iframe src="https://player.vimeo.com/video/{value}?title=0&amp;byline=0&amp;portrait=0" title="National Humane Society video {n_video}" loading="lazy" allow="fullscreen; picture-in-picture" allowfullscreen></iframe></div></figure>""")
    return '    <div class="more-wall">\n' + "\n".join(items) + "\n    </div>"


# "Our Instagram": a snapshot from fetch_instagram.py when there is one
# (instagram_feed.json), otherwise six placeholder tiles.
def instagram_feed():
    path = OUT_DIR / "instagram_feed.json"
    posts = json.loads(path.read_text(encoding="utf-8"))["posts"] if path.exists() else []
    if not posts:
        tiles = "\n".join(f'      <div class="ig-tile" aria-hidden="true">{INSTAGRAM_ICON}</div>' for _ in range(6))
        note = review_note("<p>The current site fills this section with the 12 latest Instagram posts. It does that from the browser using an access token written into the page, which anyone can copy, so the prototype does not reproduce it. In the WordPress build the posts are fetched on the server, with the token kept private; the tiles below only hold their place. To see real posts here, run <code>fetch_instagram.py</code> with a token (instructions at the top of that file).</p>")
        return note, f'    <div class="ig-grid">\n{tiles}\n    </div>'
    tiles = []
    for p in posts:
        caption = html.escape(" ".join(p["caption"].split())[:110] + ("…" if len(p["caption"]) > 110 else ""))
        badge = '<span class="ig-badge">▶ Video</span>' if p["media_type"] == "VIDEO" else ""
        tiles.append(f"""      <a class="ig-post" href="{html.escape(p['permalink'])}" target="_blank" rel="noopener" data-ig="{p['kind']}/{p['shortcode']}">
        {embed_loader("Loading…")}
        <img src="{p['image']}" alt="Instagram post: {caption}" loading="lazy" decoding="async">
        {badge}
        <span class="ig-caption">{caption}</span>
      </a>""")
    note = review_note("<p>A snapshot of the latest posts, taken with <code>fetch_instagram.py</code>, which does what the WordPress site will do on its server. Click a post to play it here.</p>")
    return note, '    <div class="ig-grid ig-grid-posts">\n' + "\n".join(tiles) + "\n    </div>"


IG_FEED_NOTE, IG_FEED_GRID = instagram_feed()

VIDEOS_BODY = page_hero(
    "Videos and More",
    "Videos, photos and stories from our work, our shelter partners and our Instagram.",
    "Videos &amp; More",
) + f"""
<section class="section featured-post">
  <div class="container featured-post-grid">
    <div>
      <p class="eyebrow">Featured post</p>
      <h2>Featured on Instagram</h2>
      <p class="lead">Our latest featured Instagram collaboration. Follow along for rescue stories, sweepstakes news and animal welfare updates.</p>
    </div>
    <div class="featured-post-embed" data-embed data-embed-instagram>
      {embed_loader("Loading post…", (C.INSTAGRAM_FEATURED, "Taking a while? View it on Instagram →"))}
      <blockquote class="instagram-media" data-instgrm-permalink="{C.INSTAGRAM_FEATURED}" data-instgrm-version="14">
        <a href="{C.INSTAGRAM_FEATURED}" target="_blank" rel="noopener">{INSTAGRAM_ICON}<span>View this post on Instagram</span></a>
      </blockquote>
    </div>
  </div>
</section>

<section class="section section-soft ig-feed-section">
  <div class="container">
    <div class="ig-profile">
      <a class="ig-avatar" href="{C.SOCIAL[0][1]}" target="_blank" rel="noopener"><img src="assets/img/ig-profile.jpg" alt="@{C.INSTAGRAM_HANDLE} on Instagram" width="100" height="100"></a>
      <div>
        <p class="eyebrow">Our Instagram</p>
        <h2>@{C.INSTAGRAM_HANDLE}</h2>
      </div>
      {instagram_button("Follow on Instagram", "ig-profile-btn")}
    </div>
    {IG_FEED_NOTE}
{IG_FEED_GRID}
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head">
      <div>
        <p class="eyebrow">And more</p>
        <h2>Photos and videos</h2>
      </div>
    </div>
    {review_note("<p>The current page shows these photos and videos with no titles or captions; a short caption for each would help visitors and search engines.</p>")}
{more_wall()}
    <div class="text-center" style="margin-top:var(--space-7)">
      {instagram_button("See more on Instagram")}
    </div>
  </div>
</section>
"""

# --- ANIMAL INFO: PET TIPS --------------------------------------------------
# Pet Tips: the full article, laid out as sections (photo intro, three ways,
# numbered actions, Q&A cards, closing panel). Copy lives in content.py.
PET_TIPS_WAY_ICONS = {"Time": "⏱", "Space": "⌂", "Money": "♥"}


BOOK_ICON = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v17H6.5A2.5 2.5 0 0 0 4 21.5z"/><path d="M4 21.5A2.5 2.5 0 0 1 6.5 19H20v3H6.5"/><path d="M8 7h8M8 11h6"/></svg>'
)


def source_domain(url):
    return url.split("//", 1)[-1].split("/", 1)[0].removeprefix("www.")


def with_refs(text, sources=None):
    """Turn the article's link texts into reference links: the words keep a
    coral underline and a small arrow, with a numbered marker that matches the
    Sources list at the end of the page. `sources` defaults to Pet Tips'."""
    for n, (phrase, url) in enumerate(sources or C.PET_TIPS_SOURCES, 1):
        if phrase in text:
            # The last word and the marker stay together, so the number never
            # wraps onto a line by itself
            head, _, last = phrase.rpartition(" ")
            head = head + " " if head else ""
            text = text.replace(phrase, (
                f'<a class="ref-link" href="{url}" target="_blank" rel="noopener" '
                f'title="{source_domain(url)}">{head}<span class="ref-tail">{last}'
                f'<span class="ref-mark" aria-hidden="true">{n}</span></span></a>'), 1)
    return text


def pet_tips_sources(sources=None):
    cards = "\n".join(
        f"""      <a class="source-card" href="{url}" target="_blank" rel="noopener">
        <span class="source-num">{n}</span>
        <span class="source-text"><strong>“{phrase}”</strong><small><span class="source-globe" aria-hidden="true">{GLOBE_ICON}</span>{source_domain(url)}</small></span>
        <span class="source-arrow" aria-hidden="true">↗</span>
      </a>""" for n, (phrase, url) in enumerate(sources or C.PET_TIPS_SOURCES, 1))
    return f'    <div class="source-grid">\n{cards}\n    </div>'


def pet_tips_faq():
    items = []
    for n, (q, a) in enumerate(C.PET_TIPS_FAQ, 1):
        opened = " open" if n == 1 else ""
        items.append(f"""        <details class="faq-card"{opened}>
          <summary><span class="faq-num">{n:02d}</span><span class="faq-q">{q}</span><span class="faq-icon" aria-hidden="true"></span></summary>
          <div class="faq-a"><div class="faq-a-inner"><p>{with_refs(a)}</p></div></div>
        </details>""")
    return "\n".join(items)


PET_TIPS_WAY_CARDS = "\n".join(
    f'      <div class="way-card"><span class="way-icon" aria-hidden="true">{PET_TIPS_WAY_ICONS[w]}</span><h3>{w}</h3><p>{t}</p></div>'
    for w, t in C.PET_TIPS_THREE_WAYS)
PET_TIPS_ACTION_CARDS = "\n".join(
    f'      <article class="action-card"><span class="action-num" aria-hidden="true">{n}</span><h3>{t}</h3><p>{with_refs(d)}</p></article>'
    for n, (t, d) in enumerate(C.PET_TIPS_ACTIONS, 1))


PET_TIPS_BODY = page_hero(
    "Pet Tips",
    "Simple, practical ways anyone can help shelter pets, whatever your schedule, space or budget.",
    "Pet Tips",
) + f"""
<section class="section">
  <div class="container tips-intro">
    <div>
      <p class="eyebrow">Getting started</p>
      <h2>{C.PET_TIPS_INTRO_TITLE}</h2>
      <p class="tips-lead">{C.PET_TIPS_INTRO}</p>
    </div>
    <div class="tips-photo">
      <img src="assets/img/animal-winterpup.jpg" alt="A dog wearing a fuzzy bear-ears hood" width="570" height="618">
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <div class="text-center" style="max-width:760px; margin:0 auto var(--space-6)">
      <p class="eyebrow">Find your lane</p>
      <h2>{C.PET_TIPS_THREE_WAYS_TITLE}</h2>
    </div>
    <div class="ways-grid">
{PET_TIPS_WAY_CARDS}
    </div>
    <div class="container-narrow tips-prose" style="padding:0; margin-top:var(--space-7)">
{paragraphs([with_refs(p) for p in C.PET_TIPS_THREE_WAYS_TEXT])}
    </div>
  </div>
</section>

<section class="section">
  <div class="container-narrow tips-prose">
    <p class="eyebrow">Going further</p>
    <h2>{C.PET_TIPS_NONPROFIT_TITLE}</h2>
{paragraphs([with_refs(p) for p in C.PET_TIPS_NONPROFIT])}
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <div class="text-center" style="max-width:760px; margin:0 auto var(--space-6)">
      <p class="eyebrow">Your menu</p>
      <h2>{C.PET_TIPS_ACTIONS_TITLE}</h2>
      <p class="lead" style="margin:0 auto">{C.PET_TIPS_ACTIONS_INTRO}</p>
    </div>
    <div class="action-grid">
{PET_TIPS_ACTION_CARDS}
    </div>
  </div>
</section>

<section class="section">
  <div class="container-narrow">
    <div class="text-center" style="margin-bottom:var(--space-6)">
      <p class="eyebrow">Q&amp;A</p>
      <h2>{C.PET_TIPS_FAQ_TITLE}</h2>
    </div>
    <div class="faq-group">
{pet_tips_faq()}
    </div>
  </div>
</section>

<section class="section section-cream tips-closing">
  <div class="container">
    <div class="tips-closing-card">
      <p class="eyebrow">Keep it going</p>
      <h2>{C.PET_TIPS_CLOSING_TITLE}</h2>
      <p class="tips-closing-text">{C.PET_TIPS_CLOSING}</p>
      <a class="btn btn-primary btn-lg btn-donate" href="donate.html"><span class="donate-heart" aria-hidden="true">♥</span>Give monthly</a>
    </div>
    <aside class="tips-sources" aria-labelledby="tips-sources-title">
      <div class="tips-sources-head">
        <span class="tips-sources-icon" aria-hidden="true">{BOOK_ICON}</span>
        <div>
          <h3 id="tips-sources-title">Sources mentioned in this article</h3>
          <p>Outside websites referenced in the text. Each opens in a new tab.</p>
        </div>
      </div>
{pet_tips_sources()}
    </aside>
  </div>
</section>
"""

# --- ANIMAL INFO: CATS & DOGS -----------------------------------------------
def article_cards(exclude=None):
    """Cats & Dogs article cards. Scanned articles open in the page viewer
    (nav.js, [data-doc]); without JavaScript the link opens the first page.
    `exclude` drops the card that links to that page."""
    cards = []
    for title, topic, colour, pages, href in C.CATS_DOGS_ARTICLES:
        if exclude and href == exclude:
            continue
        safe = html.escape(title)
        if pages:
            count = f"{len(pages)} page{'s' if len(pages) > 1 else ''}"
            pages_attr = html.escape(json.dumps([f"assets/img/{p}" for p in pages]))
            link = (f'<a class="doc-card-link" href="assets/img/{pages[0]}" data-doc="{pages_attr}" data-doc-title="{safe}">'
                    f'Read article <span aria-hidden="true">→</span></a>')
            badge = f'<span class="doc-badge">{count}</span>'
        else:
            link = f'<a class="doc-card-link" href="{href}">Read article <span aria-hidden="true">→</span></a>'
            badge = '<span class="doc-badge">Full page</span>'
        cards.append(f"""      <article class="doc-card">
        <div class="post-cover is-{colour}" aria-hidden="true">
          <span class="post-cover-topic">{topic}</span>
          {badge}
        </div>
        <div class="doc-card-body">
          <h3>{safe}</h3>
          {link}
        </div>
      </article>""")
    return "\n".join(cards)


CATS_DOGS_BODY = page_hero(
    "Information on Cats &amp; Dogs",
    "A little know-how goes a long way toward a happy, healthy pet, and a safe one when the unexpected happens.",
    "Cats &amp; Dogs",
) + f"""
<section class="section">
  <div class="container tips-intro">
    <div>
      <p class="eyebrow">Pet care reading</p>
      <h2>Helpful articles for cat and dog owners</h2>
      <p class="tips-lead">{C.CATS_DOGS_INTRO}</p>
    </div>
    <div class="tips-photo">
      <img src="assets/img/catsdogs-photo.jpg" alt="A woman playing with a beagle on a sunny path" width="570" height="618">
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <div class="section-head">
      <div>
        <p class="eyebrow">Articles</p>
        <h2>{len(C.CATS_DOGS_ARTICLES)} articles to read</h2>
      </div>
    </div>
    {review_note("<p>On the current site, four of these titles open pop-ups of <strong>scanned article pages</strong> rather than real text, and the scans credit other websites as their source (e.g. vetdepot.com). They are carried over the same way here. As images they can't be searched, resized or read by screen readers, so for the WordPress site we'd suggest re-typing them as real articles, and confirming NHS has permission to republish them.</p>")}
    <div class="doc-grid">
{article_cards()}
    </div>
  </div>
</section>
"""

# --- ANIMAL INFO: FOODS TO AVOID --------------------------------------------
PHONE_ICON = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'
)
FOOD_COLOURS = ["coral", "teal", "orange", "blue"]


def food_slug(name):
    return "food-" + "".join(ch if ch.isalnum() else "-" for ch in name.lower().replace("&amp;", "and")).strip("-").replace("--", "-").replace("--", "-")


FOODS_INTRO_HTML = C.FOODS_INTRO.replace(
    C.FOODS_POISON_PHONE, f'<a class="poison-num" href="tel:{C.FOODS_POISON_PHONE}">{C.FOODS_POISON_PHONE}</a>')
FOODS_JUMP = "\n".join(
    f'      <a class="foods-chip" href="#{food_slug(name)}">{name}</a>' for name, _ in C.FOODS_TO_AVOID)
FOODS_ITEMS = "\n".join(
    f"""      <article class="food-card is-{FOOD_COLOURS[i % 4]}" id="{food_slug(name)}">
        <span class="food-num" aria-hidden="true">{i + 1:02d}</span>
        <h3>{name}</h3>
        <p>{text}</p>
      </article>""" for i, (name, text) in enumerate(C.FOODS_TO_AVOID))

FOODS_BODY = page_hero(
    "ASPCA List of People Foods to Avoid Feeding Your Pets",
    "Some everyday foods that are safe for people can make cats and dogs seriously ill. Here’s what to keep out of reach, and why.",
    "Foods to Avoid",
    parent=("Cats &amp; Dogs", "cats-and-dogs.html"),
) + f"""
<section class="section">
  <div class="container">
    <div class="poison-card">
      <span class="poison-icon" aria-hidden="true">{PHONE_ICON}</span>
      <div class="poison-text">
        <p class="eyebrow">Think your pet ate something harmful?</p>
        <h2>Act fast and call for help</h2>
        <p>{FOODS_INTRO_HTML}</p>
      </div>
      <a class="btn btn-primary btn-lg poison-call" href="tel:{C.FOODS_POISON_PHONE}"><span aria-hidden="true">{PHONE_ICON}</span>Call {C.FOODS_POISON_PHONE}</a>
    </div>
    <nav class="foods-jump" aria-labelledby="foods-jump-title">
      <h2 class="foods-jump-title" id="foods-jump-title">Browse by food</h2>
      <div class="foods-chips">
{FOODS_JUMP}
      </div>
    </nav>
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <div class="text-center" style="max-width:760px; margin:0 auto var(--space-6)">
      <p class="eyebrow">The list</p>
      <h2>{len(C.FOODS_TO_AVOID)} people foods that can harm pets</h2>
    </div>
    <div class="foods-grid">
{FOODS_ITEMS}
    </div>
    <aside class="tips-sources foods-sources" aria-labelledby="foods-sources-title">
      <div class="tips-sources-head">
        <span class="tips-sources-icon" aria-hidden="true">{BOOK_ICON}</span>
        <div>
          <h3 id="foods-sources-title">Source for this list</h3>
          <p>The list above comes from the ASPCA. The link opens in a new tab.</p>
        </div>
      </div>
      <a class="source-card" href="{C.FOODS_SOURCE[1]}" target="_blank" rel="noopener">
        <span class="source-num">1</span>
        <span class="source-text"><strong>“{C.FOODS_SOURCE[0]}”</strong><small><span class="source-globe" aria-hidden="true">{GLOBE_ICON}</span>{source_domain(C.FOODS_SOURCE[1])}</small></span>
        <span class="source-arrow" aria-hidden="true">↗</span>
      </a>
    </aside>
  </div>
</section>

<section class="section section-cream">
  <div class="container">
    <div class="section-head">
      <div>
        <p class="eyebrow">Keep reading</p>
        <h2>More articles for cat and dog owners</h2>
      </div>
      <a class="btn btn-secondary" href="cats-and-dogs.html">All Cats &amp; Dogs articles</a>
    </div>
    <div class="doc-grid is-four">
{article_cards(exclude='foods-to-avoid.html')}
    </div>
  </div>
</section>
"""

# --- ANIMAL INFO: HURRICANES ------------------------------------------------
# Kit cards: (cover label, cover colour) for each HURRICANE_KIT group. The
# text in brackets in the group name becomes a note under the cover.
KIT_COVERS = {
    "Cats and Dogs": ("Cats &amp; dogs", "coral"),
    "Snake": ("Snakes", "teal"),
    "Small mammals (in small carriers)": ("Small mammals", "orange"),
    "Birds (in carrier with perch inside)": ("Birds", "blue"),
}
HU_X_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" aria-hidden="true">'
             '<path d="M6 6l12 12M18 6L6 18"/></svg>')
HU_CHECK_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                 '<path d="M5 12.5l4.5 4.5L19 7"/></svg>')
MUST_HAVE_ICONS = {
    "Pet Travel Carrier": '<rect x="2.5" y="7" width="19" height="13.5" rx="2"/><path d="M16 20.5V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v15.5"/>',
    "Proper Identification": '<path d="M20.6 13.4l-7.2 7.2a2 2 0 0 1-2.8 0L2 12V2h10l8.6 8.6a2 2 0 0 1 0 2.8z"/><circle cx="7" cy="7" r="1.6"/>',
    "Health Records &amp; Medication": '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M9 12h6M9 16h4"/>',
}
MUST_COLOURS = ["coral", "teal", "orange"]
HU_PLAN = [
    ("hu-kit", "Pack an evacuation kit", "What each kind of pet needs"),
    ("hu-dos", "Know the dos and don'ts", "Decisions to make before an order"),
    ("hu-must", "Get the must-haves", "Carrier, ID and health records"),
    ("hu-after", "Help them settle back in", "After the storm passes"),
]


def kit_card(name, items, main=False):
    label, colour = KIT_COVERS[name]
    note = name.split("(", 1)[1].rstrip(")") if "(" in name else ""
    note_html = f'\n          <span class="kit-cover-note">{note[0].upper() + note[1:]}</span>' if note else ""
    key = name.split("(")[0].strip().lower().replace(" ", "-")
    rows = "\n".join(
        f'            <li><label class="kit-item"><input type="checkbox"><span>{item}</span></label></li>'
        for item in items)
    return f"""      <article class="kit-card is-{colour}{' is-main' if main else ''}" data-kit="{key}">
        <div class="post-cover is-{colour}">
          <span class="post-cover-topic">{label}</span>{note_html}
          <span class="doc-badge kit-count" aria-live="polite">{len(items)} items</span>
        </div>
        <div class="kit-card-body">
          <ul class="kit-list">
{rows}
          </ul>
        </div>
      </article>"""


HU_PLAN_STEPS = "\n".join(
    f'          <li><a href="#{anchor}"><span class="hu-plan-num">{n}</span>'
    f'<span class="hu-plan-text"><strong>{title}</strong><small>{sub}</small></span>'
    f'<span class="hu-plan-arrow" aria-hidden="true">↓</span></a></li>'
    for n, (anchor, title, sub) in enumerate(HU_PLAN, 1))
KIT_MAIN = kit_card(*C.HURRICANE_KIT[0], main=True)
KIT_SIDE = "\n".join(kit_card(name, items) for name, items in C.HURRICANE_KIT[1:])
HU_DONTS = "\n".join(
    f'          <li><span class="dd-mark">{HU_X_ICON}</span><span>{t}</span></li>' for t in C.HURRICANE_DONTS)
HU_DOS = "\n".join(
    f'          <li><span class="dd-mark">{HU_CHECK_ICON}</span><span>{with_refs(t, C.HURRICANE_SOURCES)}</span></li>'
    for t in C.HURRICANE_DOS)
MUST_CARDS = "\n".join(
    f"""      <article class="must-card is-{MUST_COLOURS[i % 3]}">
        <span class="must-icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{MUST_HAVE_ICONS[name]}</svg></span>
        <h3>{name}</h3>
        <ul class="must-list">
{chr(10).join(f"          <li>{t}</li>" for t in items)}
        </ul>
      </article>""" for i, (name, items) in enumerate(C.HURRICANE_MUST_HAVES))

HURRICANE_BODY = page_hero(
    "Hurricanes &amp; Your Pets",
    "When it's time to evacuate, everyone in your household should know exactly what to grab, and that includes everything your pets will need.",
    "Hurricanes &amp; Your Pets",
) + f"""
<section class="section">
  <div class="container">
    {review_note("<p>This guidance was written for Louisiana — it names the LA/SPCA, the Louisiana Department of Agriculture &amp; Forestry and a free-tag offer “for a limited time”. Carried over unchanged; worth generalizing for a national audience.</p><p>The Major Dos also send readers to <strong>www.petsallowed-hotels.com</strong>, which no longer exists (checked October 2026). It needs replacing or removing.</p>")}
    <div class="tips-intro hu-intro">
      <div>
        <p class="eyebrow">Before the storm</p>
        <h2>Make a plan before you need it</h2>
        <p class="tips-lead">{C.HURRICANE_INTRO}</p>
      </div>
      <nav class="hu-plan" aria-labelledby="hu-plan-title">
        <h3 id="hu-plan-title">Your storm plan, step by step</h3>
        <ol>
{HU_PLAN_STEPS}
        </ol>
      </nav>
    </div>
  </div>
</section>

<section class="section section-soft" id="hu-kit">
  <div class="container">
    <div class="text-center" style="max-width:760px; margin:0 auto var(--space-6)">
      <p class="eyebrow">Evacuation kit</p>
      <h2>What to pack for each pet</h2>
      <p class="lead" style="margin:0 auto">{C.HURRICANE_KIT_INTRO}</p>
      <div class="kit-toolbar">
        <p class="kit-tip">Tap an item to tick it off as you pack. Your ticks are remembered on this device.</p>
        <button type="button" class="kit-clear" disabled><span aria-hidden="true">↺</span> Clear</button>
      </div>
    </div>
    <div class="kit-grid">
{KIT_MAIN}
      <div class="kit-side">
{KIT_SIDE}
      </div>
    </div>
  </div>
</section>

<section class="section" id="hu-dos">
  <div class="container">
    <div class="text-center" style="max-width:760px; margin:0 auto var(--space-6)">
      <p class="eyebrow">Plan ahead</p>
      <h2>What to do, and what to avoid</h2>
    </div>
    <div class="dd-grid">
      <div class="dd-card is-dont">
        <div class="dd-head"><span class="dd-head-icon" aria-hidden="true">{HU_X_ICON}</span><h3>Major Don'ts</h3></div>
        <ul class="dd-list">
{HU_DONTS}
        </ul>
      </div>
      <div class="dd-card is-do">
        <div class="dd-head"><span class="dd-head-icon" aria-hidden="true">{HU_CHECK_ICON}</span><h3>Major Dos</h3></div>
        <ul class="dd-list">
{HU_DOS}
        </ul>
      </div>
    </div>
    <aside class="tips-sources hu-sources" aria-labelledby="hu-sources-title">
      <div class="tips-sources-head">
        <span class="tips-sources-icon" aria-hidden="true">{BOOK_ICON}</span>
        <div>
          <h3 id="hu-sources-title">Websites mentioned above</h3>
          <p>Outside websites referenced in the Major Dos. Each opens in a new tab.</p>
        </div>
      </div>
{pet_tips_sources(C.HURRICANE_SOURCES)}
    </aside>
  </div>
</section>

<section class="section section-soft" id="hu-must">
  <div class="container">
    <div class="text-center" style="max-width:760px; margin:0 auto var(--space-6)">
      <p class="eyebrow">Must haves</p>
      <h2>Three things every pet needs</h2>
    </div>
    <div class="must-grid">
{MUST_CARDS}
    </div>
  </div>
</section>

<section class="section section-cream tips-closing" id="hu-after">
  <div class="container">
    <div class="tips-closing-card">
      <p class="eyebrow">After the storm</p>
      <h2>Be patient as your pet settles back in</h2>
      <p class="tips-closing-text">{C.HURRICANE_AFTER}</p>
      <a class="btn btn-secondary btn-lg" href="cats-and-dogs.html">More pet care articles</a>
    </div>
  </div>
</section>
"""

# --- ANIMAL INFO: DELAWARE RESIDENTS ----------------------------------------
DE_ICONS = {
    "pin": ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>'),
    "globe": GLOBE_ICON,
    "heart": ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z"/></svg>'),
}
DE_FACT_CARDS = "\n".join(
    f'      <div class="way-card"><span class="way-icon" aria-hidden="true">{DE_ICONS[icon]}</span><h3>{title}</h3><p>{text}</p></div>'
    for title, icon, text in C.DELAWARE_FACTS)


def de_partner(name, colour, site):
    """Horizontal partner card: a paw badge in the card's colour stands in for
    a logo; the website (if any) is a small reference-style link."""
    link = "\n          " + site_link(*site) if site else ""
    return f"""      <article class="de-partner is-{colour}">
        <span class="de-partner-mark" aria-hidden="true">{PAW_ICON}</span>
        <div class="de-partner-body">
          <p class="de-partner-label">Supported by NHS</p>
          <h3>{name}</h3>{link}
        </div>
        <span class="de-partner-watermark" aria-hidden="true">{PAW_ICON}</span>
      </article>"""


DE_PARTNER_CARDS = "\n".join(de_partner(*p) for p in C.DELAWARE_PARTNERS)

DELAWARE_BODY = page_hero(
    "Delaware Residents",
    "We're a Delaware nonprofit helping animals in all 50 states, and support from Delaware goes to animal charities right here at home.",
    "Delaware Residents",
) + f"""
<section class="section">
  <div class="container">
    <div class="text-center" style="max-width:960px; margin:0 auto var(--space-6)">
      <p class="eyebrow">Our home state</p>
      <h2>A Delaware nonprofit with a national reach</h2>
    </div>
    <div class="ways-grid de-facts">
{DE_FACT_CARDS}
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <div class="text-center" style="max-width:760px; margin:0 auto var(--space-6)">
      <p class="eyebrow">Local partners</p>
      <h2>Delaware shelters we've supported</h2>
      <p class="lead" style="margin:0 auto">{C.DELAWARE_PARTNERS_LINE}</p>
    </div>
    <div class="de-partners-wrap">
      {review_note("<p>The page says NHS has given to <strong>“Delaware Humane Society”</strong>. The Wilmington shelter of that kind was the Delaware Humane Association, which merged with the Delaware SPCA in 2022 to become Humane Animal Partners (humaneanimalpartners.org). Please confirm the name to show, and whether to link their website.</p>")}
      <div class="de-partners">
{DE_PARTNER_CARDS}
      </div>
    </div>
  </div>
</section>

<section class="section section-cream tips-closing">
  <div class="container">
    <div class="tips-closing-card">
      <p class="eyebrow">Questions?</p>
      <h2>Have a question about giving from Delaware?</h2>
      <p class="tips-closing-text">Our customer service team is happy to help. You can also read about the shelters and animals your support reaches across the country.</p>
      <div class="de-actions">
        <a class="btn btn-primary btn-lg de-call" href="{tel(C.CUSTOMER_SERVICE)}"><span aria-hidden="true">{PHONE_ICON}</span>Call {C.CUSTOMER_SERVICE}</a>
        <a class="btn btn-secondary btn-lg" href="donations-helping-animals.html">Donations Helping Animals</a>
      </div>
    </div>
  </div>
</section>
"""

# --- ANIMAL PROGRAMS --------------------------------------------------------
PROG_ICONS = {
    "national": ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">'
                 '<circle cx="12" cy="12" r="9.5"/><path d="M2.5 12h19"/><path d="M12 2.5c2.6 2.6 3.9 5.8 3.9 9.5s-1.3 6.9-3.9 9.5c-2.6-2.6-3.9-5.8-3.9-9.5s1.3-6.9 3.9-9.5z"/></svg>'),
    "breed": ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
              '<ellipse cx="12" cy="15.6" rx="5.2" ry="4.4"/><ellipse cx="5.2" cy="9.6" rx="2.1" ry="2.7"/>'
              '<ellipse cx="9.1" cy="5.8" rx="2.2" ry="2.9"/><ellipse cx="14.9" cy="5.8" rx="2.2" ry="2.9"/>'
              '<ellipse cx="18.8" cy="9.6" rx="2.1" ry="2.7"/></svg>'),
    "working": ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                '<circle cx="12" cy="9" r="6"/><path d="M8.5 13.9L7 22l5-3 5 3-1.5-8.1"/></svg>'),
}
PROG_COLOURS = ["coral", "teal", "orange", "blue"]
_STROKE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
           'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">')
PROG_ICONS.update({
    "pin": _STROKE + '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
    "list": _STROKE + '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r="1"/><circle cx="4.5" cy="12" r="1"/><circle cx="4.5" cy="18" r="1"/></svg>',
    "info": _STROKE + '<circle cx="12" cy="12" r="9.5"/><path d="M12 11v6"/><path d="M12 7.5h.01"/></svg>',
    "hospital": _STROKE + '<rect x="3.5" y="3.5" width="17" height="17" rx="3"/><path d="M12 8v8M8 12h8"/></svg>',
    "book": _STROKE + '<path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v17H6.5A2.5 2.5 0 0 0 4 21.5z"/><path d="M4 21.5A2.5 2.5 0 0 1 6.5 19H20v3H6.5"/><path d="M8 7h8M8 11h6"/></svg>',
})


def dir_link(name, url):
    """One organization in the directory: name, domain, arrow; opens in a new tab."""
    return (f'<a class="dir-link" href="{url}" target="_blank" rel="noopener">'
            f'<span class="dir-link-text"><strong>{name}</strong>'
            f'<small><span class="site-link-globe" aria-hidden="true">{GLOBE_ICON}</span>{source_domain(url)}</small></span>'
            f'<span class="dir-link-arrow" aria-hidden="true">↗</span></a>')


def org_details(org, note):
    """The extra text under a state organization: its note as an info line,
    then any clinics, each with a hospital icon, address and call chip."""
    clinics = C.VET_CLINICS.get(org, [])
    if not note and not clinics:
        return ""
    parts = []
    if note:
        parts.append(f'<p class="org-note"><span class="org-note-icon" aria-hidden="true">{PROG_ICONS["info"]}</span><span>{note}</span></p>')
    if clinics:
        rows = "\n".join(
            f'                <li class="clinic"><span class="clinic-icon" aria-hidden="true">{PROG_ICONS["hospital"]}</span>'
            f'<span class="clinic-text"><strong>{name}</strong><span>{street}, {city}</span>'
            f'<a class="clinic-phone" href="{tel(phone)}"><span aria-hidden="true">{PHONE_ICON}</span>{phone}</a></span></li>'
            for name, street, city, phone in clinics)
        parts.append(f'<ul class="clinics">\n{rows}\n              </ul>')
    return '\n            <div class="org-details">\n              ' + "\n              ".join(parts) + '\n            </div>'


def dir_group(title, icon, colour, items):
    links = "\n".join(f"          <li>{dir_link(n, u)}</li>" for n, u in items)
    return f"""      <div class="dir-group is-{colour}">
        <div class="dir-group-head"><span class="dir-group-icon" aria-hidden="true">{PROG_ICONS[icon]}</span><h3>{title}</h3></div>
        <ul class="dir-links">
{links}
        </ul>
      </div>"""


def state_slug(state):
    return "state-" + state.lower().replace(" ", "-")


def state_cards():
    cards = []
    for i, (state, orgs) in enumerate(C.VET_STATES):
        rows = []
        for name, url, note in orgs:
            rows.append(f"""          <li class="dir-org">
            {dir_link(name, url)}{org_details(name, note)}
          </li>""")
        cards.append(f"""      <section class="state-card is-{PROG_COLOURS[i % 4]}" id="{state_slug(state)}" aria-labelledby="{state_slug(state)}-title">
        <div class="state-card-head"><span class="state-abbr" aria-hidden="true">{C.STATE_ABBR[state]}</span><h4 id="{state_slug(state)}-title">{state}</h4></div>
        <ul class="dir-links">
{chr(10).join(rows)}
        </ul>
      </section>""")
    return "\n".join(cards)


STATE_CHIPS = "\n".join(
    f'      <a class="foods-chip" href="#{state_slug(st)}">{st}</a>' for st, _ in C.VET_STATES)
PROG_GROUPS = "\n".join([
    dir_group("National organizations", "national", "coral", C.VET_GENERAL),
    dir_group("Breed Specific Assistance Programs", "breed", "teal", C.VET_BREED),
    dir_group("Working Dog", "working", "orange", C.VET_WORKING_DOG),
])


def prog_resource(colour, icon, title, sub, button, href):
    """A tinted, fully clickable panel: icon, title, small line, button.
    Outside links open in a new tab; # links jump down the page."""
    outside = href.startswith("http")
    target = ' target="_blank" rel="noopener"' if outside else ""
    arrow = "↗" if outside else "↓"
    return (f'<a class="prog-resource is-{colour}" href="{href}"{target}>'
            f'<span class="prog-resource-icon" aria-hidden="true">{PROG_ICONS[icon]}</span>'
            f'<span class="prog-resource-text"><strong>{title}</strong><small>{sub}</small></span>'
            f'<span class="prog-resource-btn">{button} <span aria-hidden="true">{arrow}</span></span></a>')


SPAY_RESOURCE = prog_resource(
    "coral", "pin", C.SPAY_LINK[0], f"{source_domain(C.SPAY_LINK[1])} · opens in a new tab",
    "Find help near you", C.SPAY_LINK[1])
VET_RESOURCE = prog_resource(
    "teal", "list", "Veterinary care assistance directory", "National, breed-specific and state programs",
    "Browse the directory", "#vet-directory")


PROGRAMS_BODY = page_hero(
    "Animal Programs",
    "Resources to help pet owners find spay/neuter services and financial help with veterinary care.",
    "Animal Programs",
) + f"""
<section class="section">
  <div class="container">
    <div class="text-center" style="max-width:760px; margin:0 auto var(--space-6)">
      <p class="eyebrow">Where to start</p>
      <h2>Spay/neuter and vet care resources</h2>
    </div>
    <div class="prog-grid">
      <article class="prog-card">
        <div class="post-cover is-coral"><span class="post-cover-topic">Spay/Neuter</span></div>
        <div class="prog-card-body">
          <h3>Additional Spay/Neuter Info</h3>
          {SPAY_RESOURCE}
        </div>
      </article>
      <article class="prog-card">
        <div class="post-cover is-teal"><span class="post-cover-topic">Veterinary Care</span></div>
        <div class="prog-card-body">
          <h3>Help paying for vet care</h3>
          {VET_RESOURCE}
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section section-soft" id="vet-directory">
  <div class="container">
    <div class="tips-intro prog-intro">
      <div>
        <p class="eyebrow">Veterinary care</p>
        <h2>Veterinary Care Help</h2>
        <p class="tips-lead">{C.VET_HELP_INTRO}</p>
      </div>
      <div class="tips-photo">
        <img src="assets/img/programs-vet.jpg" alt="A veterinarian holding a cat during a check-up" width="570" height="618">
      </div>
    </div>

    {review_note("<p>We checked every link in this directory (October 2026). Several no longer work:</p><ul><li><strong>Redirect to a different site:</strong> PAWS San Diego (pawssdc.org now goes to an unrelated pet-gear site, pawgearlab.com); Max Fund (maxfund.org now goes to truecompanions.org; it may have rebranded).</li><li><strong>Website no longer exists:</strong> Voice for the Animals Foundation (vftafoundation.org); Manchester Area Network on AIDS AID-A-PET (mana-ct.net).</li><li><strong>Not responding:</strong> Canine Cancer Awareness, PAWS San Francisco, RIVMA Companion Animal Foundation.</li><li><strong>Page not found:</strong> Phinney&#8217;s Friends (MSPCA) and SPCA of Texas. Their home pages still work.</li></ul><p>Suggest NHS reviews the directory before launch: confirm, update or remove these entries.</p>")}
    <div class="dir-groups">
{PROG_GROUPS}
    </div>

    <div class="text-center prog-states-head">
      <p class="eyebrow">By state</p>
      <h2>State-Specific Programs</h2>
    </div>
    <nav class="foods-jump prog-jump-nav" aria-labelledby="prog-states-title">
      <h3 class="foods-jump-title" id="prog-states-title">Browse by state</h3>
      <div class="foods-chips">
{STATE_CHIPS}
      </div>
    </nav>
    <div class="state-grid">
{state_cards()}
    </div>
    <div class="prog-more">
      <span class="prog-more-icon" aria-hidden="true">{PROG_ICONS["book"]}</span>
      <div class="prog-more-text">
        <h3>More information</h3>
        <p>{C.CDC_LINK[0]}.</p>
      </div>
      <a class="btn btn-secondary prog-more-btn" href="{C.CDC_LINK[1]}" target="_blank" rel="noopener">CDC Healthy Pets <span aria-hidden="true">↗</span></a>
    </div>
  </div>
</section>

<section class="section section-cream tips-closing">
  <div class="container">
    <div class="tips-closing-card">
      <p class="eyebrow">Make it possible</p>
      <h2>Help more animals get the care they need</h2>
      <p class="tips-closing-text">Your support helps shelters and rescues care for animals across the country.</p>
      <a class="btn btn-primary btn-lg btn-donate" href="donate.html"><span class="donate-heart" aria-hidden="true">♥</span>Donate today</a>
    </div>
  </div>
</section>
"""

# --- WILLS & ESTATES --------------------------------------------------------
_WS = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
       'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">')
WILLS_ICONS = {k: _WS + v + "</svg>" for k, v in {
    "dollar": '<path d="M12 2v20"/><path d="M17 6.5c-1-1.5-2.8-2.5-5-2.5-2.8 0-5 1.6-5 3.8 0 5.2 10 2.6 10 8 0 2.3-2.2 4.2-5 4.2-2.4 0-4.4-1-5.3-2.7"/>',
    "percent": '<path d="M19 5L5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 13l9 5 9-5"/>',
    "cash": '<rect x="2.5" y="6" width="19" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/><path d="M6 9.5h.01M18 14.5h.01"/>',
    "gift": '<rect x="3" y="8" width="18" height="13" rx="2"/><path d="M12 8v13M3 12.5h18"/><path d="M12 8C10.5 5 7 4.5 7 6.8 7 8 9 8 12 8zm0 0c1.5-3 5-3.5 5-1.2C17 8 15 8 12 8z"/>',
    "home": '<path d="M3 11l9-7 9 7"/><path d="M5 9.5V20h14V9.5"/><path d="M10 20v-5h4v5"/>',
    "chart": '<path d="M3 20h18"/><path d="M6 16l4-5 3 3 5-7"/><path d="M15 7h3v3"/>',
    "heart": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
    "bank": '<path d="M3 10l9-6 9 6"/><path d="M5 10v8M9.5 10v8M14.5 10v8M19 10v8"/><path d="M3 21h18"/>',
    "umbrella": '<path d="M3 12a9 9 0 0 1 18 0z"/><path d="M12 12v7a2 2 0 0 1-4 0"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6l8-3z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "doc": '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6"/><path d="M8 13h8M8 17h5"/>',
    "copy": '<rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/>',
    "info": '<circle cx="12" cy="12" r="9.5"/><path d="M12 11v6"/><path d="M12 7.5h.01"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
}.items()}

WILLS_WAY_CARDS = "\n".join(
    f'      <div class="way-card"><span class="way-icon" aria-hidden="true">{WILLS_ICONS[icon]}</span><h3>{title}</h3><p>{text}</p></div>'
    for title, icon, text in C.WILLS_WAYS)
# Bequest: blanks are labelled lines on screen and underscores when copied
WILLS_BEQUEST_HTML = "".join(
    part if i % 2 == 0 else f'<span class="bequest-blank">{part}</span>'
    for i, part in enumerate(C.WILLS_BEQUEST))
WILLS_BEQUEST_COPY = html.escape("\u201c" + "".join(
    part if i % 2 == 0 else "________" for i, part in enumerate(C.WILLS_BEQUEST)) + "\u201d", quote=True)
WILLS_TRUST_TILES = "\n".join(
    f'      <div class="trust-tile is-{PROG_COLOURS[i % 4]}"><span class="trust-icon" aria-hidden="true">{WILLS_ICONS[icon]}</span><span>{name}</span></div>'
    for i, (name, icon) in enumerate(C.WILLS_TRUST_ITEMS))
WILLS_FORM_CARDS = "\n".join(
    f"""      <article class="must-card is-{('coral', 'teal')[i]}">
        <span class="must-icon" aria-hidden="true">{WILLS_ICONS[icon]}</span>
        <h3>{title}</h3>
        <p class="must-text">{text}</p>
      </article>""" for i, (title, icon, text) in enumerate(C.WILLS_FORMS))
WILLS_RETIREMENT_BLOCKS = "\n".join(
    f'        <div class="plan-block"><h4>{t}</h4><p>{x}</p></div>' for t, x in C.WILLS_RETIREMENT)
WILLS_LIFE_CARDS = "\n".join(
    f'        <div class="life-option"><span class="life-num" aria-hidden="true">{n}</span><h4>{t}</h4><p>{x}</p></div>'
    for n, (t, x) in enumerate(C.WILLS_LIFE_OPTIONS, 1))

WILLS_BODY = page_hero(
    "Wills &amp; Estates",
    "Remember animals in need with a gift in your will, trust, retirement account or life insurance policy.",
    "Wills &amp; Estates",
) + f"""
<section class="section">
  <div class="container">
    {review_note("<p>Carried over from the current page with three small clean-ups: the sample bequest language has labelled blanks where the address and amounts go (and a Copy button that copies it with underscores); a paragraph about spaying that had been pasted into the Life Insurance section is left out; and the second of two identical “Charitable gifts by assigning a beneficiary” headings is retitled.</p>")}
    <div class="tips-intro wills-intro">
      <div>
        <p class="eyebrow">Planned giving</p>
        <h2>Distributing Wills</h2>
        <p class="tips-lead">{C.WILLS_INTRO}</p>
      </div>
      <aside class="charity-card" aria-labelledby="charity-title">
        <span class="charity-icon" aria-hidden="true">{WILLS_ICONS["shield"]}</span>
        <p class="charity-label">National Humane Society</p>
        <h3 id="charity-title">Charity Information</h3>
        <p class="charity-text">{C.WILLS_CHARITY}</p>
        <div class="charity-taxid">
          <span class="charity-taxid-label">Our tax ID number is:</span>
          <span class="charity-taxid-row"><span class="charity-taxid-num">{C.WILLS_TAX_ID}</span><button type="button" class="bequest-copy taxid-copy" data-copy="{C.WILLS_TAX_ID}" aria-label="Copy tax ID number"><span aria-hidden="true">{WILLS_ICONS["copy"]}</span><span class="bequest-copy-label">Copy</span></button></span>
        </div>
        <span class="charity-paw" aria-hidden="true">{PAW_ICON}</span>
      </aside>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <div class="text-center" style="max-width:820px; margin:0 auto var(--space-6)">
      <p class="eyebrow">Your will or trust</p>
      <h2>Different ways to give back with your will or trust</h2>
    </div>
    <div class="ways-grid wills-ways">
{WILLS_WAY_CARDS}
    </div>

    <figure class="bequest-doc">
      <div class="bequest-doc-head">
        <span class="bequest-doc-icon" aria-hidden="true">{WILLS_ICONS["doc"]}</span>
        <figcaption>Below is an example of how to include such language in your will or trust:</figcaption>
        <button type="button" class="bequest-copy" data-copy="{WILLS_BEQUEST_COPY}"><span aria-hidden="true">{WILLS_ICONS["copy"]}</span><span class="bequest-copy-label">Copy text</span></button>
      </div>
      <blockquote class="bequest-text">\u201c{WILLS_BEQUEST_HTML}\u201d</blockquote>
    </figure>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="text-center" style="max-width:760px; margin:0 auto var(--space-6)">
      <p class="eyebrow">Trusts</p>
      <h2>Trusts can also be gifted to the National Humane Society to include:</h2>
    </div>
    <div class="trust-grid">
{WILLS_TRUST_TILES}
    </div>

    <div class="text-center wills-forms-head">
      <h2>Your Will and/or Trusts can be bequeathed in two different forms</h2>
    </div>
    <div class="wills-forms">
{WILLS_FORM_CARDS}
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <div class="text-center" style="max-width:760px; margin:0 auto var(--space-6)">
      <p class="eyebrow">More ways to give</p>
      <h2>Retirement assets and life insurance</h2>
    </div>
    <article class="plan-card is-blue">
      <div class="plan-head"><span class="plan-icon" aria-hidden="true">{WILLS_ICONS["bank"]}</span><h3>Assets from Retirement</h3></div>
      <div class="plan-blocks">
{WILLS_RETIREMENT_BLOCKS}
      </div>
    </article>
    <article class="plan-card is-orange">
      <div class="plan-head"><span class="plan-icon" aria-hidden="true">{WILLS_ICONS["umbrella"]}</span><h3>Life Insurance Policies</h3></div>
      <p class="plan-intro">{C.WILLS_LIFE_INTRO}</p>
      <div class="life-options">
{WILLS_LIFE_CARDS}
      </div>
    </article>
    <aside class="wills-disclaimer" aria-labelledby="disclaimer-title">
      <span class="wills-disclaimer-icon" aria-hidden="true">{WILLS_ICONS["info"]}</span>
      <div><h3 id="disclaimer-title">Disclaimer</h3><p>{C.WILLS_DISCLAIMER}</p></div>
    </aside>
  </div>
</section>

<section class="section section-cream tips-closing">
  <div class="container">
    <div class="tips-closing-card">
      <p class="eyebrow">Questions?</p>
      <h2>Thinking about leaving a gift?</h2>
      <p class="tips-closing-text">We're happy to answer your questions about including the National Humane Society in your will or estate plans.</p>
      <div class="de-actions">
        <a class="btn btn-primary btn-lg de-call" href="{tel(C.CUSTOMER_SERVICE)}"><span aria-hidden="true">{PHONE_ICON}</span>Call {C.CUSTOMER_SERVICE}</a>
        <a class="btn btn-secondary btn-lg de-call" href="mailto:{C.EMAIL}"><span aria-hidden="true">{WILLS_ICONS["mail"]}</span>Email us</a>
      </div>
    </div>
  </div>
</section>
"""

# --- CONTACT ----------------------------------------------------------------
CONTACT_ICONS = {k: _WS + v + "</svg>" for k, v in {
    "pin": '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "headset": '<path d="M4 14v-2a8 8 0 0 1 16 0v2"/><rect x="2.5" y="13.5" width="4" height="6" rx="1.5"/><rect x="17.5" y="13.5" width="4" height="6" rx="1.5"/><path d="M19.5 19.5c0 1.5-1.5 2.5-4 2.5h-2"/>',
    "send": '<path d="M21.5 2.5L10.5 13.5"/><path d="M21.5 2.5l-7 19-4-8-8-4z"/>',
}.items()}
X_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" '
          'd="M17.75 3h3.07l-6.71 7.67L22 21h-6.18l-4.84-6.33L5.44 21H2.37l7.18-8.2L2 3h6.34l4.37 5.78L17.75 3zm-1.08 16.17h1.7L7.4 4.74H5.58l11.09 14.43z"/></svg>')
CONTACT_ADDRESS = ["N.H.S."] + C.ADDRESS_LINES[1:]


def contact_copy(text, label, aria):
    """Small Copy button for the light contact cards (uses nav.js [data-copy])."""
    return (f'<button type="button" class="bequest-copy contact-copy" data-copy="{text}" aria-label="{aria}">'
            f'<span aria-hidden="true">{WILLS_ICONS["copy"]}</span><span class="bequest-copy-label">{label}</span></button>')


CONTACT_CARDS = "\n".join([
    f"""      <article class="contact-card is-coral">
        <span class="contact-card-icon" aria-hidden="true">{PHONE_ICON}</span>
        <h3>Order Line</h3>
        <a class="contact-card-value" href="{tel(C.ORDER_LINE)}">{C.ORDER_LINE}</a>
        <div class="contact-card-actions"><a class="contact-action" href="{tel(C.ORDER_LINE)}">Call now</a></div>
      </article>""",
    f"""      <article class="contact-card is-teal">
        <span class="contact-card-icon" aria-hidden="true">{CONTACT_ICONS["headset"]}</span>
        <h3>Customer Service</h3>
        <a class="contact-card-value" href="{tel(C.CUSTOMER_SERVICE)}">{C.CUSTOMER_SERVICE}</a>
        <div class="contact-card-actions"><a class="contact-action" href="{tel(C.CUSTOMER_SERVICE)}">Call now</a></div>
      </article>""",
    f"""      <article class="contact-card is-blue">
        <span class="contact-card-icon" aria-hidden="true">{WILLS_ICONS["mail"]}</span>
        <h3>Email</h3>
        <a class="contact-card-value contact-card-email" href="mailto:{C.EMAIL}">{C.EMAIL.replace("@", "@<wbr>")}</a>
        <div class="contact-card-actions"><a class="contact-action" href="mailto:{C.EMAIL}">Email us</a>{contact_copy(C.EMAIL, "Copy", "Copy email address")}</div>
      </article>""",
    f"""      <article class="contact-card is-orange">
        <span class="contact-card-icon" aria-hidden="true">{CONTACT_ICONS["pin"]}</span>
        <h3>By mail</h3>
        <address class="contact-card-value contact-card-address">{"<br>".join(CONTACT_ADDRESS)}</address>
        <div class="contact-card-actions">{contact_copy(", ".join(CONTACT_ADDRESS), "Copy address", "Copy mailing address")}</div>
      </article>""",
])

CONTACT_BODY = page_hero(
    "Contact",
    "Call, email or write to us. We're always glad to hear from you.",
    "Contact",
) + f"""
<section class="section">
  <div class="container">
    <div class="contact-banner">
      <div class="contact-banner-media"><img class="contact-banner-img" src="assets/img/header-cat-glasses.jpg" alt="A cat wearing glasses being petted" width="1200" height="800"></div>
      <div class="contact-banner-card">
        <p class="eyebrow">Get in touch</p>
        <h2>We're here to help</h2>
        <p>Should you need any information concerning our car raffles, the spaying and neutering of cats and dogs or if you have any other questions or comments please contact us.</p>
      </div>
      <span class="contact-banner-paw" aria-hidden="true">{PAW_ICON}</span>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <div class="text-center" style="max-width:760px; margin:0 auto var(--space-6)">
      <p class="eyebrow">Contact details</p>
      <h2>Ways to reach us</h2>
    </div>
    <div class="contact-grid">
{CONTACT_CARDS}
    </div>
  </div>
</section>

<section class="section">
  <div class="container contact-split">
    <div class="contact-form-card">
      <p class="eyebrow">Write to us</p>
      <h2>Send a message</h2>
      {review_note("<p>The current contact page lists phone, email and mailing address only. This form is a proposed addition; the topic list would let staff route messages.</p>")}
      <form class="form-grid form-wide" onsubmit="event.preventDefault(); alert('Preview only — contact form');">
        <div class="contact-form-pair">
          <div class="form-row"><label for="cf-name">Full name</label><input id="cf-name" type="text" autocomplete="name" required></div>
          <div class="form-row"><label for="cf-email">Email address</label><input id="cf-email" type="email" autocomplete="email" required></div>
        </div>
        <div class="form-row"><label for="cf-topic">What is it about?</label>
          <select id="cf-topic">
            <option>Sweepstakes or Raffle Plus tickets</option>
            <option>A donation</option>
            <option>Wills &amp; estates</option>
            <option>Pet care or vet help</option>
            <option>Something else</option>
          </select>
        </div>
        <div class="form-row"><label for="cf-message">Message</label><textarea id="cf-message" rows="6" required></textarea></div>
        <button class="btn btn-primary btn-lg contact-send" type="submit"><span aria-hidden="true">{CONTACT_ICONS["send"]}</span>Send message</button>
      </form>
    </div>
    <aside class="contact-x-card" aria-labelledby="contact-x-title">
      <span class="contact-x-logo" aria-hidden="true">{X_ICON}</span>
      <p class="contact-x-label">National Humane Society</p>
      <h3 id="contact-x-title">@NationalHumane</h3>
      <p>Follow us on X for the latest updates, rescue stories, and animal welfare news.</p>
      <a class="btn btn-primary contact-x-btn" href="{C.SOCIAL[3][1]}" target="_blank" rel="noopener"><span aria-hidden="true">{X_ICON}</span>Follow on X</a>
      <span class="contact-x-paw" aria-hidden="true">{PAW_ICON}</span>
    </aside>
  </div>
</section>
"""

# ---------------------------------------------------------------------------
# Proposed pages — audit recommendations, not on the current site.
# Bracketed values are placeholders that need real numbers from NHS.
# ---------------------------------------------------------------------------

# --- IMPACT (proposed) ------------------------------------------------------
IMPACT_BODY = page_hero(
    "Impact &amp; Outcomes",
    "Annual numbers, multi-year trends, and the specific outcomes your support makes possible.",
    "Impact",
) + """
<section class="section">
  <div class="container">
    <p class="eyebrow text-center">2025 At a glance</p>
    <h2 class="text-center" style="margin-bottom:var(--space-7)">Last year, by the numbers.</h2>
    <div class="grid grid-4">
      <div class="stat-block"><span class="num">[1,234]</span><span class="label">Animals placed</span></div>
      <div class="stat-block coral"><span class="num">[$1.2M]</span><span class="label">Granted to shelters</span></div>
      <div class="stat-block"><span class="num">[123]</span><span class="label">Partner shelters</span></div>
      <div class="stat-block coral"><span class="num">[12,345]</span><span class="label">Spay/neuter procedures</span></div>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <h2>Multi-year trend.</h2>
    <p class="lead">Animals placed in homes through funded shelter programs.</p>
    <table class="table-clean">
      <thead><tr><th>Year</th><th>Animals placed</th><th>Shelter partners</th><th>Grants disbursed</th></tr></thead>
      <tbody>
        <tr><td>2021</td><td>[XXX]</td><td>[XX]</td><td>$[XXX,XXX]</td></tr>
        <tr><td>2022</td><td>[XXX]</td><td>[XX]</td><td>$[XXX,XXX]</td></tr>
        <tr><td>2023</td><td>[XXX]</td><td>[XX]</td><td>$[XXX,XXX]</td></tr>
        <tr><td>2024</td><td>[XXX]</td><td>[XX]</td><td>$[X.X M]</td></tr>
        <tr><td>2025</td><td>[1,234]</td><td>[123]</td><td>$[1.2 M]</td></tr>
      </tbody>
    </table>
    <p style="margin-top:var(--space-5)"><a class="btn btn-secondary" href="donations-helping-animals.html">See the groups we have funded →</a></p>
  </div>
</section>
"""

# --- FINANCIAL TRANSPARENCY (proposed) --------------------------------------
FINANCIAL_BODY = page_hero(
    "Financial Transparency",
    "Audited financials, IRS Form 990, and a clear breakdown of how every dollar is spent.",
    "Financial Transparency",
) + f"""
<section class="section">
  <div class="container-narrow">
    <h2>Where every dollar goes.</h2>
    <div class="expense-bar">
      <span style="background:var(--color-navy); flex: 78">[78]% Programs</span>
      <span style="background:var(--color-coral); flex: 14">[14]% Fundraising</span>
      <span style="background:var(--color-text-muted); flex: 8">[8]% Admin</span>
    </div>
    <p style="color:var(--color-text-muted); font-size:.9rem">Percentages are placeholders. Replace with figures from the most recent audited financial statement.</p>

    <h3 style="margin-top:var(--space-7)">Documents</h3>
    <ul class="list-check">
      <li>Annual Report (PDF) — to be supplied</li>
      <li>Audited Financial Statements (PDF) — to be supplied</li>
      <li>IRS Form 990 (most recent) — to be supplied</li>
      <li>501(c)(3) Determination Letter — to be supplied</li>
      <li>State charitable solicitation registrations — to be supplied</li>
    </ul>

    <h3 style="margin-top:var(--space-7)">Verify our status</h3>
    <p>We are a 501(c)(3) tax-exempt charity.</p>
    <div class="grid grid-3" style="margin-top:var(--space-5)">
      <div class="card text-center"><strong>Charity Navigator</strong><p style="margin-top:8px; color:var(--color-text-muted)">Rating placeholder</p></div>
      <div class="card text-center"><strong>Candid (GuideStar)</strong><p style="margin-top:8px; color:var(--color-text-muted)">Seal placeholder</p></div>
      <div class="card text-center"><strong>BBB Wise Giving</strong><p style="margin-top:8px; color:var(--color-text-muted)">Accreditation placeholder</p></div>
    </div>
  </div>
</section>
"""

# --- MONTHLY GIVING (proposed) ----------------------------------------------
MONTHLY_BODY = page_hero(
    "Monthly Giving",
    "Predictable support, compounded impact.",
    "Monthly Giving",
) + f"""
<section class="section">
  <div class="container grid grid-2" style="align-items:center">
    <div>
      <h2>Why give monthly.</h2>
      <p>The current site already takes monthly donations on the Donate page. A dedicated page would explain why recurring gifts matter and what donors can expect.</p>
      <ul class="list-check">
        <li>[Cost-per-outcome examples — to be supplied by NHS]</li>
        <li>[How to change or cancel a monthly gift]</li>
        <li>[Year-end tax summary — confirm whether offered]</li>
      </ul>
    </div>
    <div class="donate-widget" data-donate>
      <h3>Become a monthly donor</h3>
{DONATE_TOGGLE}
      <div class="amount-grid">
{donate_amount_buttons()}
      </div>
      <a class="btn btn-primary donate-cta" href="donate.html" style="width:100%; justify-content:center">Donate $25 monthly →</a>
    </div>
  </div>
</section>
"""

# --- VOLUNTEER (proposed) ---------------------------------------------------
VOLUNTEER_BODY = page_hero(
    "Volunteer",
    "Ways to help that fit your time and ability.",
    "Volunteer",
) + """
<section class="section">
  <div class="container">
    <div class="grid grid-3">
      <div class="card">
        <div class="card-icon">🐕</div>
        <h3>At a local shelter</h3>
        <p>[Placeholder — walk dogs, socialize cats, help with adoption events.]</p>
      </div>
      <div class="card">
        <div class="card-icon">💻</div>
        <h3>Remote &amp; skills-based</h3>
        <p>[Placeholder — photography, social media, writing.]</p>
      </div>
      <div class="card">
        <div class="card-icon">📨</div>
        <h3>Spread the word</h3>
        <p>[Placeholder — share a rescue story or a sweepstakes entry.]</p>
      </div>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container-narrow">
    <h2>Volunteer interest form</h2>
    <form class="form-grid" onsubmit="event.preventDefault(); alert('Preview only — volunteer signup');">
      <div class="form-row"><label>Full name</label><input type="text" required></div>
      <div class="form-row"><label>Email address</label><input type="email" required></div>
      <div class="form-row"><label>City &amp; state</label><input type="text" required></div>
      <div class="form-row"><label>Anything else we should know?</label><textarea rows="4"></textarea></div>
      <button class="btn btn-primary" type="submit">Submit interest →</button>
    </form>
  </div>
</section>
"""

# --- CORPORATE PARTNERS (proposed) ------------------------------------------
CORP_BODY = page_hero(
    "Corporate Partners",
    "Workplace giving, sponsorships, and matching gifts.",
    "Corporate Partners",
) + """
<section class="section">
  <div class="container">
    <div class="grid grid-3">
      <div class="card"><h3>Prize partners</h3><p>Cars for the sweepstakes are provided by Winner Automobile Group of Delaware and Porsche of Delaware.</p></div>
      <div class="card"><h3>Workplace giving</h3><p>[Placeholder — payroll deduction and employer match.]</p></div>
      <div class="card"><h3>Sponsorships</h3><p>[Placeholder — sponsor a sweepstakes or a program.]</p></div>
    </div>
    <div class="text-center" style="margin-top:var(--space-6)">
      <a class="btn btn-primary" href="contact.html">Talk to us →</a>
    </div>
  </div>
</section>
"""

# ---------------------------------------------------------------------------
# Page registry: (title, slug, body, status)
# ---------------------------------------------------------------------------
PAGES = [
    ("Home", "index.html", HOME_BODY, "live"),
    ("About", "about.html", ABOUT_BODY, "live"),
    ("Animal Programs", "animal-programs.html", PROGRAMS_BODY, "live"),
    ("Donations Helping Animals", "donations-helping-animals.html", DONATIONS_BODY, "live"),
    ("Impact & Outcomes", "impact.html", IMPACT_BODY, "proposed"),
    ("Financial Transparency", "financial-transparency.html", FINANCIAL_BODY, "proposed"),
    ("Sweepstakes", "sweepstakes.html", SWEEPSTAKES_BODY, "live"),
    ("Raffle Plus", "raffle-plus.html", RAFFLE_BODY, "live"),
    ("Enter Our Sweepstakes", "raffle-home-page.html", RAFFLE_HOME_BODY, "live"),
] + [
    (f"{p[1]} Sweepstakes", p[0], prize_body(p), "live") for p in C.PRIZES
] + [
    ("How the Sweepstakes Works", "how-it-works.html", HOW_IT_WORKS_BODY, "new"),
    ("FAQ", "faq.html", FAQ_BODY, "live"),
    ("Sweepstakes & Raffle Rules", "sweepstakes-rules.html", RULES_BODY, "live"),
    ("Previous Winners", "previous-winners.html", WINNERS_BODY, "live"),
    ("Donate", "donate.html", DONATE_BODY, "live"),
    ("Monthly Giving", "monthly-giving.html", MONTHLY_BODY, "proposed"),
    ("Wills & Estates", "wills-estates.html", WILLS_BODY, "live"),
    ("Volunteer", "volunteer.html", VOLUNTEER_BODY, "proposed"),
    ("Corporate Partners", "corporate-partners.html", CORP_BODY, "proposed"),
    ("Educational Messages", "blog.html", BLOG_BODY, "live"),
    ("How Your $10 Monthly Donation Really Helps Shelter Animals", "blog-post.html", BLOG_POST_BODY, "live"),
    ("Videos and More", "videos-and-more.html", VIDEOS_BODY, "live"),
    ("Pet Tips", "pet-tips.html", PET_TIPS_BODY, "live"),
    ("Cats & Dogs", "cats-and-dogs.html", CATS_DOGS_BODY, "live"),
    ("Foods to Avoid", "foods-to-avoid.html", FOODS_BODY, "live"),
    ("Hurricanes & Your Pets", "hurricanes-and-your-pets.html", HURRICANE_BODY, "live"),
    ("Delaware Residents", "delaware-residents.html", DELAWARE_BODY, "live"),
    ("Contact", "contact.html", CONTACT_BODY, "live"),
]


def check_references(pages):
    """Every internal link and local asset a page points at must exist."""
    slugs = {slug for _t, slug, _h in pages}
    problems = []
    for _title, slug, html in pages:
        # The path only: query strings (?tickets=3) and #fragments are ignored.
        for ref in re.findall(r'(?:href|src)="([^"#?]+)(?:[?#][^"]*)?"', html):
            if re.match(r"(https?:|mailto:|tel:|//)", ref):
                continue
            if ref.endswith(".html"):
                if ref not in slugs:
                    problems.append(f"{slug}: broken link to {ref}")
            elif not (OUT_DIR / ref).exists():
                problems.append(f"{slug}: missing asset {ref}")
        for ref in re.findall(r"url\('([^']+)'\)", html):
            if not (OUT_DIR / ref).exists():
                problems.append(f"{slug}: missing image {ref}")
    return sorted(set(problems))


def main():
    rendered = [(title, slug, page(title.replace("&", "&amp;"), slug, body, status))
                for title, slug, body, status in PAGES]
    for _title, slug, html in rendered:
        (OUT_DIR / slug).write_text(html, encoding="utf-8")
    print(f"Wrote {len(rendered)} pages.")

    # Generated pages that are no longer in PAGES would otherwise linger and
    # still be deployed.
    keep = {slug for _t, slug, _h in rendered}
    for stale in sorted(OUT_DIR.glob("*.html")):
        if stale.name not in keep:
            stale.unlink()
            print(f"  removed stale page {stale.name}")

    problems = check_references(rendered)
    for p in problems:
        print(f"  ! {p}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
