# Kathak Vancouver

A community-curated, static directory of Kathak artists and teachers across the
Lower Mainland of British Columbia.

## Architecture

**Static Jekyll site, no database.** All data lives as markdown.

- **Generator:** Jekyll 4 (no theme — single hand-written layout in `_layouts/`)
- **Data:** one markdown file per artist in `_artists/`. One per event in
  `_events/`. Both are Jekyll collections.
- **Filter:** vanilla JS, toggling `data-neighborhood` on cards (no framework)
- **Styling:** plain CSS in `assets/css/main.css`, one typeface (Schibsted
  Grotesk). The design system is documented in `docs/styleguide.md`. Read that
  file before you change color, type, spacing, or shape. It carries the rules
  and the reasons, including why brass has two tokens and why the heading
  reveal does not use `transition-delay`.
- **Hosting:** GitHub Pages, built and deployed by GitHub Actions
- **Domain:** `kathakvancouver.com`, DNS on Cloudflare

### Key files

```
_artists/*.md           # one card per file
_events/*.md            # one event card per file. Can be absent.
assets/artists/*.jpg    # one photograph or logo per listing, in 3 widths
assets/events/*.jpg     # one photograph per event, in 3 widths
assets/motifs/*.svg     # five abstract Kathak figures, the fallback graphic
tools/make-image.py     # builds the 3 widths from one source file
_config.yml             # neighborhoods filter order, timezone, site metadata
_layouts/default.html   # site shell (header, nav, footer)
_layouts/page.html      # for /about and /submit
index.html              # homepage: events, then artist grid and filter
about.md                # /about/
submit.md               # /submit/
assets/css/main.css     # all styling
assets/favicon.svg
docs/styleguide.md      # the design system, and how it was derived
docs/styleguide-preview.html  # live specimen of the system. Not published.
CNAME                   # the custom domain, copied into _site/ by Jekyll
.github/workflows/pages.yml  # build and deploy, plus the daily rebuild
mise.toml               # ruby 4.0.6
```

### Adding an artist

Drop a file in `_artists/` (filename = slug used for sorting if `name` is the
same). Frontmatter:

```yaml
---
name: Artist Name
neighborhood: Surrey            # must match a label in _config.yml `neighborhoods`
                                # — or any new value, which appears as a filter button
website: https://example.com    # optional
instagram: their_handle         # optional, no @
youtube: https://...            # optional
teaches: false                  # data only. The card renders no badge, and the
                                # blurb does not state it either. A listing that
                                # does not teach simply says nothing about
                                # teaching.
image: artist-slug              # optional. Names a set of 3 widths in
                                # assets/artists/. No extension, no path.
                                # Without it the card shows a motif.
tags:                           # optional. Rendered as one quiet meta line,
                                # joined by " · ", not as a row of pills.
  - Lucknow Gharana
  - Kids classes
---

A factual blurb (3–5 sentences). Public information only — no home addresses
or personal phone numbers. The blurb is shown on the homepage card.
```

The homepage sorts artists alphabetically by `name`.

### Card and event graphics

Every card and every event row leads with a 4:3 plate. The plate holds a
photograph when the listing has one, and an abstract motif when it does not.

**Photographs.** Build the files with `tools/make-image.py`, then set `image:`
to the slug. The slug names a set of three widths, so it carries no extension
and no path.

```bash
tools/make-image.py ~/photo.jpg assets/artists/artist-slug --fit
tools/make-image.py ~/photo.jpg assets/artists/artist-slug --crop 0,220,1711,1503
tools/make-image.py ~/logo.jpg  assets/artists/artist-slug --pad
```

`--fit` centre-crops to 4:3. `--crop` takes a box that is already 4:3, for when
the centre is the wrong place to cut. `--pad` contains a logo on a white
ground. Each run writes `slug-400.jpg`, `slug-600.jpg` and `slug-900.jpg`.

Never hand a full-resolution file to the page. A card plate is at most 340 CSS
pixels wide. An event tile is 240 on a wide screen, and full width below 640px,
where the row stacks. The `srcset` in `index.html` lets the browser take 400 on
a plain screen and 900 on a 2x screen. Add a width to `WIDTHS` and to both
`srcset` attributes together, or not at all.

Two rules govern what goes in:

1. Ask the artist before you publish a photograph of them. A photograph on a
   public website is not a license to republish it.
2. Name the photographer in `credit:` when you know the name. The event row
   renders it as one quiet line. A logo needs no credit.

A school with no performance photograph can use its logo. `--pad` trims the
border and centres the logo on white, so it fills the same plate as a
photograph. `ghungroo-kathak-academy` is the example.

**Motifs.** `assets/motifs/` holds five abstract figures from the Kathak
vocabulary: `chakkar` (the turn), `ghungroo` (bells on a cord), `teentaal`
(sixteen beats, with sam, tali, and khali marked), `tatkar` (one bar per
footwork syllable) and `chakradar` (a phrase unrolling). Each is black on
transparent, and the CSS uses it as a mask, not as an image. The figure
therefore takes `--accent` and changes color with its section. Do not give a
motif a fill color of its own.

A card with no photograph picks its motif by position in the grid, so no two
neighbors repeat. An event picks by day of month, so its motif never changes.

