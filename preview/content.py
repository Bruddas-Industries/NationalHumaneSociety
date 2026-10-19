"""
National Humane Society — copy and data carried over from the live site.

Everything in this file was taken from nationalhumanesociety.org (the current
Webflow site) on 2026-10-08. build.py owns layout and navigation; this file
owns the facts. If the client changes a price, a date, a rule or a prize,
change it here and re-run `python build.py`.
"""

# ---------------------------------------------------------------------------
# Organization facts
# ---------------------------------------------------------------------------
# Not shown anywhere on the site (CJ, 2026-10-15). Kept on record for tax
# receipts and donor emails in the WordPress build.
EIN = "58-2399783"
ADDRESS_LINES = ["National Humane Society", "406 Suburban DR #364", "Newark, DE 19711"]
ORDER_LINE = "844-807-4052"
CUSTOMER_SERVICE = "877-285-0710"
EMAIL = "info@nationalhumanesociety.org"
SOCIAL = [
    ("Instagram", "https://www.instagram.com/nationalhumane/"),
    ("LinkedIn", "https://www.linkedin.com/company/national-humane"),
    ("Facebook", "https://www.facebook.com/nationalhumane"),
    ("X", "https://twitter.com/NationalHumane"),
]
LIVE_SITE = "https://www.nationalhumanesociety.org"

# ---------------------------------------------------------------------------
# Sweepstakes facts
# ---------------------------------------------------------------------------
# The Sweepstakes and Raffle Plus drawings are held every six months, so this
# date moves twice a year. It is the only place the date is written: the hero,
# the entry forms, the Rules and the FAQ all read it from here.
DRAWING_DATE = "December 31, 2026"

# (tickets bought, free tickets, sweepstakes price, raffle plus price, most popular?)
TICKET_TIERS = [
    (1, "50", 25, 125, False),
    (3, "2500", 75, 175, True),
    (10, "6000", 250, 350, False),
]

# Every car a winner can choose: the same list on both entry forms, in the
# Sweepstakes and Raffle Plus page galleries and in the prize lineup.
# Source: the live entry forms, confirmed by CJ on 2026-10-15 as the correct
# prize list, with the Rivian (R1T, R1S) and the Lucid (Gravity, Air) each
# offered as two models instead of one. (The Ford F-150 Lightning on the live
# EV page is not a prize; CJ.)
# Grouped by make here; the live forms list them in no particular order.
# (label as shown on the forms, thumbnail, prize page)
CAR_PRIZES = [
    ("Porsche 911 Carrera Cabriolet", "prize-porsche-911.webp", "new-porsche-sweepstakes.html"),
    ("Electric Porsche Taycan", "prize-porsche-taycan.jpg", "new-porsche-sweepstakes.html"),
    ("Macan S", "prize-porsche-macan.webp", "new-porsche-sweepstakes.html"),
    ("1965 Porsche", "prize-porsche-1965.jpg", "1965-porsche-sweepstakes.html"),
    ("Corvette", "prize-corvette-new.jpg", "new-corvette-sweepstakes.html"),
    ("Corvette E-Ray", "prize-corvette-eray.webp", "new-corvette-sweepstakes.html"),
    ("Classic 1967 Corvette", "prize-corvette-classic.jpg", "classic-corvette-sweepstakes.html"),
    ("Tesla Y", "prize-tesla-y.jpg", "tesla-sweepstakes.html"),
    ("Rivian R1T", "prize-rivian.jpg", "ev-sweepstakes.html"),
    ("Rivian R1S", "prize-rivian-r1s.avif", "ev-sweepstakes.html"),
    ("Lucid Gravity", "prize-lucid-gravity.jpg", "lucid.html"),
    ("Lucid Air", "prize-lucid-air.webp", "lucid.html"),
    ("Cadillac Escalade", "prize-cadillac-escalade.avif", "cadillac-sweepstakes.html"),
]

# Sweepstakes: one car or the cash. (label, thumbnail or None for cash)
SWEEPSTAKES_PRIZE_OPTIONS = [(label, image) for label, image, _page in CAR_PRIZES] + [
    ("$50,000.00 Cash", None),
]

# Raffle Plus: any two cars, or one car and $50,000, or $100,000 on its own.
# (label, thumbnail or None for cash, kind)
# kind: "car", "cash" ($50,000, pairs with one car) or "all" ($100,000, on its own)
RAFFLE_PLUS_PRIZE_OPTIONS = [(label, image, "car") for label, image, _page in CAR_PRIZES] + [
    ("$50,000.00 Cash", None, "cash"),
    ("$100,000.00 Cash", None, "all"),
]

AD_SOURCES = ["Postcard", "Email", "Instagram", "Facebook", "Google Ad",
              "Google Search", "Other (Enter in comment)"]

