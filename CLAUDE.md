# Kathak Vancouver

A community-curated, static directory of Kathak artists and teachers across the
Lower Mainland of British Columbia.

## Architecture

**Static Jekyll site, no database.** All data lives as markdown.

- **Generator:** Jekyll 4 (no theme — single hand-written layout in `_layouts/`)
- **Data:** one markdown file per artist in `_artists/`. One per event in
  `_events/`. Both are Jekyll collections.
- **Filter:** vanilla JS, toggling `data-neighborhood` on cards (no framework)
- **Styling:** plain CSS in `assets/css/main.css` (Playfair Display + Inter)
- **Runtime:** `nginx:alpine` serving the built `_site/`
- **Hosting:** Coolify on the Homelab server

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
Dockerfile              # multi-stage: jekyll build → nginx
nginx.conf              # serves _site/, gzip on, sensible cache headers
bin/deploy              # triggers Coolify deploy via API, polls until done
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
teaches: true                   # shows the green "Teaches" badge
tags:                           # optional badges
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

`Gemfile.lock` is in git on purpose. The Dockerfile copies it before
`bundle install`, so the image installs the locked versions. Without the file,
the image resolves the newest gems. `COPY . .` then adds a lock that names
different versions, and the build fails with `Bundler::GemNotFound`. Do not add
`Gemfile.lock` back to `.gitignore`.

Test the docker image locally:

```bash
docker build -t kathakvancouver .
docker run --rm -p 8080:80 kathakvancouver
# open http://localhost:8080
```

## Deployment

Deployment details, server addresses, and Coolify identifiers are in
`DEPLOYMENT.local.md`. That file is gitignored and stays on the maintainer
machine.

The short form:

```bash
git push origin main && bin/deploy
```

`bin/deploy` reads `.env`, calls the Coolify API, and polls until the deploy
finishes. It usually takes about 2 minutes. `.env` is gitignored. See
`.env.example` for the shape.

### Nightly rebuild (required for events)

Liquid computes the upcoming and past cutoff at build time against `site.time`.
The served page does not read the date again. A past event stays on the homepage
until the next build. A daily rebuild keeps the event list correct.

Two conditions must hold:

1. **A daily job must trigger a build.** The Coolify server is on a private
   network, so a hosted runner cannot reach it. The cron entry belongs on that
   network. The exact line is in `DEPLOYMENT.local.md`.

2. **The Docker build cache must be off for this app.** The build stage runs
   `COPY . .` and then `RUN bundle exec jekyll build`. On an unchanged git SHA,
   Docker reuses that cached layer. The image then ships an identical site with
   a frozen `site.time`. The daily job runs and changes nothing, and it reports
   no error. After the first nightly run, make sure that the date moved.

Until both conditions hold, delete a past event by hand. If you do not, it stays
on the homepage.

## Editorial principles

- **Public information only** — websites, public Instagram, neighborhood-level
  location. Never home addresses or personal phone numbers.
- **Free** — no ads, no marketplace, no payment.
- **Removal on request** — anyone listed can ask to be edited or removed at
  `hello@kathakvancouver.com` (see `/submit/`).
- **Curated** — listings are added in good faith for any practising Kathak
  artist or teacher in the Lower Mainland.
