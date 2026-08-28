# Repair services lead-generation sites

Eight standalone marketing sites for home-services companies — **four for appliance
repair** and **four for HVAC repair** — each built as a separate, self-contained
static site with its own brand, palette, typography and page structure.

All seven currently advertise **San Diego County, California** as the service area,
and every company name is the placeholder `<name>`. Both are swapped with one
command — see [Renaming](#renaming).

## The sites

| Directory | Trade | Design direction |
|---|---|---|
| `sites/appliance-01-bluecrest` | Appliance | Clean corporate blue. Split hero with a sticky quote card, photo service grid, three-step process. |
| `sites/appliance-02-boltyellow` | Appliance | High-contrast black and amber. Full-bleed photo hero with an inline quick-quote bar, scrolling ticker, photo tiles. |
| `sites/appliance-03-hearth` | Appliance | Warm cream and forest green, serif headlines. Circular service photos, testimonial-led, family-shop tone. |
| `sites/appliance-04-subzero-wolf` | Appliance | Restrained luxury in bone and brass, Cormorant serif. Sub-Zero and Wolf specialist — three service pillars, a fault index and a maintenance programme. |
| `sites/hvac-01-thermaline` | HVAC | Cool-to-warm gradient. Floating capsule nav, paired cooling/heating panels, horizontal process timeline. |
| `sites/hvac-02-nocturne` | HVAC | Dark premium with cyan accents. Glass form card, bento service grid, three pricing plans. |
| `sites/hvac-03-redalert` | HVAC | Emergency red utility. Square borders, published flat-rate price table, dense information layout. |
| `sites/hvac-04-sundesert` | HVAC | Sand and terracotta editorial. Magazine collage hero, drop-cap essay, numbered service spreads. |

Open `index.html` at the repository root for a gallery linking to all eight.

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
becomes `&amp;` in HTML and stays literal inside JSON-LD.

## Before going live

These are complete front-ends, but a few things are deliberately left as
placeholders for whoever deploys them:

1. **Form delivery.** Forms validate and show a confirmation, but post nowhere.
   Add `data-endpoint="https://…"` to the `<form>` element and the existing
   JavaScript will `POST` the `FormData` there — no other change needed. Any
   form backend, CRM webhook or serverless function will do.
2. **Phone numbers.** Every site ships with `(619) 555-0142`, a reserved
   non-working number. Replace it via `rename.py --phone` before launch, and
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
8. **Trademarks on the Sub-Zero and Wolf site.** `appliance-04-subzero-wolf`
   names both marques, which a repair company may do to describe the equipment
   it services (nominative fair use). To stay on the right side of that line the
   site uses no manufacturer logo, colour scheme or trade dress, and states its
   independence in three places: the top bar, the first FAQ answer, and the
   footer. **Keep those disclaimers** unless you actually hold factory
   authorization — in which case replace them with the real, current wording
   your agreement permits. The photography on that site was also chosen to
   exclude visible manufacturer branding.

## Credits

See [CREDITS.md](CREDITS.md) for photography and font licensing.