# One entry per prize page on the live site. Headlines are the live ones,
# except the Rivian and Lucid pages, which both said "Win a new EV" (CJ,
# 2026-10-18).
# slug, card label, headline, sub-headline, tagline, card image, cars
# car = (name, model-year note, image, [(spec label, value), ...])
PRIZES = [
    ("new-porsche-sweepstakes.html", "Porsche", "Win a new Porsche",
     "911 Carrera Cabriolet, Taycan, Macan", "Accept No Substitute.",
     "prize-porsche-911.webp", [
        ("Porsche 911 Cabriolet", "2026 Model", "prize-porsche-911.webp", [
            ("Engine", "DOHC 24-valve flat-6, aluminum block and heads, direct fuel injection"),
            ("Transmission", "6-speed manual, 7-speed dual-clutch automatic"),
            ("Horsepower", "388 hp @ 8400 rpm"),
            ("Torque", "334 lb-ft @ 6100 rpm"),
            ("Top speed", "181 mph"),
            ("Acceleration", "60 mph: 3.9 sec"),
        ]),
        ("Porsche Taycan S", "2026 Model", "prize-porsche-taycan.jpg", [
            ("Electric motor", "560 kW, Overboost Power with Launch Control"),
            ("Transmission", "2-speed transmission on the rear axle"),
            ("Horsepower", "402 hp, Overboost Power with Launch Control"),
            ("Torque", "254 lb-ft (max. torque with Launch Control)"),
            ("Top speed", "143 mph"),
            ("Acceleration", "0–60 mph with Launch Control 5.1 s"),
        ]),
        ("Porsche Macan", "2026 Model", "prize-porsche-macan.webp", [
            ("Engine", "2.0-liter turbocharged 4-cylinder engine"),
            ("Transmission", "7-speed Porsche Doppelkupplung (PDK) transmission"),
            ("Horsepower", "261 hp"),
            ("Torque", "295 lb-ft"),
            ("Acceleration", "0–60 mph: 4.3 s"),
        ]),
     ]),
    ("1965-porsche-sweepstakes.html", "1965 Porsche", "Win a 1965 Porsche",
     "356C", "", "prize-porsche-1965.jpg", [
        ("1965 Porsche 356C", "", "prize-porsche-1965.jpg", [
            ("Engine", "Displacement 1582 cc | 96.5 cu in. | 1.6 L"),
            ("Transmission", "4 Manual"),
            ("Horsepower", "74 BHP (54.464 KW) @ 5200 RPM"),
            ("Torque", "88 Ft-Lbs (119 NM) @ 3600 RPM"),
            ("Top speed", "106.898 mph"),
            ("Acceleration", "0–60 mph 13.5 seconds"),
        ]),
     ]),
    ("new-corvette-sweepstakes.html", "Corvette", "Win a new Corvette",
     "Stingray, EV E-Ray", "Ultimate Thrill", "prize-corvette-new.jpg", [
        ("Corvette Stingray", "2026 Model", "prize-corvette-new.jpg", [
            ("Engine", "6.2-liter V8"),
            ("Transmission", "8-speed dual-clutch automatic"),
            ("Horsepower", "525 hp"),
            ("Torque", "520 lb-ft"),
            ("Top speed", "194 mph"),
            ("Acceleration", "0–60 in 3.3 seconds"),
        ]),
        ("EV Corvette E-Ray", "2026 Model", "prize-corvette-eray.webp", [
            ("Engine", "6.2-liter V8"),
            ("Transmission", "8-speed automatic transmission"),
            ("Horsepower", "655 hp"),
            ("Torque", "470 lb-ft"),
            ("Top speed", "184 mph"),
            ("Acceleration", "0–60 in 2.5 seconds"),
        ]),
     ]),
    ("classic-corvette-sweepstakes.html", "Classic Corvette", "Win a Classic Corvette",
     "1967 Stingray", "", "prize-corvette-classic.jpg", [
        ("Classic Corvette 1967 Stingray", "", "prize-corvette-classic.jpg", [
            ("Engine", "16-valve V-8 427 cu in (6994 cc)"),
            ("Transmission", "4-speed manual"),
            ("Horsepower", "435 HP @ 5800 RPM"),
            ("Torque", "460 LB-FT @ 4000 RPM"),
            ("Top speed", "142 mph"),
            ("Acceleration", "0–60 mph 4.7 seconds"),
        ]),
     ]),
    ("tesla-sweepstakes.html", "Tesla", "Win a new Tesla Y",
     "", "", "prize-tesla-y.jpg", [
        ("Tesla Y (Long Range)", "2026 Model", "prize-tesla-y.jpg", [
            ("Engine", "Electric Dual Motor All-Wheel Drive, range 330 mi"),
            ("Transmission", "Single-speed"),
            ("Horsepower", "456 HP"),
            ("Torque", "247 lb·ft (335 N·m)"),
            ("Top speed", "155 mph"),
            ("Acceleration", "0–60 mph 3.5 seconds"),
        ]),
     ]),
    ("ev-sweepstakes.html", "Rivian", "Win a new Rivian",
     "Rivian", "", "prize-rivian.jpg", [
        ("Rivian R1T", "2026 Model", "prize-rivian.jpg", [
            ("Range", "260 to 314 mi battery-only"),
            ("Towing capacity", "11,000 lbs"),
            ("Battery charge", "13h at 220V"),
            ("Horsepower", "600 to 835 hp"),
        ]),
        ("Rivian R1S", "2026 Model", "prize-rivian-r1s.avif", [
            ("Range", "270 miles"),
            ("0–60", "4.5 sec"),
            ("Horsepower", "553 hp"),
        ]),
     ]),
    ("lucid.html", "Lucid", "Win a new Lucid",
     "Lucid", "", "prize-lucid-gravity.jpg", [
        ("Lucid Gravity", "2026 Model", "prize-lucid-gravity.jpg", [
            ("Range", "up to 450 mi"),
            ("0–60", "3.4 sec"),
            ("Horsepower", "828 hp"),
        ]),
        ("Lucid Air", "2026 Model", "prize-lucid-air.webp", [
            ("Range", "up to 420 miles"),
            ("0–60", "4.5 sec"),
            ("Horsepower", "430 hp"),
        ]),
     ]),
    ("cadillac-sweepstakes.html", "Cadillac", "Win a new Cadillac",
     "", "Accept No Substitute.", "prize-cadillac-escalade.avif", [
        ("Cadillac Escalade", "2026 Model", "prize-cadillac-escalade.avif", [
            ("Engine", "6.2L V8 with premium gasoline"),
            ("Horsepower", "420 hp"),
            ("Torque", "460 lb-ft with premium gasoline"),
            ("Towing capacity", "8100 lbs max available on 2WD models"),
        ]),
     ]),
]

