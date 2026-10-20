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
      <a class="btn btn-primary" href="donate.html">Donate</a>
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


# Section backgrounds that are not white (see styles.css)
COLOURED_SECTIONS = {"section-soft", "section-cream", "section-navy"}


def page(title, slug, body, status="live", description=None):
    """Returns the full html string for a single page."""
    desc = description or f"{title} — National Humane Society"
    body_class = "is-home" if slug == "index.html" else "is-interior"
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
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Reusable content blocks
# ---------------------------------------------------------------------------
def page_hero(title, lead, breadcrumb_label, parent=None):
    crumb = '<a href="index.html">Home</a> &nbsp;/&nbsp; '
    if parent:
        crumb += f'<a href="{parent[1]}">{parent[0]}</a> &nbsp;/&nbsp; '
    lead_html = f'\n    <p class="lead">{lead}</p>' if lead else ""
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
            pic = f"""<div class="winner-pic"><img src="assets/img/{image}" alt="{name}, {state}" loading="lazy"></div>"""
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
# topic header instead. First keyword found in the title wins.
BLOG_TOPICS = [
    (("spay", "neuter"), "Spay &amp; Neuter", "teal"),
    (("abuse", "cruelty"), "Animal Welfare", "coral"),
    (("volunteer",), "Volunteering", "blue"),
    (("foster",), "Fostering", "orange"),
    (("donation", "donate"), "Giving", "coral"),
    (("summer", "winter", "holiday", "safe "), "Pet Safety", "blue"),
    (("stories", "transformation"), "Rescue Stories", "orange"),
    (("adopt", "myth"), "Adoption", "navy"),
    (("shelter",), "Shelters", "teal"),
]


def blog_topic(title):
    lowered = title.lower()
    for keywords, topic, colour in BLOG_TOPICS:
        if any(k in lowered for k in keywords):
            return topic, colour
    return "Animal Care", "navy"


def blog_cards(posts):
    cards = []
    for title, slug in posts:
        if slug == C.BLOG_SAMPLE_SLUG:
            href, target = "blog-post.html", ""
        else:
            href, target = f"{C.LIVE_SITE}/post/{slug}", ' target="_blank" rel="noopener"'
        topic, colour = blog_topic(title)
        cards.append(f"""      <article class="post-card">
        <div class="post-cover is-{colour}" aria-hidden="true">
          <span class="post-cover-topic">{topic}</span>
        </div>
        <div class="post-body">
          <h3><a href="{href}"{target}>{title}</a></h3>
          <span class="post-more">Read article →</span>
        </div>
      </article>""")
    return '    <div class="grid grid-3">\n' + "\n".join(cards) + "\n    </div>"


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


