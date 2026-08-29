# Repair services lead-generation sites

Nine standalone marketing sites for home-services companies — **five for appliance
repair** and **four for HVAC repair** — each built as a separate, self-contained
static site with its own brand, palette, typography and page structure.

Five of the nine now carry real brands, domains and markets (see
[Brands](#brands)). The remaining four — all the HVAC sites — still use the
`<name>` placeholder and advertise San Diego County, and are swapped with one
command; see [Renaming](#renaming).

## The sites

| Directory | Trade | Design direction |
|---|---|---|
| `sites/appliance-01-bluecrest` | Appliance | Clean corporate blue. Split hero with a sticky quote card, photo service grid, three-step process. |
| `sites/appliance-02-boltyellow` | Appliance | High-contrast black and amber. Full-bleed photo hero with an inline quick-quote bar, scrolling ticker, photo tiles. |
| `sites/appliance-03-hearth` | Appliance | Warm cream and forest green, serif headlines. Circular service photos, testimonial-led, family-shop tone. |
| `sites/appliance-04-subzero-wolf` | Appliance | Restrained luxury in bone and brass, Cormorant serif. Sub-Zero and Wolf specialist — three service pillars, a fault index and a maintenance programme. |
| `sites/appliance-05-subzero-wolf-palm-springs` | Appliance | The Atelier design run for a second market — Palm Springs and the Coachella Valley, with desert-climate maintenance copy. |
| `sites/hvac-01-thermaline` | HVAC | Cool-to-warm gradient. Floating capsule nav, paired cooling/heating panels, horizontal process timeline. |
| `sites/hvac-02-nocturne` | HVAC | Dark premium with cyan accents. Glass form card, bento service grid, three pricing plans. |
| `sites/hvac-03-redalert` | HVAC | Emergency red utility. Square borders, published flat-rate price table, dense information layout. |
| `sites/hvac-04-sundesert` | HVAC | Sand and terracotta editorial. Magazine collage hero, drop-cap essay, numbered service spreads. |

Open `index.html` at the repository root for a gallery linking to all nine.

## Brands

Five sites have been taken off the placeholder and branded for a live market.
Their `<name>` placeholder is gone, so `rename.py` no longer affects them.

| Site | Company | Domain | Market | Phone |
|---|---|---|---|---|
| `appliance-03-hearth` | San Diego Home Appliance Care | sdappliancecare.com | San Diego | (619) 555-0142 |
| `appliance-04-subzero-wolf` | San Diego Built-In Appliance Specialists | subzero-maintenance.com | San Diego | (619) 555-0142 |
| `appliance-02-boltyellow` | Bit Appliance Services | bitapplianceservices.com | Palm Springs | (760) 555-0142 |
| `appliance-01-bluecrest` | La Quinta Appliance Repair | applianceservice-laquinta.com | Palm Springs | (760) 555-0142 |
| `appliance-05-subzero-wolf-palm-springs` | Palm Springs Built-In Appliance Specialists | subzero-servicecenter.com | Palm Springs | (760) 555-0142 |

Each logo is a two-line lockup — the wordmark carries the distinctive part of
the name and the tagline supplies the rest, so together they read as the full
company name without repeating it.

The phone numbers are still reserved 555 placeholders and need replacing before
launch. The domains are not attached to anything yet — see
[Pointing the domains](#pointing-the-domains).

## Pointing the domains

The sites are deployed on `*.vercel.app` URLs. To move one onto its real domain:

1. In the Vercel dashboard, open the project → Settings → Domains → Add.
2. Add the apex (`example.com`) and, if you want it, `www`.
3. At your registrar, create the DNS records Vercel shows — an `A` record for
   the apex and a `CNAME` for `www`.

Vercel issues the TLS certificate automatically once DNS resolves.

## What every site includes

- A single `index.html` — no build step, no framework, no runtime dependencies.
- Its own SVG logo and favicon, drawn to match the design.
- Real photography, resized and compressed locally (`assets/img/`), no hotlinking.
- Self-hosted WOFF2 fonts (`assets/fonts/`), so nothing is fetched from a third party.
- Lead capture: a validated quote form with an inline success state, a honeypot
  field, click-to-call links throughout and a sticky mobile call bar.
- Trust content: services, process, reviews, service-area list and an FAQ.
- SEO basics: title, meta description, Open Graph tags and `LocalBusiness`
  JSON-LD carrying the service area.
- Responsive layouts down to 360px, visible focus states and labelled form fields.

## Previewing

Any static server works. From the repository root:

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000/> for the gallery, or go straight to a site at
`http://localhost:8000/sites/hvac-02-nocturne/`. Opening `index.html` from the
filesystem works too.

Each site directory is independent — deploy one by uploading that folder alone.

## Renaming

The company name appears as `<name>` throughout. In HTML body text it is written
as the entity `&lt;name&gt;` so browsers render the angle brackets rather than
treating it as a tag; in attributes, JSON-LD and comments it appears raw.
`rename.py` handles both forms, along with the phone number, email and service
area:

```sh
./rename.py "Pacific Appliance Repair"

./rename.py "Pacific Appliance Repair" \
    --phone "(858) 555-0199" \
    --email service@pacificappliance.example \
    --area "Orange County"

./rename.py "Pacific Appliance Repair" --dry-run          # preview only
./rename.py "Pacific Appliance Repair" --only hvac-01-thermaline
```

The script rewrites files in place, so run it on a clean checkout (or a branch)
and review the diff. Escaping is context-aware: an ampersand in the company name
becomes `&amp;` in HTML and stays literal inside JSON-LD. Phone numbers are
replaced in all three forms they appear in — display, `tel:` href, and the
hyphenated form inside the JSON-LD.

Because the set now covers two markets, `--phone` and `--area` hit every site
unless you narrow them with `--only`. The per-city lists inside each page are
prose and still need editing by hand.

## Before going live

These are complete front-ends, but a few things are deliberately left as
placeholders for whoever deploys them:

1. **Form delivery.** Forms validate and show a confirmation, but post nowhere.
   Add `data-endpoint="https://…"` to the `<form>` element and the existing
   JavaScript will `POST` the `FormData` there — no other change needed. Any
   form backend, CRM webhook or serverless function will do.
2. **Phone numbers.** San Diego sites carry `(619) 555-0142` and Palm Springs
   sites `(760) 555-0142` — both reserved, non-working numbers. Replace it via `rename.py --phone` before launch, and
   ideally use a per-site tracking number so lead sources stay distinguishable.
3. **Licence numbers.** `CSLB #000000` is a placeholder. California requires the
   real licence number on advertising for contracted work over $500.
4. **Reviews, ratings and statistics.** The testimonials, star ratings, review
   counts and figures such as "87% first-visit fix rate" are illustrative
   sample copy. Replace them with real, attributable data — publishing invented
   reviews or ratings is deceptive advertising under FTC rules.
5. **Pricing.** The prices shown — including the published price table on
   `hvac-03-redalert` — are examples and must be set to your actual rates.
6. **Brand names.** `appliance-01-bluecrest` lists manufacturer names as plain
   text under "we service all major brands". No manufacturer logos or marks are
   used. Confirm any brand claim is accurate for your business before launch.
7. **Analytics and consent.** No tracking of any kind is included. Add your own
   analytics, call tracking and cookie notice as your jurisdiction requires.
8. **Trademarks on the Sub-Zero and Wolf sites.** `appliance-04-subzero-wolf`
   and `appliance-05-subzero-wolf-palm-springs` name both marques, which a repair company may do to describe the equipment
   it services (nominative fair use). To stay on the right side of that line the
   site uses no manufacturer logo, colour scheme or trade dress, and states its
   independence in three places: the top bar, the first FAQ answer, and the
   footer. **Keep those disclaimers** unless you actually hold factory
   authorization — in which case replace them with the real, current wording
   your agreement permits. The photography on those sites was also chosen to
   exclude visible manufacturer branding.

   Note separately that the two domains chosen for them —
   `subzero-maintenance.com` and `subzero-servicecenter.com` — put the
   trademark in the domain name itself. That is a materially weaker position
   than using it in body copy: brand owners police domains far more actively,
   and a domain incorporating another party's mark is the usual target of a
   UDRP complaint. Worth a trademark attorney's opinion before you build
   anything on top of them.

## Credits

See [CREDITS.md](CREDITS.md) for photography and font licensing.