# Verbatim, in the order published on /sweepstakes-rules, plus the 18+ age
# rule from the FAQ (added at CJ's request, 2026-10-18).
RULES = [
    "Tickets are $25.00 and can be paid for by credit card, money order or check.",
    "Winner will be announced at time and place of drawing.",
    "All entries to \"the presenter\" will remain property of the presenter.",
    "All tickets will be sent within 48 hours via email or USPS.",
    "By entering, entrants release the \"presenter\" and it's members, agents, employees and other related entities from any and all liabilities with respect to the prize.",
    "By entering winners consent to promotional use of their names and likeness without additional compensation.",
    "Need not be present to win.",
    "All decisions and interpretations of the rules and regulations are of the National Humane Society and its judgment is final.",
    "The event is subject to all federal rules, local laws and regulations and is void where prohibited by law.",
    "Entrants must be 18 years of age or older.",
    "All employees of the sponsoring organization and their families are not eligible to win.",
    "The winner of the prize must enter into contract within 30 days of selection of the winner and agree to execute all the documents necessary to effect the intent of these rules and accomplish the transfer of title.",
    "Payment of all applicable federal, state and local taxes, fees and surcharges, tags and registrations fees are the responsibility of the winner, who must provide proof of insurance to take delivery.",
    "Failure of the winner to claim the prize within 30 days will result in forfeiture of the prize.",
    "If the winner bought a Raffle Plus ticket they have their choice of any 2 cars or 1 car and the cash prize. Without Raffle Plus the winner has a choice of either any one car, or $50,000.00 cash. If the cash prize is selected it will be paid in 3 installments, 60 days apart.",
    "The prize is not transferable.",
    "In the case of a dispute or a disqualification the decision of the \"presenter\" shall be deemed final, conclusive and not subject to review.",
    "NHS officials reserve the right to amend any of the rules including the postponement of the drawing at any time and are not subject to review.",
    "By entering or accepting a prize winners agree to be bound by these official rules.",
    "If a prize is not generally available at programs end, a substitution of equal value will be made at the sponsors sole discretion.",
    "If a minimum number of tickets are not sold the prize becomes a cash amount of the net proceeds to be determined by the National Humane Society.",
    "The NHS reserves the right to refuse anyone from participating in any of it's drawings that they deem detrimental to the drawing or the charity.",
    f"Drawing date {DRAWING_DATE}.",
    "No purchase is necessary. Please send a self-addressed stamped envelope to NHS 406 Suburban Dr #364 Newark, DE 19711.",
]

# (question, answer html) from /faq. Two answers on the live page still carry a
# 2025 drawing date and a different mailing address; those are swapped for the
# values used everywhere else on the site and called out in a review note.
FAQ = [
    ("How old do I have to be to purchase a Sweepstakes or Raffle Plus ticket?",
     "<p>You must be 18 years or older to purchase a ticket for our Sweepstakes or Raffle Plus.</p>"),
    ("How do I purchase a Sweepstakes or Raffle Plus ticket?",
     "<p>Sweepstakes and Raffle Plus tickets are on sale on our website. Place an order online, send a check to 406 Suburban DR #364, Newark, DE 19711 or call our order line at 844-807-4052.</p>"
     f'<p>The winning ticket will be drawn on <strong class="faq-date">{DRAWING_DATE}</strong>.</p>'),
    ("Can I buy a ticket as a gift for or on behalf of someone else?",
     "<p>Yes! To purchase an entry for someone else, simply use their name and contact information when completing your purchase.</p>"),
    ("How can I get a copy of my ticket?",
     "<p>Your ticket numbers will be emailed or mailed to you within 48 hours of your purchase.</p>"),
    ("How will the winners be informed?",
     "<p>The lucky prize winner will receive a phone call directly from us immediately following the drawings. In the event that we cannot reach winners by phone, we will email them.</p>"),
    ("Do I have to be present for the drawing in order to win?",
     "<p>No, winners do not need to be present to win.</p>"),
    ("What is the value of the prizes?",
     "<p>Varies depending on the car or cash prize selected.</p>"),
    ("When are the drawings?",
     f"<p>The winning ticket will be drawn on {DRAWING_DATE}.</p>"),
    ("What percentage of the money raised goes to charity?",
     "<p>100% of your donation goes to the National Humane Society, a 501(c)(3) organization.</p>"
     "<p>All of the donations benefit animal shelters, Spay and Neuter programs to help reduce the large number of unwanted animals born in the US each year, Veterinarian bills for pet owners and other animal related aspects of our charitable mission.</p>"
     "<p>A few of the groups that have benefited from donations are: Second Chance Animal Rescue Society, The Humane Society of the United States, American Society for the Prevention of Cruelty to Animals, San Francisco Humane Society, Jacksonville Humane Society among many others.</p>"),
    ("Is there a limit on how many people can enter?",
     "<p>Yes. Only 1,000 participants can purchase tickets for each drawing.</p>"),
    ("Who provides the prizes?",
     "<p>Cars provided by Winner Automobile Group of Delaware and Porsche of Delaware.</p>"),
    ("If I still have questions about the National Humane Society's Sweepstakes or Raffle Plus, who do I contact?",
     "<p>Send an e-mail to <a href=\"mailto:info@nationalhumanesociety.org\">info@nationalhumanesociety.org</a> or call us at 877-285-0710 and we will gladly clear up any questions you may have!</p>"),
]

