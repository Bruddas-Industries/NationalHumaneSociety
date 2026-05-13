"""
National Humane Society — preview site generator.

Single source of truth for header/footer/nav. Each page's content lives in
the PAGES list below. Run `python build.py` to (re)generate every .html
file in this directory.

When we port to WordPress, the LAYOUT here becomes the block theme's
header.html and footer.html templates, and each PAGE entry becomes either
a page template or a page filled with block patterns.
"""

from pathlib import Path

OUT_DIR = Path(__file__).parent

# ---------------------------------------------------------------------------
# Navigation structure (proposed sitemap, audit Section 1.2)
# ---------------------------------------------------------------------------
NAV = [
    ("Our Mission", "about.html", [
        ("About", "about.html"),
        ("Programs", "programs.html"),
        ("Impact & Outcomes", "impact.html"),
        ("Shelter Partners", "shelter-partners.html"),
        ("Financial Transparency", "financial-transparency.html"),
    ]),
    ("Sweepstakes", "sweepstakes.html", [
        ("All Active Sweepstakes", "sweepstakes.html"),
        ("Raffle Plus", "raffle-plus.html"),
        ("How It Works", "how-it-works.html"),
        ("FAQ", "faq.html"),
        ("Rules", "rules.html"),
        ("Previous Winners", "previous-winners.html"),
    ]),
    ("Get Involved", "donate.html", [
        ("Donate", "donate.html"),
        ("Monthly Giving", "monthly-giving.html"),
        ("Wills & Estates", "wills-estates.html"),
        ("Volunteer", "volunteer.html"),
        ("Corporate Partners", "corporate-partners.html"),
    ]),
    ("Resources", "blog.html", [
        ("Blog", "blog.html"),
        ("Videos", "videos.html"),
        ("Pet Care: Cats", "pet-care-cats.html"),
        ("Pet Care: Dogs", "pet-care-dogs.html"),
        ("Hurricane Prep", "pet-care-hurricane.html"),
    ]),
    ("Contact", "contact.html", []),
]

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
def render_nav():
    items = []
    for label, href, children in NAV:
        if children:
            kids = "\n".join(
                f'        <a href="{c_href}">{c_label}</a>'
                for c_label, c_href in children
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
      <img src="assets/img/logo.png" alt="National Humane Society" width="186" height="55" style="display:block; height:48px; width:auto">
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
    return """<footer class="site-footer">
  <div class="container">
    <div class="footer-trust">
      <div class="badge"><strong>Charity Navigator</strong>Rating placeholder</div>
      <div class="badge"><strong>Candid / GuideStar</strong>Seal placeholder</div>
      <div class="badge"><strong>BBB Wise Giving</strong>Accreditation placeholder</div>
      <div class="badge"><strong>EIN</strong>XX-XXXXXXX</div>
    </div>
    <div class="footer-grid">
      <div>
        <div class="footer-brand">National Humane Society</div>
        <p style="font-size:.9rem; color:rgba(255,255,255,.7)">A 501(c)(3) animal welfare organization advocating for, rescuing, and protecting animals across the United States.</p>
        <p style="font-size:.85rem; margin-top:1rem">
          <strong style="color:#fff">Contact</strong><br>
          Customer Service: 877-285-0710<br>
          <a href="contact.html">Send a message</a>
        </p>
      </div>
      <div>
        <h4>Our Mission</h4>
        <ul>
          <li><a href="about.html">About</a></li>
          <li><a href="programs.html">Programs</a></li>
          <li><a href="impact.html">Impact &amp; Outcomes</a></li>
          <li><a href="shelter-partners.html">Shelter Partners</a></li>
          <li><a href="financial-transparency.html">Financial Transparency</a></li>
        </ul>
      </div>
      <div>
        <h4>Sweepstakes</h4>
        <ul>
          <li><a href="sweepstakes.html">Active Sweepstakes</a></li>
          <li><a href="raffle-plus.html">Raffle Plus</a></li>
          <li><a href="how-it-works.html">How It Works</a></li>
          <li><a href="faq.html">FAQ</a></li>
          <li><a href="rules.html">Rules</a></li>
          <li><a href="previous-winners.html">Previous Winners</a></li>
        </ul>
      </div>
      <div>
        <h4>Get Involved</h4>
        <ul>
          <li><a href="donate.html">Donate</a></li>
          <li><a href="monthly-giving.html">Monthly Giving</a></li>
          <li><a href="wills-estates.html">Wills &amp; Estates</a></li>
          <li><a href="volunteer.html">Volunteer</a></li>
          <li><a href="corporate-partners.html">Corporate Partners</a></li>
        </ul>
      </div>
      <div>
        <h4>Resources</h4>
        <ul>
          <li><a href="blog.html">Blog</a></li>
          <li><a href="videos.html">Videos</a></li>
          <li><a href="pet-care-cats.html">Pet Care: Cats</a></li>
          <li><a href="pet-care-dogs.html">Pet Care: Dogs</a></li>
          <li><a href="pet-care-hurricane.html">Hurricane Prep</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div>© 2026 National Humane Society. All rights reserved.</div>
      <div>
        <a href="#">Privacy Policy</a>
        <a href="#">Donor Privacy</a>
        <a href="#">State Registrations</a>
        <a href="#">IRS Form 990</a>
      </div>
    </div>
  </div>
</footer>"""


def page(title, slug, body, description=None):
    """Returns the file (slug, html-string) for a single page."""
    desc = description or f"{title} — National Humane Society"
    html = f"""<!doctype html>
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
<body>
{render_header()}
<main>
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
    return slug, html


# ---------------------------------------------------------------------------
# Reusable content blocks
# ---------------------------------------------------------------------------
def page_hero(title, lead, breadcrumb_label):
    return f"""
<section class="page-hero">
  <div class="container">
    <div class="breadcrumb"><a href="index.html">Home</a> &nbsp;/&nbsp; {breadcrumb_label}</div>
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>
"""


PROCEEDS_PANEL = """
<aside class="proceeds-panel">
  <h4>Where your entry goes</h4>
  <p style="margin:0">A clearly disclosed percentage of net proceeds from every sweepstakes entry funds our four mission programs and named shelter-partner grants. <a href="financial-transparency.html">See the breakdown</a>.</p>
</aside>
"""

NEWSLETTER_BLOCK = """
<section class="section">
  <div class="container-narrow">
    <div class="newsletter">
      <p class="eyebrow" style="color:var(--color-yellow)">Stay in touch</p>
      <h2>Get rescue stories in your inbox.</h2>
      <p style="opacity:.85">One email a month — adoption success stories, sweepstakes winners, and the impact of your support. Unsubscribe anytime.</p>
      <form onsubmit="event.preventDefault(); alert('Preview only — newsletter capture goes here.');">
        <input type="email" placeholder="you@example.com" required>
        <button class="btn btn-yellow" type="submit">Subscribe</button>
      </form>
    </div>
  </div>
</section>
"""


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

# --- HOMEPAGE ---------------------------------------------------------------
HOME_BODY = """
<section class="hero-video">
  <video autoplay muted loop playsinline preload="metadata"
         poster="assets/video/humane-mission-poster.jpg">
    <source src="assets/video/humane-mission.webm" type="video/webm">
    <source src="assets/video/humane-mission.mp4" type="video/mp4">
  </video>
  <div class="container hero-content">
    <p class="eyebrow">A 501(c)(3) animal welfare organization</p>
    <h1>Working to end suffering for all animals.</h1>
    <p class="lead">We rescue, advocate, educate, and promote compassion for animals across the United States — funded by donors and our nationally-known sweepstakes program.</p>
    <div style="display:flex; gap:12px; flex-wrap:wrap; margin-top:var(--space-5)">
      <a class="btn btn-primary btn-lg" href="donate.html">Donate Now</a>
      <a class="btn btn-ghost btn-lg" href="about.html">Our Mission</a>
    </div>
  </div>
</section>

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

<!-- Trust strip — audit Section 3.4 -->
<section class="trust-strip">
  <div class="container trust-grid">
    <div class="trust-badge"><strong>Charity Navigator</strong>Rating placeholder</div>
    <div class="trust-badge"><strong>Candid Platinum</strong>Seal placeholder</div>
    <div class="trust-badge"><strong>BBB Wise Giving</strong>Accreditation placeholder</div>
    <div class="trust-badge"><strong>EIN XX-XXXXXXX</strong>IRS-verified 501(c)(3)</div>
  </div>
</section>

<!-- Mission pillars (verbatim from current /about page) -->
<section class="section">
  <div class="container">
    <div class="text-center" style="max-width:680px; margin:0 auto var(--space-7)">
      <p class="eyebrow">Our Mission</p>
      <h2>Four pillars guide every dollar we receive.</h2>
    </div>
    <div class="grid grid-4">
      <div class="pillar">
        <div class="pillar-num">01</div>
        <h3>Rescuing &amp; Protecting</h3>
        <p>Providing lifesaving care, rehabilitation, and support to vulnerable animals, while working to ensure their long-term well-being and quality of life.</p>
      </div>
      <div class="pillar">
        <div class="pillar-num">02</div>
        <h3>Advocating for Change</h3>
        <p>Confronting cruelty at its root through research, policy reform, and systemic advocacy, especially where animals face the greatest and most entrenched harm.</p>
      </div>
      <div class="pillar">
        <div class="pillar-num">03</div>
        <h3>Educating Communities</h3>
        <p>Helping people understand the issues animals face and encouraging responsible choices, including spaying and neutering, to prevent needless suffering.</p>
      </div>
      <div class="pillar">
        <div class="pillar-num">04</div>
        <h3>Promoting Compassion</h3>
        <p>Leading with respect and compassion as we work alongside our partners, supporters, and communities to build a more humane future for the animals.</p>
      </div>
    </div>
  </div>
</section>

<!-- Inline donate widget — audit Section 3.1 -->
<section class="section section-soft">
  <div class="container grid grid-2" style="align-items:center">
    <div>
      <p class="eyebrow">Make an immediate impact</p>
      <h2>$25 funds one spay/neuter procedure.</h2>
      <p>Direct, recurring support is the single most effective way to fund the four mission pillars. Choose an amount, choose monthly or one-time — that's it.</p>
      <ul class="list-check">
        <li>100% tax-deductible</li>
        <li>Cancel monthly giving anytime</li>
        <li>Receipts emailed automatically</li>
      </ul>
      <a class="btn btn-secondary" href="donate.html">Other ways to give →</a>
    </div>
    <div class="donate-widget">
      <h3>Your donation, your impact</h3>
      <p style="color:var(--color-text-muted); font-size:.95rem">Preview only — connects to GiveWP / Stripe in production.</p>
      <div class="donate-toggle">
        <button class="is-active">Monthly</button>
        <button>One-time</button>
      </div>
      <div class="amount-grid">
        <button class="amount-btn">$10<small>1 meal/day</small></button>
        <button class="amount-btn is-active">$25<small>1 spay/neuter</small></button>
        <button class="amount-btn">$50<small>vet checkup</small></button>
        <button class="amount-btn">$100<small>shelter grant</small></button>
        <button class="amount-btn">$250<small>rescue transport</small></button>
        <button class="amount-btn">Other</button>
      </div>
      <button class="btn btn-primary" style="width:100%; justify-content:center">Donate $25 monthly →</button>
    </div>
  </div>
</section>

<!-- Sweepstakes — single section, links to hub -->
<section class="section">
  <div class="container">
    <div style="display:flex; justify-content:space-between; align-items:end; flex-wrap:wrap; gap:16px; margin-bottom:var(--space-6)">
      <div>
        <p class="eyebrow">Fundraising sweepstakes</p>
        <h2>Enter to win. Help fund the mission.</h2>
        <p class="lead" style="margin:0">A portion of every entry funds our shelter-partner grants and rescue programs. <a href="how-it-works.html">How it works →</a></p>
      </div>
      <a class="btn btn-secondary" href="sweepstakes.html">View all active sweepstakes →</a>
    </div>
    <div class="grid grid-3">
      <div class="prize-card">
        <div class="prize-image" style="background-image:url('assets/img/prize-porsche-911.webp')"></div>
        <div class="prize-body">
          <div class="prize-meta"><span>Drawing · Sept 2026</span><span class="prize-status">Active</span></div>
          <h3>New Porsche 911 Carrera</h3>
          <p style="color:var(--color-text-muted); margin-bottom:16px">Or take $[XXX,XXX] cash. Entries from $[X].</p>
          <a class="btn btn-primary btn-sm" href="sweepstakes-detail.html">Enter Now</a>
        </div>
      </div>
      <div class="prize-card">
        <div class="prize-image" style="background-image:url('assets/img/prize-tesla-s.webp')"></div>
        <div class="prize-body">
          <div class="prize-meta"><span>Drawing · Oct 2026</span><span class="prize-status">Active</span></div>
          <h3>Tesla Model S Plaid</h3>
          <p style="color:var(--color-text-muted); margin-bottom:16px">Or take $[XXX,XXX] cash. Entries from $[X].</p>
          <a class="btn btn-primary btn-sm" href="sweepstakes-detail.html">Enter Now</a>
        </div>
      </div>
      <div class="prize-card">
        <div class="prize-image" style="background-image:url('assets/img/prize-corvette-classic.jpg')"></div>
        <div class="prize-body">
          <div class="prize-meta"><span>Drawing · Nov 2026</span><span class="prize-status">Active</span></div>
          <h3>Classic Corvette Stingray</h3>
          <p style="color:var(--color-text-muted); margin-bottom:16px">Or take $[XX,XXX] cash. Entries from $[X].</p>
          <a class="btn btn-primary btn-sm" href="sweepstakes-detail.html">Enter Now</a>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Impact -->
<section class="section section-navy">
  <div class="container">
    <div class="text-center" style="max-width:680px; margin:0 auto var(--space-7)">
      <p class="eyebrow">The problem</p>
      <h2>4 to 6 million animals are euthanized in U.S. shelters every year.</h2>
      <p class="lead" style="margin:0 auto">Of the [7 million] dogs and cats that enter shelters annually, only about half find homes. We're working to change that.</p>
    </div>
    <div class="grid grid-3">
      <div class="stat-block coral">
        <span class="num">[1,234]</span>
        <span class="label">Animals placed in homes (2025)</span>
      </div>
      <div class="stat-block">
        <span class="num">[$1.2M]</span>
        <span class="label">Granted to shelter partners</span>
      </div>
      <div class="stat-block coral">
        <span class="num">[123]</span>
        <span class="label">Active shelter partners</span>
      </div>
    </div>
    <div class="text-center" style="margin-top:var(--space-6)">
      <a class="btn btn-yellow" href="impact.html">See full impact report →</a>
    </div>
  </div>
</section>

<!-- Stories -->
<section class="section">
  <div class="container">
    <div class="text-center" style="max-width:680px; margin:0 auto var(--space-6)">
      <p class="eyebrow">Real animals · Real outcomes</p>
      <h2>Stories from our shelter partners.</h2>
    </div>
    <div class="grid grid-3">
      <div class="story-card">
        <div class="story-image" style="background-image:url('assets/img/animal-winterpup.jpg')"></div>
        <div class="story-body">
          <blockquote>“[Placeholder — shelter director quote about how a grant funded the medical care that let them save XX dogs from a hoarding case.]”</blockquote>
          <cite>[Director Name] · [Shelter Name], [State]</cite>
        </div>
      </div>
      <div class="story-card">
        <div class="story-image" style="background-image:url('assets/img/animal-cat.jpg')"></div>
        <div class="story-body">
          <blockquote>“[Placeholder — adopter quote about meeting their rescue dog through a funded shelter program.]”</blockquote>
          <cite>[Adopter Name] · Adopted [Pet Name], 2025</cite>
        </div>
      </div>
      <div class="story-card">
        <div class="story-image" style="background-image:url('assets/img/animal-vet-exam.jpg')"></div>
        <div class="story-body">
          <blockquote>“[Placeholder — donor quote about why they give monthly and what it's meant to them.]”</blockquote>
          <cite>[Donor Name] · Monthly donor since [year]</cite>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Get involved -->
<section class="section section-soft">
  <div class="container">
    <div class="text-center" style="max-width:680px; margin:0 auto var(--space-6)">
      <p class="eyebrow">Get involved</p>
      <h2>Five ways to help, beyond a donation.</h2>
    </div>
    <div class="grid grid-3">
      <div class="card">
        <div class="card-icon">$</div>
        <h3>Monthly giving</h3>
        <p>Predictable funding lets us commit to multi-year shelter partnerships.</p>
        <a href="monthly-giving.html">Become a monthly donor →</a>
      </div>
      <div class="card">
        <div class="card-icon">♥</div>
        <h3>Volunteer</h3>
        <p>From shelter shifts to remote skills-based volunteering.</p>
        <a href="volunteer.html">Find a volunteer role →</a>
      </div>
      <div class="card">
        <div class="card-icon">📜</div>
        <h3>Wills &amp; estates</h3>
        <p>Leave a legacy that protects animals for generations.</p>
        <a href="wills-estates.html">Planned giving →</a>
      </div>
      <div class="card">
        <div class="card-icon">🏢</div>
        <h3>Corporate partners</h3>
        <p>Workplace giving, sponsorships, and matching gifts.</p>
        <a href="corporate-partners.html">Partner with us →</a>
      </div>
      <div class="card">
        <div class="card-icon">★</div>
        <h3>Sweepstakes entries</h3>
        <p>A portion of every entry directly funds the mission.</p>
        <a href="sweepstakes.html">View active sweepstakes →</a>
      </div>
      <div class="card">
        <div class="card-icon">📨</div>
        <h3>Spread the word</h3>
        <p>Share an animal story or a sweepstakes entry with someone you love.</p>
        <a href="contact.html">Get a media kit →</a>
      </div>
    </div>
  </div>
</section>

<!-- Latest from blog -->
<section class="section">
  <div class="container">
    <div style="display:flex; justify-content:space-between; align-items:end; flex-wrap:wrap; gap:16px; margin-bottom:var(--space-6)">
      <div>
        <p class="eyebrow">Resources</p>
        <h2>From the blog.</h2>
      </div>
      <a class="btn btn-secondary" href="blog.html">All articles →</a>
    </div>
    <div class="grid grid-3">
      <article class="post-card">
        <div class="post-image" style="background-image:url('assets/img/animal-vet-exam-2.jpg')"></div>
        <div class="post-body">
          <div class="post-tag">Donor education</div>
          <h3><a href="blog-post.html">How your $10 monthly donation really helps shelter animals</a></h3>
          <p style="color:var(--color-text-muted)">A breakdown of where every dollar goes — and the math behind why monthly giving compounds.</p>
        </div>
      </article>
      <article class="post-card">
        <div class="post-image" style="background-image:url('assets/img/animal-first-aid-1.jpg')"></div>
        <div class="post-body">
          <div class="post-tag">Volunteer guide</div>
          <h3><a href="blog-post.html">How to volunteer at a local animal shelter</a></h3>
          <p style="color:var(--color-text-muted)">Six ways to start — even if you've never set foot in a shelter before.</p>
        </div>
      </article>
      <article class="post-card">
        <div class="post-image" style="background-image:url('assets/img/animal-lost-dog.jpg')"></div>
        <div class="post-body">
          <div class="post-tag">Pet care</div>
          <h3><a href="blog-post.html">Hurricane prep checklist for pet owners</a></h3>
          <p style="color:var(--color-text-muted)">Evacuation kits, microchipping, and the 72-hour plan every household needs.</p>
        </div>
      </article>
    </div>
  </div>
</section>

""" + NEWSLETTER_BLOCK


# --- ABOUT ------------------------------------------------------------------
ABOUT_BODY = page_hero(
    "Our Mission",
    "We are an animal welfare organization working to end suffering for all animals — through rescue, advocacy, education, and a commitment to compassion.",
    "Our Mission",
) + """
<section class="section">
  <div class="container-narrow">
    <p class="lead">For decades, the National Humane Society has stood with shelters, humane societies, and rescue groups across the United States. We're funded by individual donors and a national sweepstakes program — and every dollar of net proceeds is committed to our four mission pillars.</p>
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <p class="eyebrow text-center">The four pillars</p>
    <h2 class="text-center" style="margin-bottom:var(--space-7)">Every program traces back to one of these four commitments.</h2>
    <div class="grid grid-2">
      <div class="pillar">
        <div class="pillar-num">01</div>
        <h3>Rescuing and Protecting Animals in Need</h3>
        <p>Providing lifesaving care, rehabilitation, and support to vulnerable animals, while working to ensure their long-term well-being and quality of life.</p>
      </div>
      <div class="pillar">
        <div class="pillar-num">02</div>
        <h3>Advocating for Lasting Change</h3>
        <p>Confronting cruelty at its root through research, policy reform, and systemic advocacy, especially where animals face the greatest and most entrenched harm.</p>
      </div>
      <div class="pillar">
        <div class="pillar-num">03</div>
        <h3>Educating and Empowering Communities</h3>
        <p>Helping people understand the issues animals face and encouraging responsible choices, including spaying and neutering, to prevent needless suffering and save lives.</p>
      </div>
      <div class="pillar">
        <div class="pillar-num">04</div>
        <h3>Promoting Compassion and Respect</h3>
        <p>Leading with respect and compassion as we work alongside our partners, supporters, and communities to build a more humane future for the animals.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <p class="eyebrow text-center">Leadership</p>
    <h2 class="text-center" style="margin-bottom:var(--space-7)">Board of directors &amp; executive team.</h2>
    <div class="grid grid-4">
      <div class="card text-center">
        <div style="width:120px; height:120px; margin:0 auto var(--space-4); border-radius:50%; background:var(--color-navy-50)"></div>
        <h3>[Name Placeholder]</h3>
        <p style="color:var(--color-text-muted); font-size:.9rem">Executive Director</p>
      </div>
      <div class="card text-center">
        <div style="width:120px; height:120px; margin:0 auto var(--space-4); border-radius:50%; background:var(--color-navy-50)"></div>
        <h3>[Name Placeholder]</h3>
        <p style="color:var(--color-text-muted); font-size:.9rem">Board Chair</p>
      </div>
      <div class="card text-center">
        <div style="width:120px; height:120px; margin:0 auto var(--space-4); border-radius:50%; background:var(--color-navy-50)"></div>
        <h3>[Name Placeholder]</h3>
        <p style="color:var(--color-text-muted); font-size:.9rem">Director of Programs</p>
      </div>
      <div class="card text-center">
        <div style="width:120px; height:120px; margin:0 auto var(--space-4); border-radius:50%; background:var(--color-navy-50)"></div>
        <h3>[Name Placeholder]</h3>
        <p style="color:var(--color-text-muted); font-size:.9rem">Director of Development</p>
      </div>
    </div>
    <p class="text-center" style="margin-top:var(--space-6)"><a href="contact.html">Full board roster &amp; bios →</a></p>
  </div>
</section>

<section class="section section-navy">
  <div class="container-narrow text-center">
    <p class="eyebrow">A 501(c)(3) nonprofit</p>
    <h2>Verifiable, transparent, accountable.</h2>
    <p class="lead" style="margin:0 auto var(--space-5)">EIN XX-XXXXXXX · Registered for charitable solicitation in [XX] states · Form 990 publicly filed annually.</p>
    <a class="btn btn-yellow" href="financial-transparency.html">View financial transparency →</a>
  </div>
</section>
"""

# --- PROGRAMS ---------------------------------------------------------------
PROGRAMS_BODY = page_hero(
    "Programs",
    "How we translate the four mission pillars into specific programs — funded by your donations and sweepstakes entries.",
    "Programs",
) + """
<section class="section">
  <div class="container grid grid-2" style="gap:var(--space-7)">
    <div class="card">
      <div class="card-icon">🐾</div>
      <h3>Shelter Partner Grant Program</h3>
      <p>Direct grants to vetted shelter partners for medical care, spay/neuter, transport, and emergency response. [Placeholder description of grant criteria, application cycle, and 2025 totals.]</p>
      <a href="shelter-partners.html">See partner directory →</a>
    </div>
    <div class="card">
      <div class="card-icon">🏥</div>
      <h3>Spay &amp; Neuter Initiative</h3>
      <p>Funds low-cost and free spay/neuter procedures through clinic partnerships in underserved areas. [Placeholder — XX procedures funded in 2025.]</p>
      <a href="impact.html">Program impact →</a>
    </div>
    <div class="card">
      <div class="card-icon">🚐</div>
      <h3>Emergency &amp; Disaster Response</h3>
      <p>Rapid funding and supplies for shelters and rescue groups responding to hurricanes, wildfires, hoarding cases, and large-scale neglect. [Placeholder — XX deployments in 2025.]</p>
      <a href="pet-care-hurricane.html">Disaster prep resources →</a>
    </div>
    <div class="card">
      <div class="card-icon">🎓</div>
      <h3>Education &amp; Advocacy</h3>
      <p>Public education campaigns, policy advocacy at state and federal levels, and resources for communities working to advance animal welfare laws.</p>
      <a href="blog.html">Educational articles →</a>
    </div>
  </div>
</section>
""" + NEWSLETTER_BLOCK

# --- IMPACT -----------------------------------------------------------------
IMPACT_BODY = page_hero(
    "Impact &amp; Outcomes",
    "Annual numbers, multi-year trends, and the specific outcomes your support makes possible. All figures audited annually.",
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
    <p class="lead">Animals placed in homes through funded shelter-partner programs.</p>
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
    <p style="margin-top:var(--space-5)"><a class="btn btn-secondary" href="financial-transparency.html">View audited financials →</a></p>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="text-center" style="margin-bottom:var(--space-6)">Outcome stories from 2025.</h2>
    <div class="grid grid-3">
      <div class="story-card">
        <div class="story-image" style="background-image:url('assets/img/animal-first-aid-2.jpg')"></div>
        <div class="story-body">
          <blockquote>“[Placeholder narrative — a hoarding case in [State] where a grant funded medical care for [XX] dogs.]”</blockquote>
          <cite>[Shelter Name]</cite>
        </div>
      </div>
      <div class="story-card">
        <div class="story-image" style="background-image:url('assets/img/animal-lost-dog.jpg')"></div>
        <div class="story-body">
          <blockquote>“[Placeholder narrative — hurricane response funding evacuation transport for [XXX] animals.]”</blockquote>
          <cite>[Shelter Name]</cite>
        </div>
      </div>
      <div class="story-card">
        <div class="story-image" style="background-image:url('assets/img/animal-heartworm.jpg')"></div>
        <div class="story-body">
          <blockquote>“[Placeholder narrative — community spay/neuter clinic preventing [X,XXX] unwanted litters.]”</blockquote>
          <cite>[Clinic Name]</cite>
        </div>
      </div>
    </div>
  </div>
</section>
"""

# --- SHELTER PARTNERS -------------------------------------------------------
SHELTER_BODY = page_hero(
    "Shelter Partners",
    "Every grant goes to a vetted, named shelter partner. The directory below lists every organization we funded in 2025 — searchable by state.",
    "Shelter Partners",
) + """
<section class="section">
  <div class="container">
    <div class="grid grid-2" style="margin-bottom:var(--space-6)">
      <div class="form-row">
        <label>Search by name or city</label>
        <input type="text" placeholder="e.g., Austin Pets Alive">
      </div>
      <div class="form-row">
        <label>Filter by state</label>
        <select>
          <option>All states</option>
          <option>Alabama</option><option>Alaska</option><option>...</option>
        </select>
      </div>
    </div>
    <table class="table-clean">
      <thead><tr><th>Shelter / Rescue</th><th>City, State</th><th>Focus</th><th>2025 grant</th></tr></thead>
      <tbody>
        <tr><td>[Placeholder Shelter Name]</td><td>[City], [ST]</td><td>Spay/neuter</td><td>$[XX,XXX]</td></tr>
        <tr><td>[Placeholder Rescue Name]</td><td>[City], [ST]</td><td>Medical care</td><td>$[XX,XXX]</td></tr>
        <tr><td>[Placeholder Shelter Name]</td><td>[City], [ST]</td><td>Hurricane response</td><td>$[XX,XXX]</td></tr>
        <tr><td>[Placeholder Shelter Name]</td><td>[City], [ST]</td><td>Adoption events</td><td>$[XX,XXX]</td></tr>
        <tr><td>[Placeholder Rescue Name]</td><td>[City], [ST]</td><td>Foster network</td><td>$[XX,XXX]</td></tr>
      </tbody>
    </table>
    <p class="text-center" style="margin-top:var(--space-5); color:var(--color-text-muted)">[Replace with full directory of 2025 shelter partners — currently the live site names zero. This page is the highest-impact addition the audit identified.]</p>
  </div>
</section>

<section class="section section-soft">
  <div class="container-narrow text-center">
    <p class="eyebrow">For shelters</p>
    <h2>Apply for a grant.</h2>
    <p class="lead">Shelter partners are vetted annually. Grant applications open quarterly.</p>
    <a class="btn btn-primary" href="contact.html">Start an application →</a>
  </div>
</section>
"""

# --- FINANCIAL TRANSPARENCY -------------------------------------------------
FINANCIAL_BODY = page_hero(
    "Financial Transparency",
    "We publish our audited financials, IRS Form 990, and a clear breakdown of how every dollar is spent.",
    "Financial Transparency",
) + """
<section class="section">
  <div class="container-narrow">
    <h2>Where every dollar goes (2025).</h2>
    <p class="lead">Independently audited. Form 990 publicly filed.</p>
    <div class="expense-bar">
      <span style="background:var(--color-navy); flex: 78">78% Programs</span>
      <span style="background:var(--color-coral); flex: 14">14% Fundraising</span>
      <span style="background:var(--color-text-muted); flex: 8">8% Admin</span>
    </div>
    <p style="color:var(--color-text-muted); font-size:.9rem">Percentages are placeholders. Replace with figures from the most recent audited financial statement.</p>

    <h3 style="margin-top:var(--space-7)">Documents</h3>
    <ul class="list-check">
      <li><a href="#">2025 Annual Report (PDF) — placeholder link</a></li>
      <li><a href="#">2024 Audited Financial Statements (PDF) — placeholder link</a></li>
      <li><a href="#">IRS Form 990 (most recent) — placeholder link</a></li>
      <li><a href="#">501(c)(3) Determination Letter — placeholder link</a></li>
      <li><a href="#">State charitable solicitation registrations — placeholder link</a></li>
    </ul>

    <h3 style="margin-top:var(--space-7)">Third-party ratings</h3>
    <div class="grid grid-3" style="margin-top:var(--space-5)">
      <div class="card text-center">
        <strong>Charity Navigator</strong>
        <p style="margin-top:8px; color:var(--color-text-muted)">Rating placeholder</p>
        <a href="#">View profile →</a>
      </div>
      <div class="card text-center">
        <strong>Candid (GuideStar)</strong>
        <p style="margin-top:8px; color:var(--color-text-muted)">Seal placeholder</p>
        <a href="#">View profile →</a>
      </div>
      <div class="card text-center">
        <strong>BBB Wise Giving</strong>
        <p style="margin-top:8px; color:var(--color-text-muted)">Accreditation placeholder</p>
        <a href="#">View profile →</a>
      </div>
    </div>
  </div>
</section>
"""

# --- SWEEPSTAKES HUB --------------------------------------------------------
SWEEPSTAKES_BODY = page_hero(
    "Sweepstakes",
    "A portion of every entry funds our shelter-partner grants and rescue programs. Browse active sweepstakes below.",
    "Sweepstakes",
) + """
<section class="section">
  <div class="container">
    """ + PROCEEDS_PANEL + """
    <div class="grid grid-3" style="margin-top:var(--space-6)">
      <div class="prize-card">
        <div class="prize-image" style="background-image:url('assets/img/prize-porsche-911.webp')"></div>
        <div class="prize-body">
          <div class="prize-meta"><span>Drawing · Sept 2026</span><span class="prize-status">Active</span></div>
          <h3>New Porsche 911 Carrera</h3>
          <p style="color:var(--color-text-muted); margin-bottom:16px">Or take $[XXX,XXX] cash. Entries from $[X].</p>
          <a class="btn btn-primary btn-sm" href="sweepstakes-detail.html">Enter Now</a>
        </div>
      </div>
      <div class="prize-card">
        <div class="prize-image" style="background-image:url('assets/img/prize-porsche-1965.jpg')"></div>
        <div class="prize-body">
          <div class="prize-meta"><span>Drawing · Sept 2026</span><span class="prize-status">Active</span></div>
          <h3>1965 Porsche 356</h3>
          <p style="color:var(--color-text-muted); margin-bottom:16px">Or take $[XXX,XXX] cash. Entries from $[X].</p>
          <a class="btn btn-primary btn-sm" href="sweepstakes-detail.html">Enter Now</a>
        </div>
      </div>
      <div class="prize-card">
        <div class="prize-image" style="background-image:url('assets/img/prize-tesla-s.webp')"></div>
        <div class="prize-body">
          <div class="prize-meta"><span>Drawing · Oct 2026</span><span class="prize-status">Active</span></div>
          <h3>Tesla Model S Plaid</h3>
          <p style="color:var(--color-text-muted); margin-bottom:16px">Or take $[XXX,XXX] cash. Entries from $[X].</p>
          <a class="btn btn-primary btn-sm" href="sweepstakes-detail.html">Enter Now</a>
        </div>
      </div>
      <div class="prize-card">
        <div class="prize-image" style="background-image:url('assets/img/prize-corvette-new.jpg')"></div>
        <div class="prize-body">
          <div class="prize-meta"><span>Drawing · Oct 2026</span><span class="prize-status">Active</span></div>
          <h3>New Corvette Stingray</h3>
          <p style="color:var(--color-text-muted); margin-bottom:16px">Or take $[XX,XXX] cash. Entries from $[X].</p>
          <a class="btn btn-primary btn-sm" href="sweepstakes-detail.html">Enter Now</a>
        </div>
      </div>
      <div class="prize-card">
        <div class="prize-image" style="background-image:url('assets/img/prize-corvette-classic.jpg')"></div>
        <div class="prize-body">
          <div class="prize-meta"><span>Drawing · Nov 2026</span><span class="prize-status">Active</span></div>
          <h3>Classic Corvette Stingray</h3>
          <p style="color:var(--color-text-muted); margin-bottom:16px">Or take $[XX,XXX] cash. Entries from $[X].</p>
          <a class="btn btn-primary btn-sm" href="sweepstakes-detail.html">Enter Now</a>
        </div>
      </div>
      <div class="prize-card">
        <div class="prize-image" style="background-image:url('assets/img/prize-rivian.jpg')"></div>
        <div class="prize-body">
          <div class="prize-meta"><span>Drawing · Nov 2026</span><span class="prize-status">Active</span></div>
          <h3>EV Truck Bundle (Rivian + Lightning)</h3>
          <p style="color:var(--color-text-muted); margin-bottom:16px">Or take $[XXX,XXX] cash. Entries from $[X].</p>
          <a class="btn btn-primary btn-sm" href="sweepstakes-detail.html">Enter Now</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container-narrow text-center">
    <p class="eyebrow">Open ended</p>
    <h2>Raffle Plus — entries any time, drawings every month.</h2>
    <p class="lead">$[XX] in monthly cash prizes. Subscribe and you're entered every month automatically.</p>
    <a class="btn btn-primary" href="raffle-plus.html">Learn about Raffle Plus →</a>
  </div>
</section>
"""

# --- SWEEPSTAKES DETAIL (template) ------------------------------------------
SWEEPSTAKES_DETAIL_BODY = """
<section class="page-hero">
  <div class="container">
    <div class="breadcrumb"><a href="index.html">Home</a> &nbsp;/&nbsp; <a href="sweepstakes.html">Sweepstakes</a> &nbsp;/&nbsp; New Porsche 911</div>
    <div class="grid grid-2" style="align-items:center">
      <div>
        <p class="eyebrow">Active sweepstakes · Drawing September 30, 2026</p>
        <h1>New Porsche 911 Carrera</h1>
        <p class="lead">Or take $[XXX,XXX] cash. Entries start at $[X]. Every entry funds shelter-partner grants.</p>
      </div>
      <div class="prize-image" style="aspect-ratio:16/10; border-radius:var(--radius-lg); background-image:url('assets/img/prize-porsche-911.webp'); background-size:cover; background-position:center"></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container grid grid-2">
    <div>
      <h2>Enter the sweepstakes.</h2>
      <p>Preview only — production form posts to Gravity Forms with state/age validation, integrated with the payment processor and email tools.</p>
      <form class="form-grid" onsubmit="event.preventDefault(); alert('Preview only — entry form');">
        <div class="grid grid-2">
          <div class="form-row"><label>First name</label><input type="text" required></div>
          <div class="form-row"><label>Last name</label><input type="text" required></div>
        </div>
        <div class="form-row"><label>Email</label><input type="email" required></div>
        <div class="form-row"><label>State</label>
          <select required><option value="">Select state</option><option>California</option><option>Texas</option><option>New York</option></select>
        </div>
        <div class="form-row"><label>Number of entries</label>
          <select><option>1 entry · $[X]</option><option>10 entries · $[XX]</option><option>50 entries · $[XX]</option></select>
        </div>
        <div class="form-row" style="font-size:.85rem; color:var(--color-text-muted)">
          <label style="display:flex; gap:8px; text-transform:none; letter-spacing:0; font-family:var(--font-body); font-weight:400; font-size:.9rem">
            <input type="checkbox" required>
            I am 18+, a U.S. resident, and have read the <a href="rules.html">Official Rules</a>.
          </label>
        </div>
        <button type="submit" class="btn btn-primary btn-lg">Submit Entry →</button>
      </form>
    </div>
    <div>
      """ + PROCEEDS_PANEL + """
      <div style="margin-top:var(--space-5)">
        <h3>Prize details</h3>
        <ul class="list-check">
          <li>2026 Porsche 911 Carrera — base trim</li>
          <li>Cash alternative: $[XXX,XXX]</li>
          <li>Drawing: September 30, 2026</li>
          <li>Winner notified by phone &amp; email within 7 days</li>
          <li>Free Alternative Method of Entry available — see <a href="rules.html">Rules</a></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container-narrow">
    <h2 class="text-center">Common questions.</h2>
    <div class="faq-item">
      <h3>Do I have to donate to enter?</h3>
      <p>No. A free Alternative Method of Entry is available by mail and is detailed in the <a href="rules.html">Official Rules</a>.</p>
    </div>
    <div class="faq-item">
      <h3>What percentage of my entry funds animal welfare?</h3>
      <p>[XX]% of net proceeds (after prize cost, fulfillment, and required fees) is granted to shelter partners and mission programs.</p>
    </div>
    <div class="faq-item">
      <h3>Is my entry tax-deductible?</h3>
      <p>Sweepstakes entries are not tax-deductible because the entry includes a chance to win a prize. <a href="donate.html">Tax-deductible donations</a> are made through our donate flow.</p>
    </div>
  </div>
</section>
"""

# --- RAFFLE PLUS ------------------------------------------------------------
RAFFLE_BODY = page_hero(
    "Raffle Plus",
    "A subscription-style sweepstakes — one signup keeps you entered in monthly drawings for cash prizes.",
    "Raffle Plus",
) + """
<section class="section">
  <div class="container grid grid-2" style="align-items:center">
    <div>
      <h2>How Raffle Plus works.</h2>
      <ol style="font-size:1.05rem; line-height:1.8">
        <li>Subscribe at $[XX]/month — one form, one time.</li>
        <li>You're automatically entered in every monthly drawing.</li>
        <li>Cash prizes drawn every month — $[XX,XXX] in total.</li>
        <li>A portion of every monthly subscription funds the mission.</li>
        <li>Cancel anytime.</li>
      </ol>
      <a class="btn btn-primary btn-lg" href="#">Subscribe — $[XX]/month</a>
    </div>
    """ + PROCEEDS_PANEL + """
  </div>
</section>
"""

# --- HOW IT WORKS -----------------------------------------------------------
HOW_IT_WORKS_BODY = page_hero(
    "How Sweepstakes Work",
    "Sweepstakes-as-fundraising is a legitimate, regulated nonprofit model. Here's exactly how ours operates.",
    "How It Works",
) + """
<section class="section">
  <div class="container-narrow">
    <h2>1. You enter.</h2>
    <p>Choose a prize, choose your entry tier (more entries = more chances to win). Or use the free Alternative Method of Entry by mail. Either way, you have an equal chance per entry.</p>

    <h2>2. We fund the mission.</h2>
    <p>Net proceeds — after the cost of the prize, payment processing, legal, and bonding fees — are granted to our shelter partners and used to fund the four mission pillars. The exact percentage is published on each prize page and in our <a href="financial-transparency.html">audited financials</a>.</p>

    <h2>3. We draw a winner.</h2>
    <p>Drawings are conducted by a licensed third-party administrator on the date listed on each prize page. Winners are contacted by phone and email within 7 days.</p>

    <h2>4. The winner takes the prize — or cash.</h2>
    <p>Every prize has a published cash alternative. Winners are responsible for taxes; we provide IRS Form W-2G when required.</p>

    <a class="btn btn-secondary" href="rules.html">Read the Official Rules →</a>
  </div>
</section>
"""

# --- FAQ --------------------------------------------------------------------
FAQ_BODY = page_hero(
    "Frequently Asked Questions",
    "Everything you might want to know about donations, sweepstakes entries, and how the National Humane Society operates.",
    "FAQ",
) + """
<section class="section">
  <div class="container-narrow">
    <h2>Donations</h2>
    <div class="faq-item">
      <h3>Is my donation tax-deductible?</h3>
      <p>Yes. We are a registered 501(c)(3) (EIN XX-XXXXXXX). You'll receive a receipt by email immediately and a year-end summary in January.</p>
    </div>
    <div class="faq-item">
      <h3>Where does my donation go?</h3>
      <p>Approximately [78]% of every dollar funds programs (shelter partner grants, spay/neuter, disaster response, education). See the <a href="financial-transparency.html">full breakdown</a>.</p>
    </div>
    <div class="faq-item">
      <h3>Can I cancel monthly giving?</h3>
      <p>Anytime, in one click, from your donor account. Or email us — we respond within one business day.</p>
    </div>

    <h2 style="margin-top:var(--space-7)">Sweepstakes</h2>
    <div class="faq-item">
      <h3>Do I have to donate to enter?</h3>
      <p>No. A free Alternative Method of Entry by mail is available and is described in the <a href="rules.html">Official Rules</a>.</p>
    </div>
    <div class="faq-item">
      <h3>Are sweepstakes entries tax-deductible?</h3>
      <p>No. Because an entry includes a chance to win a prize, the IRS does not consider it a tax-deductible donation. To make a deductible gift, use the <a href="donate.html">Donate page</a>.</p>
    </div>
    <div class="faq-item">
      <h3>What states are excluded?</h3>
      <p>Eligibility varies by sweepstakes. Each prize page lists its specific eligibility requirements; full details are in the <a href="rules.html">Official Rules</a>.</p>
    </div>

    <h2 style="margin-top:var(--space-7)">Organization</h2>
    <div class="faq-item">
      <h3>Are you the same as the Humane Society of the United States?</h3>
      <p>No. The National Humane Society is a separate, independent 501(c)(3) organization. [Add disambiguation language as needed.]</p>
    </div>
    <div class="faq-item">
      <h3>How can I verify your nonprofit status?</h3>
      <p>Search our EIN (XX-XXXXXXX) on the <a href="#">IRS Tax Exempt Organization Search</a> or view our profiles on Charity Navigator and Candid (GuideStar).</p>
    </div>
  </div>
</section>
"""

# --- RULES ------------------------------------------------------------------
RULES_BODY = page_hero(
    "Official Sweepstakes Rules",
    "The full legal terms governing every active sweepstakes. Each prize-specific rule set is available on the corresponding prize page.",
    "Rules",
) + """
<section class="section">
  <div class="container-narrow" style="font-size:.95rem; line-height:1.7">
    <h2>1. Eligibility</h2>
    <p>[Placeholder — eligibility language: open to legal U.S. residents 18+, void where prohibited, employees and immediate family excluded, etc.]</p>
    <h2>2. How to Enter</h2>
    <p>[Placeholder — paid entry method and free Alternative Method of Entry by mail.]</p>
    <h2>3. Prize Description</h2>
    <p>[Placeholder — prize specs, ARV, cash alternative.]</p>
    <h2>4. Drawing &amp; Winner Notification</h2>
    <p>[Placeholder — drawing date, method, notification window, claim period.]</p>
    <h2>5. Taxes</h2>
    <p>[Placeholder — winner is responsible for taxes; W-2G issued when required.]</p>
    <h2>6. Publicity Release</h2>
    <p>[Placeholder.]</p>
    <h2>7. Limitation of Liability</h2>
    <p>[Placeholder.]</p>
    <h2>8. Sponsor</h2>
    <p>National Humane Society, [Address], EIN XX-XXXXXXX.</p>
  </div>
</section>
"""

# --- PREVIOUS WINNERS -------------------------------------------------------
WINNERS_BODY = page_hero(
    "Previous Winners",
    "Real winners, real prizes. Every drawing is conducted by a licensed third-party administrator.",
    "Previous Winners",
) + """
<section class="section">
  <div class="container">
    <div class="grid grid-3">
      <div class="story-card">
        <div class="story-image" style="background-image:url('assets/img/winner-gonzo.jpg')"></div>
        <div class="story-body">
          <blockquote>“[Placeholder winner quote — real photo from the live site.]”</blockquote>
          <cite>Gonzo · 2022 Sweepstakes Winner</cite>
        </div>
      </div>
      <div class="story-card">
        <div class="story-image" style="background-image:url('assets/img/winner-nhs-pic.jpg')"></div>
        <div class="story-body">
          <blockquote>“[Placeholder winner quote — real photo from the live site.]”</blockquote>
          <cite>NHS Sweepstakes Winner · 2023</cite>
        </div>
      </div>
      <div class="story-card">
        <div class="story-image" style="background-image:url('assets/img/winner-tolson.jpg')"></div>
        <div class="story-body">
          <blockquote>“[Placeholder winner quote — real photo from the live site.]”</blockquote>
          <cite>T. Olson · Past Winner</cite>
        </div>
      </div>
    </div>
    <div class="grid grid-3" style="margin-top:var(--space-5)">
      <div class="story-card">
        <div class="story-image" style="background-image:url('assets/img/winner-stanley.jpg')"></div>
        <div class="story-body"><cite>T. Stanley · Past Winner</cite></div>
      </div>
      <div class="story-card">
        <div class="story-image" style="background-image:url('assets/img/winner-fleming.jpg')"></div>
        <div class="story-body"><cite>M. Fleming · Past Winner</cite></div>
      </div>
      <div class="story-card">
        <div class="story-image" style="background-image:url('assets/img/winner-malone.jpg')"></div>
        <div class="story-body"><cite>Malone · Past Winner</cite></div>
      </div>
      <div class="story-card">
        <div class="story-image" style="background-image:url('assets/img/winner-berger.jpg')"></div>
        <div class="story-body"><cite>E. Berger · Past Winner</cite></div>
      </div>
      <div class="story-card">
        <div class="story-image" style="background-image:url('assets/img/winner-harting.jpg')"></div>
        <div class="story-body"><cite>Harting · Past Winner</cite></div>
      </div>
      <div class="story-card">
        <div class="story-image" style="background-image:url('assets/img/winner-anne.jpg')"></div>
        <div class="story-body"><cite>Anne · Past Winner</cite></div>
      </div>
    </div>
    <p class="text-center" style="margin-top:var(--space-6)"><a class="btn btn-secondary" href="#">View all past winners (1999–2025) →</a></p>
  </div>
</section>
"""

# --- DONATE -----------------------------------------------------------------
DONATE_BODY = page_hero(
    "Donate",
    "Direct, tax-deductible support for the four mission pillars. Choose monthly or one-time, choose an amount, that's it.",
    "Donate",
) + """
<section class="section">
  <div class="container grid grid-2" style="align-items:start">
    <div>
      <h2>Why monthly giving matters most.</h2>
      <p>Predictable monthly support lets us commit to multi-year shelter partnerships, hire program staff, and respond to disasters within hours instead of weeks.</p>
      <ul class="list-check">
        <li>$10/month = [XX] meals for shelter animals annually</li>
        <li>$25/month = one spay/neuter procedure every month</li>
        <li>$50/month = a vet checkup for [X] animals every month</li>
        <li>$100/month = a small operating grant to one partner shelter</li>
      </ul>
      <p style="color:var(--color-text-muted); font-size:.9rem">All figures are placeholders pending real cost-per-outcome data.</p>
    </div>
    <div class="donate-widget">
      <h3>Make a donation</h3>
      <p style="color:var(--color-text-muted); font-size:.95rem">Preview only — connects to GiveWP / Stripe in production.</p>
      <div class="donate-toggle">
        <button class="is-active">Monthly</button>
        <button>One-time</button>
      </div>
      <div class="amount-grid">
        <button class="amount-btn">$10</button>
        <button class="amount-btn is-active">$25</button>
        <button class="amount-btn">$50</button>
        <button class="amount-btn">$100</button>
        <button class="amount-btn">$250</button>
        <button class="amount-btn">Other</button>
      </div>
      <div class="form-row" style="margin-bottom:var(--space-4)">
        <label>Email for receipt</label>
        <input type="email" placeholder="you@example.com">
      </div>
      <button class="btn btn-primary" style="width:100%; justify-content:center">Donate $25 monthly →</button>
      <p style="font-size:.8rem; color:var(--color-text-muted); margin-top:var(--space-3); text-align:center">100% tax-deductible · Cancel anytime · EIN XX-XXXXXXX</p>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <h2 class="text-center" style="margin-bottom:var(--space-6)">Other ways to give.</h2>
    <div class="grid grid-3">
      <div class="card"><h3>Wills &amp; estates</h3><p>Leave a planned gift in your will or trust.</p><a href="wills-estates.html">Learn more →</a></div>
      <div class="card"><h3>Stock &amp; crypto</h3><p>Donate appreciated securities or cryptocurrency.</p><a href="contact.html">Get instructions →</a></div>
      <div class="card"><h3>Donor-advised funds</h3><p>Recommend a grant from your DAF.</p><a href="contact.html">DAF instructions →</a></div>
      <div class="card"><h3>Workplace giving</h3><p>Payroll deduction and employer matches.</p><a href="corporate-partners.html">Workplace giving →</a></div>
      <div class="card"><h3>Tribute gifts</h3><p>Honor or memorialize a loved one.</p><a href="contact.html">Make a tribute →</a></div>
      <div class="card"><h3>Vehicle donation</h3><p>Donate a car, boat, or RV.</p><a href="contact.html">Vehicle donation →</a></div>
    </div>
  </div>
</section>
"""

# --- MONTHLY GIVING ---------------------------------------------------------
MONTHLY_BODY = page_hero(
    "Monthly Giving",
    "Predictable support, compounded impact. Becoming a monthly donor is the single most effective way to advance the mission.",
    "Monthly Giving",
) + """
<section class="section">
  <div class="container grid grid-2" style="align-items:center">
    <div>
      <h2>The math behind monthly giving.</h2>
      <p>One $25 monthly gift outperforms a one-time $300 gift. Why? Predictable revenue lets us commit to grants we'd otherwise have to delay, and the administrative cost per dollar is lower.</p>
      <ul class="list-check">
        <li>Less than 5% of monthly gifts are spent on processing</li>
        <li>Cancel anytime — no phone calls, no friction</li>
        <li>Update your amount or pause from your donor portal</li>
        <li>Year-end tax summary delivered automatically</li>
      </ul>
    </div>
    <div class="donate-widget">
      <h3>Become a monthly donor</h3>
      <div class="donate-toggle"><button class="is-active">Monthly</button><button>One-time</button></div>
      <div class="amount-grid">
        <button class="amount-btn">$10</button>
        <button class="amount-btn is-active">$25</button>
        <button class="amount-btn">$50</button>
      </div>
      <button class="btn btn-primary" style="width:100%; justify-content:center">Donate $25 monthly →</button>
    </div>
  </div>
</section>
"""

# --- WILLS & ESTATES --------------------------------------------------------
WILLS_BODY = page_hero(
    "Wills &amp; Estates",
    "A gift in your will or trust costs nothing today and can transform animal welfare for generations.",
    "Wills &amp; Estates",
) + """
<section class="section">
  <div class="container-narrow">
    <h2>Sample bequest language.</h2>
    <pre style="background:var(--color-mist); padding:var(--space-5); border-radius:var(--radius); overflow-x:auto; font-family:ui-monospace,monospace; font-size:.9rem">"I give and bequeath to the National Humane Society, a 501(c)(3) charitable
organization (EIN XX-XXXXXXX), located at [Address], the sum of $[amount]
[or X% of my estate] to be used for its general charitable purposes."</pre>
    <h2 style="margin-top:var(--space-7)">Other planned gifts</h2>
    <ul class="list-check">
      <li>Beneficiary designations (IRA, 401(k), life insurance)</li>
      <li>Charitable remainder trusts</li>
      <li>Charitable gift annuities</li>
      <li>Donor-advised fund successor designations</li>
    </ul>
    <p style="margin-top:var(--space-5)">Considering a planned gift? Our team can answer questions confidentially and at no cost.</p>
    <a class="btn btn-primary" href="contact.html">Speak with planned giving →</a>
  </div>
</section>
"""

# --- VOLUNTEER --------------------------------------------------------------
VOLUNTEER_BODY = page_hero(
    "Volunteer",
    "From shelter shifts to skills-based remote roles — there's a way to help that fits your time and ability.",
    "Volunteer",
) + """
<section class="section">
  <div class="container">
    <div class="grid grid-3">
      <div class="card">
        <div class="card-icon">🐕</div>
        <h3>At a partner shelter</h3>
        <p>Walk dogs, socialize cats, help with adoption events. Schedules vary by shelter — find one near you.</p>
        <a href="shelter-partners.html">Find a shelter →</a>
      </div>
      <div class="card">
        <div class="card-icon">💻</div>
        <h3>Remote &amp; skills-based</h3>
        <p>Photography, social media, grant writing, web development. Help us amplify the work of partner shelters.</p>
        <a href="contact.html">Apply →</a>
      </div>
      <div class="card">
        <div class="card-icon">🚐</div>
        <h3>Disaster response</h3>
        <p>Trained responders deploy to hurricanes, wildfires, and large-scale rescue operations. Background check + training required.</p>
        <a href="contact.html">Get on the roster →</a>
      </div>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container-narrow">
    <h2>Volunteer interest form</h2>
    <form class="form-grid" onsubmit="event.preventDefault(); alert('Preview only — volunteer signup');">
      <div class="grid grid-2">
        <div class="form-row"><label>First name</label><input type="text" required></div>
        <div class="form-row"><label>Last name</label><input type="text" required></div>
      </div>
      <div class="form-row"><label>Email</label><input type="email" required></div>
      <div class="form-row"><label>City &amp; state</label><input type="text" required></div>
      <div class="form-row"><label>What kind of volunteering interests you?</label>
        <select><option>At a local shelter</option><option>Remote / skills-based</option><option>Disaster response</option><option>Not sure yet</option></select>
      </div>
      <div class="form-row"><label>Anything else we should know?</label><textarea rows="4"></textarea></div>
      <button class="btn btn-primary" type="submit">Submit interest →</button>
    </form>
  </div>
</section>
"""

# --- CORPORATE PARTNERS -----------------------------------------------------
CORP_BODY = page_hero(
    "Corporate Partners",
    "Workplace giving, sponsorships, and matching gifts. Help your team rally around a cause that matters.",
    "Corporate Partners",
) + """
<section class="section">
  <div class="container">
    <div class="grid grid-3">
      <div class="card"><h3>Workplace giving</h3><p>Payroll deduction with optional employer match.</p></div>
      <div class="card"><h3>Sponsorships</h3><p>Sponsor a sweepstakes, an annual report, or a regional grant cycle.</p></div>
      <div class="card"><h3>Matching gifts</h3><p>We register with all major matching-gift platforms.</p></div>
      <div class="card"><h3>Volunteer days</h3><p>Coordinate a team day at a partner shelter.</p></div>
      <div class="card"><h3>Cause marketing</h3><p>Donate-with-purchase campaigns and round-up programs.</p></div>
      <div class="card"><h3>In-kind donations</h3><p>Pet supplies, vehicles, professional services.</p></div>
    </div>
    <div class="text-center" style="margin-top:var(--space-6)">
      <a class="btn btn-primary" href="contact.html">Talk to our partnerships team →</a>
    </div>
  </div>
</section>
"""

# --- BLOG INDEX -------------------------------------------------------------
BLOG_BODY = page_hero(
    "Blog",
    "Donor education, volunteer guides, pet care, and shelter stories.",
    "Blog",
) + """
<section class="section">
  <div class="container">
    <div class="grid grid-3">
""" + "\n".join(f"""      <article class="post-card">
        <div class="post-image" style="background-image:url('assets/img/{img}')"></div>
        <div class="post-body">
          <div class="post-tag">{tag}</div>
          <h3><a href="blog-post.html">{title}</a></h3>
          <p style="color:var(--color-text-muted)">{excerpt}</p>
        </div>
      </article>""" for tag, title, excerpt, img in [
    ("Donor education", "How your $10 monthly donation really helps shelter animals", "A breakdown of where every dollar goes — and the math behind why monthly giving compounds.", "animal-vet-exam-2.jpg"),
    ("Volunteer guide", "How to volunteer at a local animal shelter", "Six ways to start — even if you've never set foot in a shelter before.", "animal-first-aid-1.jpg"),
    ("Pet care", "Hurricane prep checklist for pet owners", "Evacuation kits, microchipping, and the 72-hour plan every household needs.", "animal-lost-dog.jpg"),
    ("Adoption", "Adopting from a shelter vs. a rescue: what's the difference?", "Both are great. Here's how to decide which is right for your household.", "animal-winterpup.jpg"),
    ("Pet care", "Spay &amp; neuter: the math that saves millions of lives", "Why a single spay/neuter procedure prevents thousands of unwanted births.", "animal-vet-exam.jpg"),
    ("Advocacy", "Five animal welfare laws that changed everything", "From the Animal Welfare Act to the PUPS Act — a brief history.", "animal-heartworm.jpg"),
    ("Pet care", "What to do if you find a stray animal", "Step-by-step: safety, identification, and finding the right shelter.", "animal-first-aid-2.jpg"),
    ("Stories", "From hoarding case to home: [Pet Name]'s rescue", "How a partner shelter rehabilitated [XX] dogs from a single intake.", "winner-gonzo.jpg"),
    ("Donor education", "Is my donation tax-deductible? A clear answer.", "What qualifies, what doesn't, and how to document it for the IRS.", "animal-cat.jpg"),
]) + """
    </div>
  </div>
</section>
"""

# --- BLOG POST --------------------------------------------------------------
BLOG_POST_BODY = """
<section class="page-hero">
  <div class="container-narrow">
    <div class="breadcrumb"><a href="index.html">Home</a> &nbsp;/&nbsp; <a href="blog.html">Blog</a> &nbsp;/&nbsp; Donor education</div>
    <p class="eyebrow">Donor education · 6 min read · Published [date]</p>
    <h1>How your $10 monthly donation really helps shelter animals</h1>
    <p class="lead">A breakdown of where every dollar goes — and the math behind why monthly giving compounds.</p>
  </div>
</section>

<section class="section">
  <div class="container-narrow" style="font-size:1.05rem; line-height:1.8">
    <p><em>This article is a preview placeholder. The real article would carry the same byline, author bio, and structured content — published through the blog post type in WordPress.</em></p>
    <h2>The cost-per-outcome math</h2>
    <p>[Placeholder body — explanation of cost-per-spay, cost-per-meal, cost-per-vet-checkup, and how a $10/month gift compounds across a year.]</p>
    <h2>Why monthly beats one-time</h2>
    <p>[Placeholder body.]</p>
    <h2>Where exactly does the money go?</h2>
    <p>[Placeholder body — link to the financial transparency page.]</p>
    <h2>The compound effect</h2>
    <p>[Placeholder body.]</p>

    <div class="proceeds-panel" style="margin-top:var(--space-7)">
      <h4>Ready to start a monthly gift?</h4>
      <p style="margin:0 0 var(--space-3)">Most monthly donors start at $10 or $25. You can change or cancel anytime.</p>
      <a class="btn btn-primary btn-sm" href="donate.html">Donate monthly →</a>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="container">
    <h2 class="text-center" style="margin-bottom:var(--space-6)">More like this.</h2>
    <div class="grid grid-3">
      <article class="post-card"><div class="post-image" style="background-image:url('assets/img/animal-cat.jpg')"></div><div class="post-body"><div class="post-tag">Donor education</div><h3><a href="blog-post.html">Is my donation tax-deductible? A clear answer.</a></h3></div></article>
      <article class="post-card"><div class="post-image" style="background-image:url('assets/img/winner-gonzo.jpg')"></div><div class="post-body"><div class="post-tag">Stories</div><h3><a href="blog-post.html">From hoarding case to home: [Pet Name]'s rescue</a></h3></div></article>
      <article class="post-card"><div class="post-image" style="background-image:url('assets/img/animal-vet-exam.jpg')"></div><div class="post-body"><div class="post-tag">Pet care</div><h3><a href="blog-post.html">Spay &amp; neuter: the math that saves millions</a></h3></div></article>
    </div>
  </div>
</section>
"""

# --- VIDEOS -----------------------------------------------------------------
VIDEOS_BODY = page_hero(
    "Videos",
    "Rescue stories, donor education, and behind-the-scenes from partner shelters.",
    "Videos",
) + """
<section class="section">
  <div class="container">
    <div class="grid grid-3">
""" + "\n".join(f"""      <article class="post-card">
        <div class="post-image" style="background-image:url('assets/img/{img}'); position:relative;">
          <span style="position:absolute; inset:0; display:grid; place-items:center; color:#fff; font-size:2.5rem; text-shadow:0 2px 8px rgba(0,0,0,.4)">▶</span>
        </div>
        <div class="post-body">
          <div class="post-tag">{tag}</div>
          <h3>{title}</h3>
          <p style="color:var(--color-text-muted); font-size:.9rem">{duration}</p>
        </div>
      </article>""" for tag, title, duration, img in [
    ("Rescue story", "Inside a hoarding-case rescue", "4:32", "animal-first-aid-2.jpg"),
    ("Donor", "Where your dollars go: a tour", "6:15", "animal-vet-exam.jpg"),
    ("Partner", "Meet [Shelter Name]", "3:48", "animal-winterpup.jpg"),
    ("Education", "Spay/neuter explained", "5:02", "animal-vet-exam-2.jpg"),
    ("Disaster", "Hurricane response in [State]", "7:22", "animal-lost-dog.jpg"),
    ("Adoption", "[Pet Name]'s adoption day", "2:55", "winner-gonzo.jpg"),
]) + """
    </div>
  </div>
</section>
"""

# --- PET CARE: CATS ---------------------------------------------------------
PETCARE_CATS_BODY = page_hero(
    "Pet Care: Cats",
    "Resources for cat owners — adoption, health, behavior, and emergency prep.",
    "Pet Care: Cats",
) + """
<section class="section">
  <div class="container grid grid-3">
    <div class="card"><h3>Adopting a cat</h3><p>What to ask the shelter, how to prepare your home, and the first 30 days.</p><a href="#">Read more →</a></div>
    <div class="card"><h3>Indoor vs. outdoor</h3><p>Lifespan, safety, and a middle path: catios and supervised outdoor time.</p><a href="#">Read more →</a></div>
    <div class="card"><h3>Routine veterinary care</h3><p>Vaccinations, dental, and what 'wellness' visits should cover.</p><a href="#">Read more →</a></div>
    <div class="card"><h3>Spay &amp; neuter</h3><p>Why it matters, when to do it, and where to find low-cost clinics.</p><a href="#">Read more →</a></div>
    <div class="card"><h3>Behavior 101</h3><p>Litter box troubles, scratching, and introducing a new cat to your home.</p><a href="#">Read more →</a></div>
    <div class="card"><h3>Senior cat care</h3><p>What changes after age 10, and how to make life easier.</p><a href="#">Read more →</a></div>
  </div>
</section>
"""

# --- PET CARE: DOGS ---------------------------------------------------------
PETCARE_DOGS_BODY = page_hero(
    "Pet Care: Dogs",
    "Resources for dog owners — adoption, training, health, and emergency prep.",
    "Pet Care: Dogs",
) + """
<section class="section">
  <div class="container grid grid-3">
    <div class="card"><h3>Adopting a dog</h3><p>Choosing the right match, the first 30 days, and crate training basics.</p><a href="#">Read more →</a></div>
    <div class="card"><h3>Training fundamentals</h3><p>Sit, stay, recall, and why positive reinforcement wins.</p><a href="#">Read more →</a></div>
    <div class="card"><h3>Routine veterinary care</h3><p>Vaccinations, heartworm prevention, and dental.</p><a href="#">Read more →</a></div>
    <div class="card"><h3>Spay &amp; neuter</h3><p>Why it matters, when to do it, and where to find low-cost clinics.</p><a href="#">Read more →</a></div>
    <div class="card"><h3>Common behavior issues</h3><p>Pulling on leash, separation anxiety, reactivity.</p><a href="#">Read more →</a></div>
    <div class="card"><h3>Senior dog care</h3><p>Joint health, mobility, and what to expect in the senior years.</p><a href="#">Read more →</a></div>
  </div>
</section>
"""

# --- PET CARE: HURRICANE ----------------------------------------------------
PETCARE_HURRICANE_BODY = page_hero(
    "Hurricane &amp; Disaster Prep for Pet Owners",
    "A 72-hour plan that makes sure your pets are evacuated, identified, and accounted for.",
    "Hurricane Prep",
) + """
<section class="section">
  <div class="container-narrow">
    <h2>The 72-hour pet emergency kit.</h2>
    <ul class="list-check">
      <li>Three days of food and water per pet (rotate every 6 months)</li>
      <li>Medications (two-week supply, in a waterproof container)</li>
      <li>Carrier or crate for every animal</li>
      <li>Leashes, harnesses, and ID tags</li>
      <li>Vaccination and microchip records (paper copies + photos on your phone)</li>
      <li>Recent photo of you with each pet (proof of ownership at shelters)</li>
      <li>Litter and disposable trays for cats</li>
      <li>Comfort item: a familiar blanket or toy</li>
    </ul>

    <h2>Before a storm</h2>
    <ul class="list-check">
      <li>Confirm your microchip is registered to a current phone number</li>
      <li>Identify pet-friendly evacuation destinations within 200 miles</li>
      <li>Know your local pet-friendly emergency shelters</li>
      <li>Practice loading every animal into a carrier</li>
    </ul>

    <h2>If you must evacuate without your pet</h2>
    <ul class="list-check">
      <li>Never leave a pet tied or caged outdoors</li>
      <li>Leave 5–7 days of water in spill-proof bowls</li>
      <li>Place a sticker on your front window noting how many pets are inside</li>
      <li>Notify a neighbor or your local animal control</li>
    </ul>
  </div>
</section>
"""

# --- CONTACT ----------------------------------------------------------------
CONTACT_BODY = page_hero(
    "Contact",
    "Reach our team — donor support, press inquiries, shelter partnerships, planned giving, or general questions.",
    "Contact",
) + """
<section class="section">
  <div class="container grid grid-2">
    <div>
      <h2>Send a message.</h2>
      <form class="form-grid" onsubmit="event.preventDefault(); alert('Preview only — contact form');">
        <div class="grid grid-2">
          <div class="form-row"><label>First name</label><input type="text" required></div>
          <div class="form-row"><label>Last name</label><input type="text" required></div>
        </div>
        <div class="form-row"><label>Email</label><input type="email" required></div>
        <div class="form-row"><label>I'm contacting about</label>
          <select>
            <option>Donor support</option>
            <option>Sweepstakes / entry support</option>
            <option>Shelter partnership inquiry</option>
            <option>Planned giving</option>
            <option>Press / media</option>
            <option>Volunteer</option>
            <option>Something else</option>
          </select>
        </div>
        <div class="form-row"><label>Message</label><textarea rows="6" required></textarea></div>
        <button class="btn btn-primary" type="submit">Send →</button>
      </form>
    </div>
    <div>
      <h3>By phone</h3>
      <p>Customer service: <strong>877-285-0710</strong><br>Mon–Fri, 9am–6pm ET</p>

      <h3 style="margin-top:var(--space-5)">By mail</h3>
      <p>National Humane Society<br>[Street Address]<br>[City, State ZIP]</p>

      <h3 style="margin-top:var(--space-5)">Press</h3>
      <p><a href="mailto:press@nationalhumanesociety.org">press@nationalhumanesociety.org</a></p>

      <h3 style="margin-top:var(--space-5)">Shelter partners</h3>
      <p><a href="mailto:partners@nationalhumanesociety.org">partners@nationalhumanesociety.org</a></p>

      <h3 style="margin-top:var(--space-5)">Planned giving</h3>
      <p><a href="mailto:plannedgiving@nationalhumanesociety.org">plannedgiving@nationalhumanesociety.org</a></p>
    </div>
  </div>
</section>
"""

# ---------------------------------------------------------------------------
# Page registry
# ---------------------------------------------------------------------------
PAGES = [
    ("Home", "index.html", HOME_BODY),
    ("Our Mission", "about.html", ABOUT_BODY),
    ("Programs", "programs.html", PROGRAMS_BODY),
    ("Impact & Outcomes", "impact.html", IMPACT_BODY),
    ("Shelter Partners", "shelter-partners.html", SHELTER_BODY),
    ("Financial Transparency", "financial-transparency.html", FINANCIAL_BODY),
    ("Sweepstakes", "sweepstakes.html", SWEEPSTAKES_BODY),
    ("New Porsche 911 Sweepstakes", "sweepstakes-detail.html", SWEEPSTAKES_DETAIL_BODY),
    ("Raffle Plus", "raffle-plus.html", RAFFLE_BODY),
    ("How Sweepstakes Work", "how-it-works.html", HOW_IT_WORKS_BODY),
    ("FAQ", "faq.html", FAQ_BODY),
    ("Official Rules", "rules.html", RULES_BODY),
    ("Previous Winners", "previous-winners.html", WINNERS_BODY),
    ("Donate", "donate.html", DONATE_BODY),
    ("Monthly Giving", "monthly-giving.html", MONTHLY_BODY),
    ("Wills & Estates", "wills-estates.html", WILLS_BODY),
    ("Volunteer", "volunteer.html", VOLUNTEER_BODY),
    ("Corporate Partners", "corporate-partners.html", CORP_BODY),
    ("Blog", "blog.html", BLOG_BODY),
    ("How your $10 monthly donation really helps", "blog-post.html", BLOG_POST_BODY),
    ("Videos", "videos.html", VIDEOS_BODY),
    ("Pet Care: Cats", "pet-care-cats.html", PETCARE_CATS_BODY),
    ("Pet Care: Dogs", "pet-care-dogs.html", PETCARE_DOGS_BODY),
    ("Hurricane Prep", "pet-care-hurricane.html", PETCARE_HURRICANE_BODY),
    ("Contact", "contact.html", CONTACT_BODY),
]


def main():
    written = []
    for title, slug, body in PAGES:
        _, html = page(title, slug, body)
        out = OUT_DIR / slug
        out.write_text(html, encoding="utf-8")
        written.append(slug)
    print(f"Wrote {len(written)} pages:")
    for s in written:
        print(f"  - {s}")


if __name__ == "__main__":
    main()