def edu_video_carousel():
    """YouTube Shorts from the educational playlist. Each card links to the
    video and plays it in place when JavaScript is on (see nav.js)."""
    cards = "\n".join(f"""      <a class="short-card" href="https://www.youtube.com/shorts/{vid}" data-video="{vid}" target="_blank" rel="noopener">
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
      <a class="btn btn-primary btn-lg" href="donate.html">Donate Today</a>
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

<section class="section">
  <div class="container grid grid-2">
    <div>
      <h2>Contribute by mail.</h2>
      <p>To contribute by mail, please send a personal check or money order made payable to the National Humane Society to:</p>
      <p><strong>{MAIL_ADDRESS}</strong></p>
    </div>
    <aside class="proceeds-panel">
      <h4>A 501(c)(3) tax-exempt charity</h4>
      <p style="margin:0"><a href="donate.html">Donate online →</a></p>
    </aside>
  </div>
</section>
"""

# --- ANIMAL PROGRAMS --------------------------------------------------------
def link_list(items):
    lis = "\n".join(
        f'        <li><a href="{url}" target="_blank" rel="noopener">{name}</a></li>'
        for name, url in items
    )
    return f'      <ul class="dir-list">\n{lis}\n      </ul>'


def state_directory():
    blocks = []
    for state, orgs in C.VET_STATES:
        lis = []
        for name, url, note in orgs:
            note_html = f'<br><span class="dir-note">{note}</span>' if note else ""
            lis.append(f'          <li><a href="{url}" target="_blank" rel="noopener">{name}</a>{note_html}</li>')
        blocks.append(f"""      <div class="dir-state">
        <h4>{state}</h4>
        <ul class="dir-list">
{chr(10).join(lis)}
        </ul>
      </div>""")
    return "\n".join(blocks)


PROGRAMS_BODY = page_hero(
    "Animal Programs",
    "Spay/neuter and veterinary care are the two programs at the center of our work.",
    "Animal Programs",
) + f"""
<section class="section">
  <div class="container grid grid-2">
    <div class="card">
      <div class="card-icon">🐾</div>
      <h3>Spay/Neuter</h3>
      <h4>Additional Spay/Neuter Info</h4>
      <p><a href="https://www.animalleague.org/get-involved/spay-usa/" target="_blank" rel="noopener">List of animal shelters and rescue organizations by state →</a></p>
    </div>
    <div class="card">
      <div class="card-icon">🏥</div>
      <h3>Veterinary Care</h3>
      <h4>Veterinary Care Help</h4>
      <p>Here is a list of organizations that provide financial assistance to pet owners who are having trouble affording veterinary care. Keep in mind that each organization is independent, and therefore, have their own set of rules and guidelines as to how they distribute assistance. This means you will have to look into each one individually to determine if you qualify for assistance.</p>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <h2>Veterinary care assistance.</h2>
    <div class="grid grid-3" style="margin-bottom:var(--space-6)">
      <div>
        <h4>National organizations</h4>
{link_list(C.VET_GENERAL)}
      </div>
      <div>
        <h4>Breed Specific Assistance Programs</h4>
{link_list(C.VET_BREED)}
      </div>
      <div>
        <h4>Working Dog</h4>
{link_list(C.VET_WORKING_DOG)}
      </div>
    </div>
    <h3>State-Specific Programs</h3>
    <div class="dir-states">
{state_directory()}
    </div>
    <p style="margin-top:var(--space-5)"><a href="https://www.cdc.gov/healthypets/" target="_blank" rel="noopener">For more information visit the CDC Healthy Pets page →</a></p>
  </div>
</section>
"""

# --- DONATIONS HELPING ANIMALS ----------------------------------------------
def story_long(story):
    title, image, signature, paras = story
    pic = f'<img class="story-photo" src="assets/img/{image}" alt="{title}" loading="lazy">' if image else ""
    return f"""    <article class="story-long">
      {pic}
      <h3>{title}</h3>
{paragraphs(paras)}
      <p class="story-sign">{signature}</p>
    </article>"""


LOGO_ROW = "\n".join(
    f'      <img src="assets/img/{img}" alt="{name}" loading="lazy">' for img, name in C.PARTNER_LOGOS
)

DONATIONS_BODY = page_hero(
    "Donations Helping Animals",
    "These are the shelters and animal groups that we have recently given money to.",
    "Donations Helping Animals",
) + f"""
<section class="section">
  <div class="container">
    <div class="logo-row">
{LOGO_ROW}
    </div>
    <p class="lead text-center" style="margin:var(--space-6) auto 0">Without your help this would not be possible. These groups shelter, feed, provide veterinarian care and rescue animals from storms.</p>
  </div>
</section>

<section class="section section-soft">
  <div class="container-narrow">
    <div class="section-head">
      <h2>Below are some of the recent animals your generous donations have helped.</h2>
      <a class="btn btn-primary" href="donate.html">Donate Today</a>
    </div>
    {review_note("<p>Cupcake's letter is published on the current site alongside a photo of the family's credit statement. The photo is left out here, and the letter itself is a request for help rather than an outcome — worth deciding whether it stays.</p>")}
{chr(10).join(story_long(s) for s in C.STORIES)}
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
    "$25.00 each",
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
DONATE_BODY = page_hero(
    "Donate Now",
    "Every dollar can make a difference for an animal in need.",
    "Donate",
) + f"""
<section class="section">
  <div class="container grid grid-2" style="align-items:start">
    <div>
      <img class="rounded-img" src="assets/img/donate-hero.jpeg" alt="" loading="lazy">
      <p style="margin-top:var(--space-5)">For over 25 years, the National Humane Society has worked tirelessly to put an end to animal abuse and neglect. We are one of the national leaders in the areas of rescue, adoption and welfare, and your tax-deductible donation will help fight cruelty and make a life-changing difference for animals across America.</p>
      <p>Thank you for making the National Humane Society and the animals we serve a part of your life.</p>
    </div>
    <form class="donate-widget" data-donate onsubmit="event.preventDefault(); alert('Preview only — donations are not submitted.');">
      <h3>Select gift amount</h3>
{DONATE_TOGGLE}
      <div class="amount-grid">
{donate_amount_buttons()}
      </div>
      <div class="form-grid">
        <div class="form-row"><label>Other amount</label><input type="text" inputmode="decimal" placeholder="$ Other Amount"></div>
{PERSON_FIELDS}
        <div class="form-row"><label>Your payment information</label>
{PAYMENT_BLOCK}
        </div>
        <button type="submit" class="btn btn-primary donate-cta" style="width:100%; justify-content:center">Donate $25 monthly →</button>
        <p class="form-footnote">Tax-deductible · 501(c)(3). Please remember to spay or neuter your pets. For any questions, please call us at <a href="{tel(C.CUSTOMER_SERVICE)}">{C.CUSTOMER_SERVICE}</a>.</p>
      </div>
    </form>
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <h2 class="text-center" style="margin-bottom:var(--space-6)">Other ways to give.</h2>
    <div class="grid grid-3">
      <div class="card"><h3>By mail</h3><p>Send a personal check or money order made payable to the National Humane Society to {", ".join(C.ADDRESS_LINES[1:])}.</p></div>
      <div class="card"><h3>Wills &amp; estates</h3><p>Assigning the National Humane Society in your will or trust is a helpful way for our organization to continue serving animals in need.</p><a href="wills-estates.html">Learn more →</a></div>
      <div class="card"><h3>Sweepstakes</h3><p>What is better than helping animals in need while winning some incredible prizes?</p><a href="sweepstakes.html">Enter Now →</a></div>
    </div>
  </div>
</section>
"""

# --- WILLS & ESTATES --------------------------------------------------------
BEQUEST = """<blockquote class="bequest">"I give and bequeath to The National Humane Society, a non-profit organization, addressed presently located at ________, in the sum of ________, or ________ of my estate, which will be used for the accomplishment of its general purposes."</blockquote>"""

WILLS_BODY = page_hero(
    "Wills &amp; Estates",
    "We are a 501(c)(3) tax-exempt charity.",
    "Wills &amp; Estates",
) + f"""
<section class="section">
  <div class="container-narrow prose">
    {review_note("<p>Carried over from the current page with three small clean-ups: the sample bequest language has blanks where the address and amounts go (shown here as underscores); a paragraph about spaying that had been pasted into the Life Insurance section is left out; and the second of two identical “Charitable gifts by assigning a beneficiary” headings is retitled.</p>")}
    <h2>Distributing Wills</h2>
    <p>Assigning the National Humane Society in your will or trust is a helpful way for our organization to continue serving animals in need. Several programs and services we offer and sponsor have been supported by individuals including the National Humane Society in their wills.</p>
    <h4>Different ways to give back with your will or trust</h4>
{bullet_list([
    "By setting a specific dollar amount or asset in your will to the National Humane Society",
    "Set a percentage of your estate assigned to the National Humane Society",
    "Designate the remaining of your estate that remains after all bequests to family and/or loved ones",
])}
    <h4>Below is an example of how to include such language in your will or trust:</h4>
    {BEQUEST}

    <h2>Trusts</h2>
    <h4>Trusts can also be gifted to the National Humane Society to include:</h4>
{bullet_list(["Cash gifts", "Personal property", "Real Estate", "Securities"])}

    <h2>Your Will and/or Trusts can be bequeathed in two different forms</h2>
{bullet_list([
    "For unrestricted general purposes. The National Humane Society will use these resources without specific direction.",
    "A specific request (the gift is used to sponsor a specific program)",
])}

    <h2>Assets from Retirement</h2>
    <h4>Charitable gifts by assigning a beneficiary</h4>
    <p>The National Humane Society can be named as a beneficiary or contingent beneficiary from your retirement account. If the account is left to a charity, there are no income taxes subject to the organization. For questions and assistance, contact your retirement plan’s administrator.</p>
    <h4>Charitable gifts through a trust</h4>
    <p>A trust can be named for your retirement plan during the event of excess or unused assets. Further, the trust can issue income to other beneficiaries or heirs for a period of time. After the time has passed, the trust’s assets will fund the assigned charity.</p>

    <h2>Life Insurance Policies</h2>
    <p>A life insurance policy is often forgotten as a way to give back to charity like the National Humane Society. As this policy is similar to beneficiaries in a will, there are many ways to issue a charitable gift.</p>
{bullet_list([
    "Adding a beneficiary or beneficiaries is quite simple. Contact your life insurance provider so they can help add in the charity, such as the National Humane Society, to the policy.",
    "Create a new policy with the National Humane Society named as the primary beneficiary. Here, you will make premium payments to your insurance company or pay on behalf of the National Humane Society. This type of gift does qualify as an income tax deduction.",
    "Give your paid-up policy and assign the National Humane Society as the new owner. Once the transfer is complete, the National Humane Society can receive the full amount immediately or receive the benefit at a later time. The original policy holder will receive an income tax deduction depending on the value of the policy.",
])}

    <h2>Disclaimer</h2>
    <p>The information posted on this page is to provide a general understanding and help guide the reader. For serious inquiries, please consult with your attorney, tax advisor, or business manager. This information is not to be viewed as financial, legal, tax or advice.</p>
  </div>
</section>
"""

# --- EDUCATIONAL MESSAGES (blog index) --------------------------------------
BLOG_BODY = page_hero(
    "Educational Messages",
    "Articles on adoption, pet care, shelters and animal welfare.",
    "Educational Messages",
) + f"""
<section class="section">
  <div class="container">
    {review_note("<p>The twelve most recent titles from the current site are shown. Only <em>How Your $10 Monthly Donation Really Helps Shelter Animals</em> opens inside the preview, as the article template; the others open the current site. All of the roughly 100 posts move across when the site is built.</p>")}
{blog_cards(C.BLOG_POSTS)}
    <p class="text-center" style="margin-top:var(--space-6)"><a class="btn btn-secondary" href="{C.LIVE_SITE}/blog" target="_blank" rel="noopener">View every article on the current site →</a></p>
  </div>
</section>
"""

# --- BLOG POST (article template, using a real post) -----------------------
BLOG_POST_BODY = f"""
<section class="page-hero">
  <div class="container-narrow">
    <div class="breadcrumb"><a href="index.html">Home</a> &nbsp;/&nbsp; <a href="blog.html">Educational Messages</a></div>
    <h1>How Your $10 Monthly Donation Really Helps Shelter Animals</h1>
  </div>
</section>

<section class="section">
  <div class="container-narrow prose">
    {review_note("<p>This article is copied from the current site as far as the first section, to show the article layout. Further down, the published post promises annual impact reports, personalized updates for monthly donors and the option to designate a gift to a specific fund — none of which the current site offers. Worth confirming before it is carried over.</p>")}
    <p>In 2025, an estimated 5.8 million dogs and cats entered U.S. shelters and rescues—a 2% decrease from the previous year, according to Shelter Animals Count's 2025 Annual Data Report. While that's encouraging progress, the numbers remain staggering: about 4.2 million animals were adopted (a modest 0.7% increase), but roughly 597,000 were euthanized, and 757,000 experienced non-live outcomes overall (a slight 1% decline). The national save rate holds steady at around 82%, with two out of three shelters achieving no-kill status (90%+ live release rate). These figures represent real animals facing uncertainty due to overcrowding, medical emergencies, economic surrenders, and limited shelter resources.</p>
    <p>At the National Humane Society, we exist to change that trajectory. We raise donations to directly support animals in crisis—providing food, medical care, transport, and foster resources—while also assisting partner shelters nationwide with funding for supplies, low-cost clinics, emergency responses, and capacity-building programs. In an era of rising veterinary costs and ongoing intake pressures, consistent support makes the biggest difference.</p>
    <p>That's why a small, recurring gift—like $10 per month—packs such powerful impact. Less than the cost of a streaming subscription or a couple of coffees, this amount delivers reliable funding that shelters can count on month after month. Below, we break it down transparently: where the money goes, real stories of animals helped, why monthly giving outperforms one-time donations in tough times, and how you can get involved.</p>

    <h2>Where Exactly Does Your $10 Monthly Donation Go? A Detailed Breakdown</h2>
    <p>Shelters face a wide range of expenses, from daily basics to life-saving interventions. The National Humane Society stretches every dollar through bulk purchasing, volunteer coordination, and partnerships with local rescues. Here's how a modest $10 monthly gift contributes in practical terms (based on national averages and our program data):</p>
    <p><strong>Nutrition and Daily Care.</strong> A medium-sized dog requires about 2–3 cups of quality dry food per day, costing roughly $10–$20 per week (depending on brand and portion). Your $10 covers a full week's worth of nutritious food for one medium dog or several cats/kittens. This prevents malnutrition, supports immune health during stressful shelter stays, and keeps animals adoptable longer.</p>
    <p><strong>Preventive Veterinary Care.</strong> Core vaccines, deworming, flea/tick prevention, and initial exams are essential to stop outbreaks and prepare animals for adoption. These basics cost $50–$150 per animal. Your recurring gift contributes toward preventive packages, reducing the risk of illness spreading in crowded facilities and lowering long-term medical burdens.</p>

    <p><a href="{C.LIVE_SITE}/post/{C.BLOG_SAMPLE_SLUG}" target="_blank" rel="noopener">Continue reading on the current site →</a></p>

    <div class="proceeds-panel" style="margin-top:var(--space-7)">
      <h4>Ready to make a reliable difference?</h4>
      <p style="margin:0 0 var(--space-3)">Your $10 monthly gift is a commitment to consistent hope for animals and shelters nationwide.</p>
      <a class="btn btn-primary btn-sm" href="donate.html">Donate today →</a>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <h2 class="text-center" style="margin-bottom:var(--space-6)">More educational messages.</h2>
{blog_cards(C.BLOG_POSTS[9:12])}
  </div>
</section>
"""

# --- VIDEOS & MORE ----------------------------------------------------------
VIDEO_EMBEDS = "\n".join(
    f'      <div class="video-embed"><iframe src="https://player.vimeo.com/video/{vid}" title="National Humane Society video" loading="lazy" allow="fullscreen; picture-in-picture" allowfullscreen></iframe></div>'
    for vid in C.VIDEO_IDS
)

VIDEOS_BODY = page_hero(
    "Videos and More",
    "",
    "Videos &amp; More",
) + f"""
<section class="section">
  <div class="container">
    {review_note("<p>The current page shows these eight videos without titles, surrounded by leftover template filler text (“Heading 1… Lorem ipsum”). The filler is dropped here; titles for each video would help.</p>")}
    <div class="video-grid">
{VIDEO_EMBEDS}
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container-narrow text-center">
    <p class="eyebrow">Our Instagram</p>
    <h2>Follow @nationalhumane.</h2>
    <p class="lead" style="margin:0 auto var(--space-5)">Rescue stories, sweepstakes news and animal welfare updates.</p>
    <a class="btn btn-primary" href="{C.INSTAGRAM_FEATURED}" target="_blank" rel="noopener">View our featured post →</a>
    <a class="btn btn-secondary" href="{C.SOCIAL[0][1]}" target="_blank" rel="noopener">Follow on Instagram</a>
  </div>
</section>
"""

# --- ANIMAL INFO: PET TIPS --------------------------------------------------
PET_TIPS_BODY = page_hero(
    "Pet Tips",
    "How to Support Shelter Pets with Time, Space, and Money",
    "Pet Tips",
) + f"""
<section class="section">
  <div class="container-narrow prose">
    {review_note("<p>On the current site this tab is headed “Help keep your pet safe during the colder months by following these simple guidelines”, but the article beneath it is about supporting shelter pets and contains several links to unrelated third-party sites. The opening and the list of ideas are shown here; the links are left out. Should this article stay, or should the cold-weather tips come back?</p>")}
    <p>Busy parents juggling work and family, apartment renters with pet limits, and animal lovers on tight budgets often carry the same quiet worry: caring about shelter and rescue pets feels meaningful, but the “right” way to help can feel out of reach. That tension is real, community support for animals is built by many people doing what they can, not a few people doing everything. Volunteering for animal shelters, pet fostering programs, and animal welfare advocacy aren’t reserved for experts or people with perfect circumstances. With a clear sense of what fits a real life, small commitments can ripple into lifesaving impact.</p>

    <h2>Understanding the Three Ways to Help Shelter Pets</h2>
    <p>Helping shelter and rescue pets usually falls into three lanes: giving time, giving space, or giving money. Time means hands-on volunteering roles that keep daily care running. Space means fostering, even short term, so an animal can rest outside the kennel. Money means donations, supplies, or sponsor style gifts that fill the gaps.</p>

    <h2>High-Impact Ways to Help This Month</h2>
    <p>If you’ve ever wished you could do something for shelter pets but didn’t know what would matter most, this is your menu. Pick one or two actions for this month, then build a rhythm you can actually sustain.</p>
    <ol>
      <li>Try fostering with a clear, short plan</li>
      <li>Volunteer where the shelter is actually bottlenecked</li>
      <li>Make one strategic, boring donation that keeps doors open</li>
      <li>Run a “wish-list only” pet supply drive in a tight time box</li>
      <li>Be the admin support rescues rarely have</li>
      <li>Show up for one rescue event and bring a plan, not just enthusiasm</li>
    </ol>
    <p><a href="{C.LIVE_SITE}/animal-info" target="_blank" rel="noopener">Read the full article on the current site →</a></p>
  </div>
</section>
"""

# --- ANIMAL INFO: CATS & DOGS -----------------------------------------------
def article_cards():
    cards = []
    for title, href in C.CATS_DOGS_ARTICLES:
        link = f'<a href="{href}">Read more →</a>' if href else '<span class="dir-note">No article on the current site</span>'
        cards.append(f'      <div class="card"><h3>{title}</h3>{link}</div>')
    return "\n".join(cards)


CATS_DOGS_BODY = page_hero(
    "Information on Dogs &amp; Cats",
    "Please read these very informative articles on topics ranging from the problems with the overpopulation of dogs and cats to useful techniques for caring for your dogs and cats.",
    "Cats &amp; Dogs",
) + f"""
<section class="section">
  <div class="container">
    {review_note("<p>The current site lists these five titles, but only the last one links to an article. The other four have no content behind them — are the articles available, or should the titles be removed?</p>")}
    <div class="grid grid-3">
{article_cards()}
    </div>
  </div>
</section>
"""

# --- ANIMAL INFO: FOODS TO AVOID --------------------------------------------
FOODS_ITEMS = "\n".join(f"""    <div class="faq-item">
      <h3>{name}</h3>
      <p>{text}</p>
    </div>""" for name, text in C.FOODS_TO_AVOID)

FOODS_BODY = page_hero(
    "ASPCA List of People Foods to Avoid Feeding Your Pets",
    "If you suspect your pet has eaten any of the following foods, please note the amount ingested and contact your veterinarian or the ASPCA Animal Poison Control Center at (888) 426-4435.",
    "Foods to Avoid",
    parent=("Cats &amp; Dogs", "cats-and-dogs.html"),
) + f"""
<section class="section">
  <div class="container-narrow">
{FOODS_ITEMS}
  </div>
</section>
"""

# --- ANIMAL INFO: HURRICANES ------------------------------------------------
KIT_BLOCKS = "\n".join(f"""      <div>
        <h4>{name}</h4>
{bullet_list(items)}
      </div>""" for name, items in C.HURRICANE_KIT)

MUST_HAVES = "\n".join(
    f"    <h4>{name}</h4>\n{bullet_list(items)}" for name, items in C.HURRICANE_MUST_HAVES
)

HURRICANE_BODY = page_hero(
    "Hurricanes &amp; Your Pets",
    "Every member of your family should know what he or she needs to take when you evacuate. You also should prepare supplies for your pets.",
    "Hurricanes &amp; Your Pets",
) + f"""
<section class="section">
  <div class="container-narrow prose">
    {review_note("<p>This guidance was written for Louisiana — it names the LA/SPCA, the Louisiana Department of Agriculture &amp; Forestry and a free-tag offer “for a limited time”. Carried over unchanged; worth generalizing for a national audience.</p>")}
    <p>Stock up on nonperishables well ahead of time, add perishable items at the last minute, and have everything ready to go at a moment's notice. Keep everything accessible, stored in sturdy containers (duffel bags, covered trash containers, etc.) that can be carried easily.</p>
    <p>Place the following items in a waterproof container so you're ready to go if you need to evacuate.</p>
    <div class="grid grid-2">
{KIT_BLOCKS}
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container grid grid-2">
    <div>
      <h2>Major Don'ts</h2>
{bullet_list(C.HURRICANE_DONTS)}
    </div>
    <div>
      <h2>Major Dos</h2>
{bullet_list(C.HURRICANE_DOS)}
    </div>
  </div>
</section>

<section class="section">
  <div class="container-narrow prose">
    <h2>Must Haves</h2>
{MUST_HAVES}
    <p>Planning and preparation will help you weather the disaster, but your home may be a very different place afterward, whether you have taken shelter at home or elsewhere, be patient with your pets after a disaster. Try to get them back into their normal routines as soon as possible, and be ready for behavioral problems that may result from the stress of the situation. If behavioral problems persist, or if your pet seems to be having any health problems, talk to your veterinarian.</p>
  </div>
</section>
"""

# --- ANIMAL INFO: DELAWARE RESIDENTS ----------------------------------------
DELAWARE_BODY = page_hero(
    "Delaware Residents",
    "",
    "Delaware Residents",
) + """
<section class="section">
  <div class="container-narrow prose">
    <p class="lead">NHS is a nonprofit organization incorporated in Delaware that provides funding to animal shelters nationally, not just in Delaware.</p>
    <p>NHS solicits and sells raffles to a national market and provides funding to local non-profits to help animal over population in any of the 50 states. Delaware supporters will be used for the benefit of Delaware non profits whose mission is related to animal care, shelters or programs to fight animal over population. In the past NHS has given to Delaware Humane Society and Faithful Friends.</p>
  </div>
</section>
"""

# --- CONTACT ----------------------------------------------------------------
CONTACT_BODY = page_hero(
    "Contact",
    "Should you need any information concerning our car raffles, the spaying and neutering of cats and dogs or if you have any other questions or comments please contact us.",
    "Contact",
) + f"""
<section class="section">
  <div class="container grid grid-2">
    <div>
      <h2>Get in Touch</h2>
      <h3>Order Line</h3>
      <p><a href="{tel(C.ORDER_LINE)}">{C.ORDER_LINE}</a></p>
      <h3 style="margin-top:var(--space-5)">Customer Service</h3>
      <p><a href="{tel(C.CUSTOMER_SERVICE)}">{C.CUSTOMER_SERVICE}</a></p>
      <h3 style="margin-top:var(--space-5)">Email</h3>
      <p><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>
      <h3 style="margin-top:var(--space-5)">By mail</h3>
      <p>N.H.S.<br>{"<br>".join(C.ADDRESS_LINES[1:])}</p>
      <h3 style="margin-top:var(--space-5)">@NationalHumane</h3>
      <p>Follow us on X for the latest updates, rescue stories, and animal welfare news.</p>
      <a class="btn btn-secondary btn-sm" href="{C.SOCIAL[3][1]}" target="_blank" rel="noopener">Follow on X</a>
    </div>
    <div>
      <h2>Send a message.</h2>
      {review_note("<p>The current contact page lists phone, email and mailing address only. This form is a proposed addition.</p>")}
      <form class="form-grid" onsubmit="event.preventDefault(); alert('Preview only — contact form');">
        <div class="form-row"><label>Full name</label><input type="text" required></div>
        <div class="form-row"><label>Email address</label><input type="email" required></div>
        <div class="form-row"><label>Message</label><textarea rows="6" required></textarea></div>
        <button class="btn btn-primary" type="submit">Send →</button>
      </form>
    </div>
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