# (name, state, image file or None) in the order shown on /previous-winners.
WINNERS = [
    ("Timothy M", "IL", None),
    ("William O", "VT", None),
    ("Lloyd G", "HI", "winner-lloyd.png"),
    ("Mike T", "CA", None),
    ("Anthony J", "MI", None),
    ("D Johnson", "WA", None),
    ("Henry C", "AL", "winner-henry.png"),
    ("Tony L", "FL", "winner-nhs-pic.jpg"),
    ("Matthew B", "MI", "winner-gonzo.jpg"),
    ("Don R", "AK", None),
    ("Vicki S", "IN", "winner-vicki.jpg"),
    ("Brent M", "Canada", "winner-brent.jpg"),
    ("David M", "WA", "winner-michaels.jpg"),
    ("Anne O", "Canada", "winner-anne.jpg"),
    ("Jim F", "CA", "winner-forsythe.jpg"),
    ("Leon J", "NJ", "winner-leon.jpg"),
    ("Anthony M", "NJ", "winner-malone.jpg"),
    ("Andy J", "MA", "winner-jenkins.jpg"),
    ("Harlin B", "SD", "winner-bachmann.jpg"),
    ("Don H", "TN", "winner-harting.jpg"),
    ("Geri C", "WV", "winner-ginger.jpg"),
    ("Emily B", "NY", "winner-berger.jpg"),
    ("Michael F", "TN", "winner-fleming.jpg"),
    ("Gerald P", "WI", "winner-gerald.jpg"),
    ("Tom O", "CO", "winner-tolson.jpg"),
    ("Tim S", "AR", "winner-stanley.jpg"),
]

# "COVID-19 & Your Pets" from the live homepage. (question, answer)
COVID_QA = [
    ("Should I test my pet for COVID-19?",
     "None of the national veterinarian groups recommend companion animals be routinely tested for COVID-19."),
    ("Can pets transmit COVID-19 to people?",
     "Currently, there is no evidence that animals can transmit this virus to people. Animal-to-human transmission events are believed to be rare."),
    ("If my pet is sick and I think it is COVID-19, what should I do?",
     "If your pet gets sick after contact with a person with COVID-19, do not take it to your veterinarian; call your vet to determine what the next steps should be for your pet's treatment and care."),
]

# ---------------------------------------------------------------------------
# Donations
# ---------------------------------------------------------------------------
DONATE_MONTHLY = [10, 25, 50, 100, 500]
DONATE_ONE_TIME = [10, 25, 50, 100, 250]

# Logos shown on /donations-helping-animals ("recently given money to").
PARTNER_LOGOS = [
    ("partner-jhs.png", "Jacksonville Humane Society"),
    ("partner-nmar.jpeg", "North Mississippi Animal Rescue"),
    ("partner-hssm.webp", "Humane Society of South Mississippi"),
    ("partner-rescueme.gif", "Rescue Me"),
]

