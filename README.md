# Kathak Vancouver

A friendly directory of Kathak artists and teachers across the Lower Mainland.

Live at **https://kathakvancouver.com**.

## Stack

- **Jekyll 4** static site (no theme — single layout, hand-written CSS).
- Artists are a Jekyll collection at `_artists/*.md`. Each file is one card on the
  homepage.
- Events are a Jekyll collection at `_events/*.md`. The homepage lists upcoming
  events above the directory. It hides the section when no event is upcoming.
- Filtering is plain vanilla JS — toggle `data-neighborhood` classes on cards.
- Built and deployed by GitHub Actions to GitHub Pages.

## Local development

```bash
mise install                                  # ruby 4.0.6
bundle install
bundle exec jekyll serve                      # http://localhost:4000
```

Add an artist by dropping a markdown file in `_artists/`:

```yaml
---
name: Artist Name
neighborhood: Surrey            # one of the values in _config.yml `neighborhoods`
website: https://example.com
instagram: their_handle         # optional, no @
teaches: true
tags:
  - Optional
  - Tags
---

A short, factual blurb (3–5 sentences). Public information only.
```

Add an event by dropping a markdown file in `_events/`:

```yaml
---
title: Kathak Recital by Example Academy
date: 2026-09-14                # required, YYYY-MM-DD
end_date: 2026-09-16            # optional, for a multi-day event
time: "7:00 PM"                 # optional
venue: Bell Performing Arts Centre
neighborhood: Surrey            # display only, no filter
host: Example Academy           # optional
link: https://example.com/tick  # optional. Not `url`. See the note below.
price: "$25"                    # optional
---

Two or three factual sentences.
```

Do not name the link field `url`. Jekyll defines `url` on every document. It
overrides a front matter key with the same name, and it reports no error.

An event stays in the list for the whole of its last day. Liquid computes the
cutoff at build time, so the site must rebuild every day. See
[`CLAUDE.md`](./CLAUDE.md).

Adding a brand-new neighborhood? Add it to `neighborhoods:` in `_config.yml` so
the filter button shows up in the recommended order. Otherwise it'll appear at
the end automatically.

## Deployment

```bash
git push origin main
```

GitHub Actions builds the site and publishes it to GitHub Pages. The workflow is
`.github/workflows/pages.yml`. A push reaches the live site in about one minute.
There is no deploy script and no server.

The same workflow runs every day at 15:00 UTC. That daily build is what makes
past events drop off the homepage, because Liquid computes the cutoff at build
time. Do not remove the `schedule:` trigger.

To publish without a code change:

```bash
gh workflow run pages.yml --repo bibstha/kathakvancouver
```

### Domain

`kathakvancouver.com` points at GitHub Pages with A and AAAA records, DNS-only
in Cloudflare. GitHub issues the certificate, and the `CNAME` file declares the
domain. `www` is proxied by Cloudflare and a Redirect Rule sends it to the apex
with a 301.

## Data principles

- Public information only — no home addresses, no personal phone numbers.
- Listings are free; no ads, no marketplace.
- Anyone listed can request removal or correction at any time — see `/submit`.
