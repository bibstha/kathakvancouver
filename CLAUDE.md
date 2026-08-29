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
teaches: true                   # data only. The card no longer renders a badge,
                                # because every listing sets it.
tags:                           # optional. Rendered as one quiet meta line,
                                # joined by " · ", not as a row of pills.
  - Lucknow Gharana
  - Kids classes
---

A factual blurb (3–5 sentences). Public information only — no home addresses
or personal phone numbers. The blurb is shown on the homepage card.
```

The homepage sorts artists alphabetically by `name`.

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
---

Two or three factual sentences.
```

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

GitHub issues the Let's Encrypt certificate for the apex, and `CNAME` in the
repository root declares the domain. The apex is deliberately not proxied.
Cloudflare in front of Pages can break the HTTP-01 challenge that GitHub uses to
renew that certificate.

The certificate covers the apex only. A Cloudflare Redirect Rule answers `www`
at the edge with a 301 to the apex, so `www` never reaches GitHub. That rule
lives in the `http_request_dynamic_redirect` phase on the zone. The Cloudflare
token in `.env.local` needs DNS Edit and Single Redirect Edit.

## Editorial principles

- **Public information only** — websites, public Instagram, neighborhood-level
  location. Never home addresses or personal phone numbers.
- **Free** — no ads, no marketplace, no payment.
- **Removal on request** — anyone listed can ask to be edited or removed at
  `hello@kathakvancouver.com` (see `/submit/`).
- **Curated** — listings are added in good faith for any practising Kathak
  artist or teacher in the Lower Mainland.