# (title, image or None, signature, paragraphs) from /donations-helping-animals.
STORIES = [
    ("Haven", "story-haven.png", "Eryn · with A Dozen Roses Animal Rescue", [
        "Haven had a rough start to life but it immediately improved when A Dozen Roses Animal Rescue pulled her from a bad situation. I work at a busy veterinary clinic and remember the day they walked through the door with this sad looking 7 week old puppy. It was clear from looking at her that she was going to lose her eye. It’s unclear how it happened but she sustained trauma or severe infection to the point that her eye had ruptured and it couldn’t be saved. Surgery was a success and although her eye was gone, she would be a lot less painful.",
        "Unfortunately, it was also discovered that Haven had a severe heart murmur. A murmur that is almost as bad as it gets. She was given a very short life expectancy. Days, weeks, maybe a few months if she was lucky. She wasn’t adoptable and she was going to break someone’s heart in a short amount of time and I decided it may as well be mine. Haven joined my family that day and she has made it to 7 months old. She has defied all odds so far.",
        "She recently had a cardiac work up done, which involved an ultrasound to see exactly where the problem with her heart lies. Haven has something called severe Pulmonic Stenosis. Pulmonic Stenosis is a congenital heart defect of the semilunar valve that is between the right ventricle of the heart and the pulmonary artery (the vessel that takes blood to the lungs). The leaflets of this valve are thickened and/or partially fused together and restricting blood flow. Because of this, Haven shows signs of exercise intolerance and will occasionally faint when she exerts herself.",
        "As bad as this all sounds, I was over the moon to find out that there is hope for Haven. PS is operable and her quality and quantity of life can be greatly improved with a procedure called a Balloon Valvuloplasty. This procedure would need to be done at The Atlantic Veterinary College in Prince Edward Island, Canada and it would be a 3 day long event from start to finish. This life saving surgery is going to cost roughly $7,000-$10,000.",
        "A Dozen Roses Animal Rescue and I are asking for your help to get Haven this life saving surgery. We can’t do this alone. Asking for help is usually out of the question for me but this is beyond my capabilities. Please help me save Haven. She is so strong and so smart. Anyone who meets her instantly loves her. Haven has made my life better for being in it and I would give anything to see her live the long and healthy life she deserves. Haven is the dog I never knew I truly needed until she was here and I can’t imagine a life without her.",
        "Thank you from the bottom of my heart for reading.",
    ]),
    ("Cupcake", None, "Carla, May and Family", [
        "To whom it may concern, I am asking for financial assistance for a hardship that my family and I have endured. We had a family member pass away in June. Due to this there was no one to care and love Cupcake. My sister drove to go pickup Cupcake and bring her home to me. We knew that Cupcake had previously been diagnosed and had been treated for kidney stones. We had a special brand of food to continue to treat her for the kidney stones. At this time, we did not realize that there was a possibility for her to have kidney stones.",
        "On November 11, Cupcake did not seem herself, I contacted Eudora Animal hospital here in the town that I live in to see how much it would cost. They recommended that I sign up for care credit and they would see her. So I took her to the vet, to have her checked out. They ran x-rays and took blood and per the x-rays it indicated that she had a kidney stone blockage which was preventing her from urinating. The doctor indicated that she had four other stones as well and said that she would probably not survive a surgery and that the surgery could run up to $8000 which at this time I did not have. He also indicated with her age that she might not survive the surgery as well, since there were kidney damage due to the kidney stones.",
        "I brought her home, so that my family could say goodbye and we took her to Mission veterinary emergency in Mission Kansas to put her down. I have included with this email a picture of Cupcake's bill. I am asking you for financial assistance with this bill to help pay for Cupcake's doctor appointments and putting her down. Any assistance that you can offer is much appreciated by me and my family.",
        "Thank you for your time and consideration.",
    ]),
    ("Second Chance Animal Refuge Society", "story-scars.jpg",
     "Maureen Cummins · Second Chance Animal Refuge Society (S.C.A.R.S.)", [
        "We are a licensed no kill shelter in rural Kansas, (S.C.A.R.S.) and can never thank the National Humane Society enough for their continued generosity. Over the years, their financial support has allowed us to literally save hundreds of dogs who were abandoned, abused or severely starved.",
        "Last month we rescued five dogs who were living under the Sardou Bridge in Topeka, Ks. It is a rough area of town, and dogs roam the banks in search of food. We were able to catch five and they have been here for a month. Two are larger brown pit bull mixes and have gained 20 lbs each. Two are smaller and have gained 10 lbs each. The last was a 3 month of fawn brindle female pittie who was riddled with a variety of worms. It took several weeks of parasite treatment from our vet to bring these under control but Baby is gaining weight and now happy and healthy.",
        "These are a small sampling of the dogs who will receive full medical care due to the support by the National Humane Society....our heroes.",
    ]),
    ("Hank", "story-hank.jpg", "Second Chance Animal Refuge Society", [
        "Saturday morn rolled around, we were all busy as bees, when the car pulled up the driveway and the couple got out, holding a stuffed bag full of towels to donate. I immediately recognized them as people who had volunteered a few years back.",
        "They came through the gate and we began chatting as the husband reached down petting every dog. He happened to glance up and I noticed something held his attention and I looked over to where he was staring. \"Is that a Great Dane\" he asked me looking at Hank who was in the big kennel having his breakfast.",
        "My mind went back to the day two years ago when my phone rang. \"There is a purebred Great Dane being starved and beaten and owner is willing to surrender if I can find a place for a giant breed.\" How could I say no? I told her to bring him over and I would figure it out.",
        "That was the beginning of months of pure hard labor on my part, and he hung in there with me. His skeletal body broke my heart and his backbone stuck out and every rib was visible. This was not going to be an overnight fix.",
        "And so I began fixing what had been broken. Each day I fed him several times, made him stay quiet for an hour and then let him exercise in varying amounts. And each day he became stronger. His ribs disappeared, his face was no longer skeletal, and he made more and more laps around the pond every day.",
        "Slowly I began to see the dog he was meant to be. He was a light champagne faun color with black around his face. His legs were incredibly long and people commented on how regal he was.",
        "I loved him. He followed me everywhere and so we went to the pond every day and he frolicked in the pasture. Could I ever part with this wonderful dog?",
        "I answered Tim. Actually he is a purebred Dane and only a year and a half old. He is just so very tall!",
        "Tim and his wife spent time with Hank in between putting up a new flag, washing out the kennels and doing so many jobs demanding attention.",
        "And then the question I had dreaded...is he up for adoption. Was he? Could I let him go since he sleeps next to our bed and we had traveled a long road together. But then I knew he needed his very own home where he could live out his years. Hank would have a Great Dane sister and children to love him..his dream come true.",
        "I put a collar on him, got his records, helped load him up and kissed his face. He was leaving me which I never thought I would do. But Terry is gone and I am flying solo. I simply cannot keep them all and this is such a young dog, he deserves his own place.",
        "And once again, I watched as the car turned in our driveway, Hank looked at me confused, and I bravely waved at him and blew a kiss. \"I love you\" I called out. Let me know if you are not happy and I will there in a heartbeat.",
        "And so once again, the car drove away holding a beloved friend of mine. So that was it. I loved him. It snuck up on me as the months flew by and meanwhile the universe was making plans of its own.",
        "So, I let him go. He was headed out to meet his new family and thus begin a new chapter of his life.",
        "Oh Hank...may your days be filled with love and joy. May you never know hunger, or the feel of an angry hand, again. May you smell the flowers in the pasture in the spring, and sniff the new fallen snow in winter. And run with the wind now that you are strong.",
        "The world is yours......",
    ]),
]