Amika Kushwaha is the one listing that still needs a photograph.

### Adding an event

Drop a file in `_events/`. Create the directory if it does not exist. Git does
not track an empty directory. Jekyll builds correctly without it.

```yaml
---
title: Kathak Recital by Example Academy
date: 2026-09-14                # required, YYYY-MM-DD
end_date: 2026-09-16            # optional, multi-day event
time: "7:00 PM"                 # optional, free text
venue: Bell Performing Arts Centre
neighborhood: Surrey            # display only. Events have no filter.
host: Example Academy           # optional
link: https://example.com/tick  # optional, tickets or info
price: "$25"                    # optional, "Free" is fine
image: 2026-09-14-recital       # optional, a set in assets/events/
credit: Photographer Name       # optional, shown under the event
---

Four to eight factual sentences. Give the reader the detail that the poster
and the box office carry: who dances, who plays, who composed and directed the
work, the running time, the street address, and every way to book. Research
the artists outside the source post and name their training and their gurus.
```

An event may carry a phone number when the poster or the box office prints one
for booking. That number is published for the event, so it is not a personal
contact. The rule against personal phone numbers still holds for an artist
listing in `_artists/`.

**Do not name the link field `url`.** Jekyll defines `url` on every document.
A front matter `url:` is ignored, and the rendered link points to a
`/events/<slug>/` page that does not exist. The field is `link` for this reason.

Events sort by `date`, ascending. An event stays in the list for the whole of
its last day. The last day is `end_date`, or `date` when there is no `end_date`.
The homepage hides the events section when no event is upcoming. This is the
normal state when `_events/` is empty. Events have no filter buttons.

## Development

```bash
mise install                       # ruby 4.0.6
bundle install
bundle exec jekyll serve           # http://localhost:4000
```

If `bundle` fails with a version error, install the matching bundler first:
`mise exec -- gem install bundler:2.6.9`.

`Gemfile.lock` is in git on purpose. The workflow uses `bundler-cache: true`,
which needs the lock to restore the cache and to install the same gem versions
that you use locally. Do not add `Gemfile.lock` back to `.gitignore`.

`mise.toml` pins Ruby 4.0.6. The workflow pins the same version. If you change
one, change the other.

## Deployment

GitHub Actions builds the site and deploys it to GitHub Pages. There is no
deploy script and no server to manage.

```bash
git push origin main
```

That is the whole procedure. The workflow at `.github/workflows/pages.yml`
builds with Jekyll and publishes the result. A push takes about one minute to
reach the live site.

To deploy without a code change, run the workflow by hand:

```bash
gh workflow run pages.yml --repo bibstha/kathakvancouver
gh run watch $(gh run list --repo bibstha/kathakvancouver --limit 1 --json databaseId --jq '.[0].databaseId') --repo bibstha/kathakvancouver
```

### Nightly rebuild (required for events)

Liquid computes the upcoming and past cutoff at build time against `site.time`.
The served page does not read the date again. A past event stays on the homepage
until the next build.

The workflow holds a `schedule:` trigger at 15:00 UTC every day. That is 08:00
in Vancouver during summer time and 07:00 in winter. The daily run is what makes
past events drop off. Do not remove it.

GitHub disables scheduled workflows in a repository with no activity for 60
days. If events stop expiring, look at this first.

### Domain and TLS

| Name | Handling |
|---|---|
| `kathakvancouver.com` | 4 A records and 4 AAAA records to GitHub Pages. DNS-only in Cloudflare. |
| `www.kathakvancouver.com` | CNAME to `bibstha.github.io`, proxied by Cloudflare. |
| `vancouverkathak.com` | Its own Cloudflare zone. Apex and `www` are A records to `192.0.2.1`, proxied. |

GitHub issues the Let's Encrypt certificate for the apex, and `CNAME` in the
repository root declares the domain. The apex is deliberately not proxied.
Cloudflare in front of Pages can break the HTTP-01 challenge that GitHub uses to
renew that certificate.

The certificate covers the apex only. A Cloudflare Redirect Rule answers `www`
at the edge with a 301 to the apex, so `www` never reaches GitHub. That rule
lives in the `http_request_dynamic_redirect` phase on the zone. The Cloudflare
token in `.env.local` needs DNS Edit and Single Redirect Edit.

`vancouverkathak.com` is a second domain that redirects to this one. It is a
separate Cloudflare zone with no origin. The apex and `www` are proxied A
records to `192.0.2.1`, an address that carries no traffic. A Redirect Rule in
the `http_request_dynamic_redirect` phase of that zone answers both hostnames
with a 301 to `https://kathakvancouver.com`, and keeps the path and the query
string. The request never leaves the Cloudflare edge, so the site needs no
`CNAME` entry and no second certificate.

## Editorial principles

- **Public information only** — websites, public Instagram, neighborhood-level
  location. Never home addresses. Never a personal phone number in an artist
  listing. An event may carry the booking number that its poster or its box
  office prints, because that number is published to sell tickets.
- **Free** — no ads, no marketplace, no payment.
- **Removal on request** — anyone listed can ask to be edited or removed at
  `hello@kathakvancouver.com` (see `/submit/`).
- **Curated** — listings are added in good faith for any practising Kathak
  artist or teacher in the Lower Mainland.