# ---------------------------------------------------------------------------
# Animal programs — veterinary care assistance directory (/animal-programs)
# ---------------------------------------------------------------------------
VET_GENERAL = [
    ("The Pet Fund", "https://www.thepetfund.com/"),
    ("Brown Dog Foundation", "https://www.browndogfoundation.org/home"),
    ("Canine Cancer Awareness", "https://www.caninecancerawareness.org"),
]
VET_BREED = [
    ("CorgiAid", "http://www.corgiaid.org/"),
    ("Labrador Lifeline", "http://www.labradorlifeline.org/"),
    ("Westimed (West Highland White Terriers)", "http://www.westiemed.org/"),
]
VET_WORKING_DOG = [
    ("Helping Harley Cancer Treatment Grant", "http://grants.landofpuregold.com/"),
]
# state -> [(name, url, note html)]
VET_STATES = [
    ("California", [
        ("Voice for the Animals Foundation, Helping Friends Program", "http://vftafoundation.org/", ""),
        ("SHARE Marin Humane Society", "https://www.marinhumane.org/", ""),
        ("PAWS San Diego", "http://www.pawssdc.org/", ""),
        ("PAWS Los Angeles", "http://www.pawsla.org/", ""),
        ("PAWS San Francisco", "https://www.pawssf.org", ""),
    ]),
    ("Colorado", [("Max Fund", "https://www.maxfund.org", "")]),
    ("Connecticut", [("Manchester Area Network on AIDS AID-A-PET", "http://www.mana-ct.net/Aid-A-Pet.html", "")]),
    ("District of Columbia", [("PETS-DC", "http://www.petsdc.org/", "")]),
    ("Georgia", [("PALS - Pets Are Loving Support", "http://www.palsatlanta.org/", "")]),
    ("Massachusetts", [
        ("Massachusetts SPCA", "https://www.mspca.org/",
         "Provides financial assistance for pet owners receiving services at one of its three medical centers: "
         "Angell Memorial Animal Hospital-Boston, 350 South Huntington Ave., Boston, MA 02130, 617-522-7282 · "
         "Angell Animal Medical Center-Nantucket, 21 Crooked Lane, Nantucket, MA 02554, 508-228-1491 · "
         "Angell Animal Medical Center-Western New England, 171 Union St., Springfield, MA 01105, 413-785-1221"),
        ("Phinney's Friends (MSPCA)", "http://www.mspca.org/site/PageServer?pagename=advo_Phinney_Friends_HIV_AIDS", ""),
        ("The Sampson Fund", "https://www.sampsonfund.org",
         "The fund is to benefit companion animals of Cape Cod and the adjacent islands of Nantucket and Martha's Vineyard."),
    ]),
    ("Michigan", [
        ("Michigan Humane Society", "http://www.michiganhumane.org/",
         "Michigan Humane Society maintains three veterinary clinics: "
         "MHS Detroit Center for Animal Care, 7401 Chrysler Drive, Detroit, MI 48211, 313-872-0004 · "
         "MHS Rochester Hills Center for Animal Care, 3600 W. Auburn Road, Rochester Hills, MI 48309, 248-852-7424 · "
         "MHS Berman Center for Animal Care, 900 N. Newburgh Road, Westland, MI 48185, 734-721-4195"),
    ]),
    ("Nevada", [("Shakespeare Animal", "http://www.shakespeareanimalfund.org/", "")]),
    ("New York", [
        ("NY S.A.V.E Inc.", "https://www.nysave.org/", ""),
        ("Humane Society of Lollypop Farm", "https://www.lollypop.org/", ""),
    ]),
    ("Rhode Island", [("RIVMA Companion Animal Foundation", "http://www.companionanimalfoundation.org/", "")]),
    ("Texas", [("SPCA of Texas", "http://www.spca.org/site/PageServer?pagename=programs_socialservices_2004#petomeals", "")]),
    ("Washington", [("Pet Project: Seattle-King County Humane Society", "https://www.seattlehumane.org/", "")]),
]

# ---------------------------------------------------------------------------
# Animal info (/animal-info and /foods-to-avoid)
# ---------------------------------------------------------------------------
# Titles listed under "Information on Dogs & Cats". Only the last one links
# anywhere on the live site.
CATS_DOGS_ARTICLES = [
    ("Annual Veterinary Exams and Preventive Care", None),
    ("Basic Emergency First Aid for Pets", None),
    ("Heartworm: The Quiet Killer", None),
    ("What To Do If Your Dog Is Lost", None),
    ("\"People Foods\" to Avoid Feeding Your Pets", "foods-to-avoid.html"),
]

FOODS_TO_AVOID = [
    ("Chocolate, Coffee, Caffeine", "These products all contain substances called methylxanthines, which can cause vomiting and diarrhea, panting, excessive thirst and urination, hyperactivity, abnormal heart rhythm, tremors, seizures and even death. The darker the chocolate, the more dangerous it is to your pet."),
    ("Alcohol", "Alcoholic beverages and food products containing alcohol can cause vomiting, diarrhea, decreased coordination, central nervous system depression, difficulty breathing, tremors, abnormal blood acidity, coma and death."),
    ("Avocado", "The leaves, fruit, seeds and bark of avocados can cause vomiting and diarrhea in dogs. Birds and rodents are especially sensitive to avocado poisoning, and can develop congestion, difficulty breathing and fluid accumulation around the heart. Some ingestions may even be fatal."),
    ("Grapes &amp; Raisins", "Although the toxic substance within grapes and raisins is unknown, these fruits can cause kidney failure. In pets who already have certain health problems, signs may be more dramatic."),
    ("Macadamia Nuts", "Macadamia nuts have caused weakness, depression, vomiting, tremors and hyperthermia in dogs. Signs usually appear within 12 hours of ingestion and last approximately 12 to 48 hours."),
    ("Milk", "Because pets do not possess significant amounts of lactase (the enzyme that breaks down lactose in milk), milk and other milk-based products cause them diarrhea or other digestive upset."),
    ("Onions, Garlic, Chives", "These vegetables and herbs can cause gastrointestinal irritation and could lead to red blood cell damage. Although cats are more susceptible, dogs are also at risk if a large enough amount is consumed. Toxicity is normally diagnosed through history, clinical signs and microscopic confirmation of Heinz bodies. An occasional low dose, such as what might be found in pet foods or treats, likely will not cause a problem, but we recommend that you do NOT give your pets large quantities of these foods."),
    ("Raw/Undercooked Meat, Eggs and Bones", "Raw meat and raw eggs can contain bacteria such as Salmonella and E. coli that can be harmful to pets. In addition, raw eggs contain an enzyme called avidin that decreases the absorption of biotin (a B vitamin), which can lead to skin and coat problems. Feeding your pet raw bones may seem like a natural and healthy option that might occur if your pet lived in the wild. However, this can be very dangerous for a domestic pet, who might choke on bones, or sustain a grave injury should the bone splinter and become lodged in or puncture your pet’s digestive tract."),
    ("Salt", "Large amounts of salt can produce excessive thirst and urination, or even sodium ion poisoning in pets. Signs that your pet may have eaten too many salty foods include vomiting, diarrhea, depression, tremors, elevated body temperature, seizures and even death. In other words, keep those salty chips to yourself!"),
    ("Xylitol", "Xylitol is used as a sweetener in many products, including gum, candy, baked goods and toothpaste. It can cause insulin release in most species, which can lead to liver failure. The increase in insulin leads to hypoglycemia (lowered sugar levels). Initial signs of toxicosis include vomiting, lethargy and loss of coordination. Signs can progress to recumbancy and seizures. Elevated liver enzymes and liver failure can be seen within a few days."),
    ("Yeast Dough", "Yeast dough can rise and cause gas to accumulate in your pet’s digestive system. This can be painful and can cause the stomach or intestines to rupture. Because the risk diminishes after the dough is cooked and the yeast has fully risen, pets can have small bits of bread as treats. However, these treats should not constitute more than 5 percent to 10 percent of your pet’s daily caloric intake."),
]

HURRICANE_KIT = [
    ("Dogs and Cats", [
        "Your veterinarian's contact name and phone number", "Copies of pet vaccination records",
        "Medications", "Extra collar", "Food and water bowls", "Bottled water", "Toys", "Treats",
        "Paper towels", "Plastic baggies for picking up pet waste", "Muzzle, if necessary",
        "First aid kit", "Current photo of your pet",
        "5-day supply of pet food and can opener if you need one", "Kitty litter",
        "Small travel kitty litter box",
    ]),
    ("Snake", ["Several pillowcases for transporting", "Heating pad", "Water bowl"]),
    ("Small mammals (in small carriers)", ["Bedding material", "Food", "Food bowl and water bottle"]),
    ("Birds (in carrier with perch inside)", ["Food", "Water mister"]),
]
HURRICANE_DONTS = [
    "Don't leave your pet behind.",
    "Don't rely on the city to evacuate or care for your pet.",
    "Don't leave your pet tied up outside to a tree or a fence. They can't escape water, wind, or falling items or they'll die trying to escape.",
    "Don't leave your pet indoors; floods from tidal surges can trap your animal in a house.",
    "Don't plan to leave your pet anywhere within the hurricane strike zone.",
    "Don't leave your pet at a boarding facility in the strike zone. There's no guarantee they have an evacuation plan.",
]
HURRICANE_DOS = [
    "Choose an evacuation destination in advance of an evacuation order. Consider pet-friendly hotels, family, friends, and boarding facilities outside of the danger area. Pet friendly hotels can be found by visiting two websites www.petswelcome.com or www.petsallowed-hotels.com. If you don't have a computer, you can also visit a local library or the LA/SPCA.",
    "Call or check the website of the Louisiana Department of Agriculture &amp; Forestry or the LA/SPCA to find out where pet-friendly shelters may be located. These should be used as a last resort; they fill quickly on a first-come, first-served basis. You will be required to care for your pet so staying close-by the pet-friendly shelter is required.",
    "Check your pet's boarding facility's evacuation plans before going on vacation. Many veterinarians were forced to leave their clients' pets behind when Hurricane Katrina threatened New Orleans. Some people who boarded their pets while on vacation were unable to get back and their pets died. Make sure your boarding facility has a plan in advance in case you are unable to come home to retrieve your pet.",
    "Keep a hurricane-ready pack for your pet so you can pick up and go without forgetting important items.",
]
HURRICANE_MUST_HAVES = [
    ("Pet Travel Carrier", [
        "Get a portable secure and covered pet carrier in advance (carriers immediately sell out when evacuation orders are called). The carrier should be large enough so that your pet can completely turn around.",
        "Mark your name, address, and phone number on the carrier and that of an alternate contact outside the strike zone.",
    ]),
    ("Proper Identification", [
        "Get a properly fitted collar with up-to-date rabies and identification tags. Add a phone number that will allow you to be reached outside the disaster zone. LA/SPCA is giving away free tags for a limited time.",
        "Microchip your pet. A microchip ensures that your pet is identified in case his/her collar/tag is lost. Make sure your address is up-to-date with the microchipping company.",
    ]),
    ("Health Records &amp; Medication", [
        "All boarding facilities and veterinarian offices require proof of immunization before accepting animals. They will not risk the health and safety of the animals on-site regardless of how much pleading you do.",
    ]),
]

# ---------------------------------------------------------------------------
# Educational Messages (/blog) — the twelve most recent titles and live slugs
# ---------------------------------------------------------------------------
BLOG_POSTS = [
    ("Adopt, Don't Shop: A Heartfelt Plea for the Millions of Homeless Animals", "adopt-dont-shop-a-heartfelt-plea-for-the-millions-of-homeless-animals"),
    ("How to Keep Your Pets Safe During the Summer Months", "how-to-keep-your-pets-safe-during-the-summer-months"),
    ("Before &amp; After: Heartwarming Shelter Animal Transformation Stories – Real Rescues That Prove Hope Wins in 2026", "before-after-heartwarming-shelter-animal-transformation-stories---real-rescues-that-prove-hope-wins-in-2026"),
    ("How to Spot Animal Abuse &amp; Report It Safely – A Guide to Protecting Animals Nationwide in 2026", "how-to-spot-animal-abuse-report-it-safely---a-guide-to-protecting-animals-nationwide-in-2026"),
    ("Volunteer Heroes: Real Stories from the Front Lines of National Animal Rescue – Why Your Time Matters in 2026", "volunteer-heroes-real-stories-from-the-front-lines-of-national-animal-rescue---why-your-time-matters-in-2026"),
    ("Spay &amp; Neuter: The Simple Surgery Stopping Shelter Overcrowding Nationwide – Why It Matters in 2026", "spay-neuter-the-simple-surgery-stopping-shelter-overcrowding-nationwide---why-it-matters-in-2026"),
    ("Fostering 101: How You Can Save a Shelter Animal Without Permanent Adoption - A Complete Guide for 2026", "fostering-101-how-you-can-save-a-shelter-animal-without-permanent-adoption---a-complete-guide-for-2026"),
    ("7 Common Myths About Shelter Animals Debunked - Facts to Help You Adopt Confidently in 2026", "7-common-myths-about-shelter-animals-debunked---facts-to-help-you-adopt-confidently-in-2026"),
    ("How Your $10 Monthly Donation Really Helps Shelter Animals", "how-your-10-monthly-donation-really-helps-shelter-animals"),
    ("Why Adopting a Shelter Animal Saves More Lives Than You Think", "why-adopting-a-shelter-animal-saves-more-lives-than-you-think"),
    ("Animal Shelters vs. Rescue Organizations: What’s the Difference?", "animal-shelters-vs-rescue-organizations-whats-the-difference"),
    ("How to Find the Best Animal Shelter Near You", "how-to-find-the-best-animal-shelter-near-you"),
]
# The post reproduced on blog-post.html as the article template.
BLOG_SAMPLE_SLUG = "how-your-10-monthly-donation-really-helps-shelter-animals"

# Vimeo ids embedded on /videos-and-more. The live page gives them no titles.
VIDEO_IDS = ["1121408406", "1121408501", "1121408389", "1121408444",
             "1121408417", "1121408461", "1121408484", "1121408430"]
INSTAGRAM_FEATURED = "https://www.instagram.com/p/DX8EX5HvPh_/"

# ---------------------------------------------------------------------------
# Educational videos — the YouTube Shorts carousel under the home page hero
# ---------------------------------------------------------------------------
# The live home page fetches this playlist in the browser through the YouTube
# Data API, so new videos show up on their own. The prototype uses a snapshot
# of the playlist taken on 2026-10-13 (7 videos, newest first); the WordPress
# build should pull the playlist itself.
EDU_PLAYLIST_ID = "PLsIcOzw_C46xsdSpdIaopLjzA4n2hSebh"
EDU_PLAYLIST_URL = "https://www.youtube.com/playlist?list=" + EDU_PLAYLIST_ID
# Reworded from the playlist's own description on YouTube ("Meet Kapiolani -
# animal advocate with years of experience in shelter volunteering and animal
# rescue. With each video, she teaches us something new about the animal safety.")
EDU_PLAYLIST_INTRO = ("An animal advocate with years of experience in shelter volunteering and "
                      "animal rescue, Kapiolani teaches us something new about animal safety "
                      "in every video.")
# (YouTube video id, title) — titles as published, minus the all-caps and emoji.
EDU_VIDEOS = [
    ("vsFYHhMeMpo", "We donated a $1K shopping spree"),
    ("-l9j1tZLAjc", "The most emotional animal rescues have one thing in common"),
    ("2APCMlkKzIA", "Why can't you volunteer or foster?"),
    ("90Cf6X35cRU", "This 3-3-3 rule saves lives"),
    ("SFKD_TzzcRA", "Here's why senior shelter dogs love the deepest"),
    ("WALa7sAT5UI", "The biggest sign you should adopt a shelter pet"),
    ("6jUTEeyMllg", "7 million new shelter dogs and cats each year"),
]
