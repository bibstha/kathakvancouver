# Design study and styleguide

Source of the study: `https://darbar.org/` and `https://darbar.org/darbar-festival-2026/`,
read on 2026-08-29. Every number below is measured from the live pages, not
estimated. The method is in Part 1.

A live specimen of Part 4 is in `docs/styleguide-preview.html`. That page is
built in the system it documents, so every color, radius, button, and reveal on
it is the proposal running. Open it with:

```bash
python3 -m http.server 8099 --directory docs
# http://127.0.0.1:8099/styleguide-preview.html
```

This file has four parts.

1. How to read the design of a website. A repeatable checklist.
2. What Darbar does, measured against that checklist.
3. Why kathakvancouver.com looks machine-generated.
4. The proposed styleguide for kathakvancouver.com.

---

## Part 1: how to read the design of a website

Look at these ten things, in this order. The order matters. Layout and
typography decide how a page feels. Color and shape decide how it looks. Most
people study color first and learn the least useful thing.

For each item there is a question to answer and a way to measure the answer.

### 1. First screen and intent

**Ask:** What does the first screen ask you to do? What does it show?
**Method:** Screenshot the page before you scroll. Name the one action the
designer wants.

### 2. Layout system

**Ask:** How wide is the content column? Where are the side margins? Does any
element break out to the full width of the window?
**Method:**

```js
const el = document.querySelector('h1, h2');
const r = el.getBoundingClientRect();
const p = el.closest('[class*=container],[class*=wrapper],main');
[innerWidth, Math.round(r.left), p.className, Math.round(p.getBoundingClientRect().width)]
```

### 3. Vertical rhythm

**Ask:** How much empty space separates one section from the next? Is the
density the same from top to bottom, or does it change?
**Method:** Read `margin` and `padding` on each `<section>`. Compare the gap
between sections to the gap inside a section. A ratio of 3:1 or more reads as
generous. A ratio near 1:1 reads as cramped.

### 4. Typography

**Ask:** How many families? What is each one for? What is the size scale, the
weight at each size, and the line height at each size? How wide is a line of
body text?
**Method:**

```js
['h1','h2','h3','p'].map(t => {
  const e = document.querySelector(t); if (!e) return [t, null];
  const c = getComputedStyle(e);
  return [t, c.fontFamily.split(',')[0], c.fontSize, c.fontWeight, c.lineHeight];
})
```

The single most useful number is the ratio of `line-height` to `font-size` at
the largest size. Amateur pages leave it near 1.4. Designed pages pull it to
1.0 or 1.1 on display sizes.

### 5. Color

**Ask:** What is the ground? What is the ink? How many accents are there, and
what is the rule that decides where each one goes?
**Method:** Count every color on the page and sort by how often it appears.

```js
const hex = c => { const m = c.match(/[\d.]+/g); return m && m.length >= 3
  ? '#' + m.slice(0,3).map(n => Math.round(+n).toString(16).padStart(2,'0')).join('')
  : c };
const t = new Map(), b = new Map();
document.querySelectorAll('body *').forEach(el => {
  const c = getComputedStyle(el);
  t.set(c.color, (t.get(c.color)||0)+1);
  if (c.backgroundColor !== 'rgba(0, 0, 0, 0)')
    b.set(c.backgroundColor, (b.get(c.backgroundColor)||0)+1);
});
({ text: [...t].sort((a,b)=>b[1]-a[1]).slice(0,8).map(([c,n])=>[hex(c),n]),
   bg:   [...b].sort((a,b)=>b[1]-a[1]).slice(0,8).map(([c,n])=>[hex(c),n]) })
```

The rule matters more than the hues. "One accent per section" is a rule. "A
nice orange" is not.

### 6. Imagery

**Ask:** Does the page work without the photographs? If it does, the design is
carrying the page. If it does not, the photographs are carrying the page.
**Method:** Block images in the browser and reload. Then judge what is left.

### 7. Component anatomy

**Ask:** For each repeated block (card, list row, button, badge), what are the
parts, in what order, at what size?
**Method:** Draw the card as a list of parts from top to bottom. Write the
font size and weight beside each part.

### 8. Shape language

**Ask:** How many corner radii are in use? Which elements have a border, which
have a fill, which have a shadow?
**Method:** Count every `border-radius` value on the page.

```js
const r = new Map();
document.querySelectorAll('body *').forEach(el => {
  const v = getComputedStyle(el).borderRadius;
  if (v && v !== '0px') r.set(v, (r.get(v)||0)+1);
});
[...r].sort((a,b)=>b[1]-a[1])
```

Two or three values is a system. Seven values is an accident. One value used
on everything is a template.

### 9. Motion and state

**Ask:** What happens on scroll? What happens on hover? How long does a
transition take?
**Method:** Scroll slowly and screenshot mid-scroll. A heading caught halfway
through a reveal tells you the animation unit: the whole block, one line, or
one word.

### 10. Responsive shape

**Ask:** At what width does the layout change? What does a card become on a
phone?
**Method:** Resize to 390px wide and repeat items 2, 3, and 7.

---

## Part 2: what Darbar does

### 2.1 First screen

A full-bleed photograph of a musician fills the whole window. Three elements
sit on top of it at the left: a small label, a display heading, and one filled
pill button. There is no card, no box, and no border. The header floats above
the image with no background.

The first screen sells the feeling of a concert. It does not explain the
organization.

### 2.2 Layout

| Property | Value |
|---|---|
| Container | `.site-container`, `max-width: 1400px` |
| Window width measured | 1904px |
| Content left edge | 245px |
| Header | `position: fixed`, height 92px, `z-index: 99999` |
| Header background | `#f9f9f9` after scroll, transparent over the hero |

The container is wide. The side margins are large. Full-bleed images break out
of the container and touch both edges of the window.

### 2.3 Vertical rhythm

Sections use Tailwind spacing classes `my-40`, `my-50`, and `my-60`. A
section with a background band uses `padding: 90px 0`. The gap between
sections is far larger than any gap inside a section.

Sections alternate between white `#ffffff` and a band of `#f9f9f9`. Darbar
separates sections with a change of ground, not with a rule or a shadow.

### 2.4 Typography

One family carries the whole site: **Beatrice**, a contemporary grotesk. The
site loads weights 100 to 800, in roman and italic. There is no second family
for headings. The `darbar` wordmark is the single exception, and it is a
serif.

| Role | Size | Line height | Ratio | Weight |
|---|---|---|---|---|
| Display (`h1`) | 50px | 55px | 1.10 | 500 |
| Section head (`h2`) | 40px | 44px | 1.10 | 400 |
| Card title (`h3`) | 24px | 28.8px | 1.20 | 400 |
| List title (`h3`) | 18px | 19.8px | 1.10 | 500 |
| Body (`p`) | 16px | 24px | 1.50 | 400 |

Two facts drive the whole look:

- Large text is **light**, not bold. The 40px section head is weight 400.
- Large text is **tight**. The line height ratio is 1.10 at display sizes and
  1.50 at body size.

Body copy runs about 630px wide. That is close to 70 characters per line.

### 2.5 Color

| Token | Hex | Use |
|---|---|---|
| Ink | `#121212` | All body and heading text on light grounds |
| Muted ink | `#53565d` | Secondary text |
| Paper | `#ffffff` | Default section ground |
| Band | `#f9f9f9` | Alternate section ground, header after scroll |
| Pink | `#e279ce` | Accent, and the color of `d761c0` when hovered |
| Yellow | `#ffd901` | Festival primary. Buttons and full-bleed panels |
| Orange | `#ff6d00` | Section accent |
| Indigo | `#3041b5` | Section accent |
| Cyan | `#00a1e2` | Academy accent |

The rule is the interesting part. **Each section heading takes its own hue.**
Measured on the festival page, in page order:

| Section heading | Color |
|---|---|
| Countdown to the Darbar Festival 2026 | `#121212` |
| Milton Hall Concerts | `#d761c0` |
| Barbican Hall Concerts | `#ff6d00` |
| Lectures and Demonstrations | `#ffd901` |
| Yoga and Wellbeing | `#3041b5` |
| The venue | `#e279ce` |

The body text under every one of those headings stays `#121212`. The color
lands on the heading only. This gives a long page a sense of chapters without
any rules, boxes, or dividers.

The two sites use different primaries. The main site leads with pink. The
2026 festival page leads with yellow. The system survives the change because
the rule is "one saturated hue per section", not "our color is pink".

### 2.6 Imagery

Photography carries both pages. Every card leads with a photograph of a
performer. Every hero is a full-bleed photograph or video. The crops are
tight on faces and hands.

Remove the photographs and almost nothing is left. That is deliberate.

### 2.7 Component anatomy

**Event card (festival page)**

1. Photograph, `border-radius: 4px`, roughly 4:3
2. Optional pill badge over the top right of the image, for example `36% Sold`
   or `SOLD OUT`. White fill, pink text.
3. Title, 24px, weight 400, ink
4. A hairline rule
5. Date and venue on one row, small, bold, ink
6. Two pill buttons: `Buy Ticket` filled, `Read more` outlined

**Event list row (home page)**

1. Date block at the left. The day number is large. The month is small and
   uppercase under it.
2. Title, 18px, weight 500
3. `Read more` link with a long arrow
4. Square thumbnail at the right, about 100px
5. A hairline rule under the row

The list row and the card show the same event with different weight. Dense
lists get rows. Featured items get cards. The page never uses a card where a
row will do.

### 2.8 Shape

| Radius | Count | Use |
|---|---|---|
| `4px` | 32 | Images, panels, cards |
| `50px` | 21 | Buttons |
| `999px` | 11 | Badges, avatars |
| `5px` | 1 | One outlier |

Two shapes, not seven. Rectangles are almost square. Buttons are fully round.
There is nothing in between.

Buttons measured:

| Property | Value |
|---|---|
| `border-radius` | `50px` |
| `padding` | `10px 25px` |
| `font-size` | `16px` |
| `font-weight` | `500` |
| `border` | `1px solid`, same color as the fill |

The border matches the fill on a filled button. To make the outlined variant,
the fill turns white or transparent and the border keeps the accent. One rule
produces both buttons.

There are no drop shadows on cards. Separation comes from the ground color
and from whitespace.

### 2.9 Motion

Section headings are split into words before they animate. The markup is:

```html
<h2><div class="split-line"><div class="split-word">The</div>
<div class="split-word">venue</div></div></h2>
```

Each `.split-word` is `display: inline-block` and fades up with a stagger when
the heading scrolls into view. A screenshot taken mid-scroll catches
`Barbican Hall Concerts` with the three words at three different opacities.

This is the effect that most separates the page from a static template. It
costs about 30 lines of JavaScript and needs no library. Darbar loads no GSAP,
no AOS, and no Lenis.

---

## Part 3: why kathakvancouver.com looks machine-generated

This is a list of tells, not of faults. Each one is defensible alone. Together
they are the signature of a generated page.

| Tell | Current value | Why it reads as generated |
|---|---|---|
| Font pair | Playfair Display + Inter | The default pair of most templates and generators |
| Ground | `#fbf6ef` cream | "Warm neutral plus one muted accent" is the default generated palette |
| Accent | `#b3361f` terracotta | One desaturated warm accent, used for every link, badge, and mark |
| Avatar | A circle with the first letter of the name | A placeholder pattern. It announces that there is no photograph |
| Card | Every card is white, `14px` radius, same soft shadow | One radius on everything, and a shadow doing the work that space must do |
| Badges | A row of uppercase letter-spaced pills | Filler that adds visual noise and no hierarchy |
| Eyebrow | A pill above the `h1` reading `LOWER MAINLAND · BRITISH COLUMBIA` | A generated-hero convention |
| Icons | The emoji `📍` and the character `↗` | Emoji in place of an icon set |
| Grid | Three equal columns, every card the same size | No item is more important than any other, so the eye has nowhere to go |
| Blurbs | Every blurb truncated at 280 characters, ending in `...` | Uniform length, uniform shape, no editorial judgment |
| Density | One density from the header to the footer | No section is given room. Nothing breathes |
| Photography | None | The site is about dance and shows no dance |

The last row is the most serious. Kathak is a visual art. A directory of
Kathak artists with no photograph of a dancer cannot look like a Kathak site.
No change to color or type will fix that.

The second most serious is the display type. `h1` uses
`clamp(2rem, 4vw, 3rem)` at weight 700 with `line-height: 1.15`. Darbar uses
weight 500 at 50px with a ratio of 1.10. Heavy display type at a small size
reads as a document. Light display type at a large size reads as design.

---

## Part 4: the styleguide

### 4.1 What to borrow, and what not to

**Borrow the system:**

- One sans family for the whole site. Drop the serif-plus-sans split.
- Light weight and tight leading on large text.
- One saturated accent hue per section, on the section heading only.
- Two radii: near-square for images and panels, fully round for buttons.
- Alternating grounds instead of shadows.
- Pill buttons in a filled and an outlined variant, built from one rule.
- A list row for dense content and a card for featured content.
- A word-stagger reveal on section headings.
- Photography as the load-bearing element.

**Do not borrow:**

- The Beatrice typeface. It is a commercial font from Sharp Type.
- The Darbar hues. Yellow `#ffd901` with pink `#e279ce` is their brand.
- The wordmark.

### 4.2 Type

Use one family. **Schibsted Grotesk** is the closest free match to Beatrice.
It is a variable font on Google Fonts, weights 400 to 900, roman and italic.
Two alternates, both verified on Google Fonts, are **Familjen Grotesk** and
**Instrument Sans**. Both stop at weight 700.

```html
<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:ital,wght@0,400..900;1,400..900&display=swap" rel="stylesheet">
```

| Role | Size | Line height | Weight | Letter spacing |
|---|---|---|---|---|
| Display | `clamp(2rem, 6vw, 4rem)` | `1.05` | 500 | `-0.02em` |
| Section head | `clamp(1.75rem, 3.5vw, 2.5rem)` | `1.10` | 400 | `-0.01em` |
| Card title | `1.375rem` | `1.20` | 500 | `-0.01em` |
| Row title | `1.0625rem` | `1.25` | 600 | normal |
| Body | `1rem` | `1.55` | 400 | normal |
| Meta | `0.8125rem` | `1.4` | 600 | normal |

Body copy must not run wider than `68ch`.

### 4.3 Color

The hues below are chosen for Kathak, not copied from Darbar. Brass is the
color of ghungroo bells. Alta is the red dye that dancers apply to the feet
and the hands.

```css
:root {
  --ink:        #17130F;   /* all text on light grounds */
  --ink-muted:  #5C554D;   /* secondary text, meta rows */
  --paper:      #FFFFFF;   /* default section ground */
  --band:       #F5F2EC;   /* alternate section ground, header */
  --line:       #E4DED4;   /* hairline rules only */

  --brass:      #E0A012;   /* FILL only. Buttons. Ink sits on top of it. */
  --brass-ink:  #8A5D00;   /* TEXT variant. Section headings, links. */
  --alta:       #C42A46;   /* events section */
  --indigo:     #2E3C8F;   /* artists section */
  --leaf:       #2C6E52;   /* about and submit */
}
```

Brass needs two tokens. Measured contrast against white:

| Token | Ratio on white | Verdict |
|---|---|---|
| `--ink` `#17130F` | 18.1:1 | pass |
| `--ink-muted` `#5C554D` | 7.4:1 | pass |
| `--brass` `#E0A012` | 2.28:1 | **fails as text** |
| `--brass` with `--ink` on top | 8.2:1 | pass |
| `--brass-ink` `#8A5D00` | 5.7:1 | pass |
| `--alta` `#C42A46` | 5.6:1 | pass |
| `--indigo` `#2E3C8F` | 9.7:1 | pass |
| `--leaf` `#2C6E52` | 6.1:1 | pass |

Without `--brass-ink` the "one hue per section" rule has only two usable
heading colors, which is not enough for the page. With it there are four.

Rules:

1. All body text is `--ink`. All secondary text is `--ink-muted`. An accent
   never carries a paragraph.
2. One accent per section, applied to the section heading only.
3. `--brass` is the only accent allowed on a button.
4. A section is either `--paper` or `--band`. Neighboring sections must
   differ.
5. Never place `--brass` as text on white. Use `--brass-ink` for text. Brass
   is a fill color, and `--ink` sits on top of it.

### 4.4 Shape

| Token | Value | Use |
|---|---|---|
| `--r-flat` | `4px` | Images, panels, cards |
| `--r-pill` | `999px` | Buttons, badges |

There is no third radius. Delete `--radius: 14px` and `--radius-sm: 8px`.

Delete `--shadow`. Cards separate by whitespace and by ground color.

### 4.5 Layout

| Token | Value |
|---|---|
| `--maxw` | `1200px` |
| Gutter | `clamp(20px, 5vw, 64px)` |
| Section gap | `clamp(72px, 10vw, 128px)` |
| Band padding | `clamp(72px, 10vw, 128px)` top and bottom |

The current `1100px` container with `24px` padding is too narrow and too
tight. Widen the container and grow the gutter with the window.

Full-bleed images break the container and touch both edges.

### 4.6 Buttons

```css
.btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 11px 26px;
  border-radius: var(--r-pill);
  border: 1px solid transparent;
  font: 500 1rem/1 inherit;
  text-decoration: none;
}
.btn-primary { background: var(--brass); border-color: var(--brass); color: var(--ink); }
.btn-ghost   { background: transparent; border-color: var(--ink); color: var(--ink); }
```

One rule, two variants. The border is always present, so the two buttons are
the same height and sit on the same baseline.

### 4.7 Components

**Artist card**

1. Photograph, 4:3, `--r-flat`. When there is no photograph, use a flat block
   of the section accent at 12 percent opacity carrying one abstract motif.
   Do not use a letter in a circle. See 4.10.
2. Name, card title size
3. Neighborhood, meta size, `--ink-muted`
4. Blurb, body size, two lines, no ellipsis
5. Link row

Keep at most one badge per card, and only when it says something the blurb
does not. Delete the badge row.

**Event row**

1. Date block. Day number at `2rem` weight 500. Month at meta size, uppercase.
2. Title, row title size
3. Venue and price, meta size, `--ink-muted`
4. `Details and tickets` link with a long arrow
5. Hairline `--line` under the row

Rows, not cards. The site rarely has more than three events.

Below 640px the row stacks. The plate goes full width, and the body follows
under it. A 128px tile beside a tall body leaves an empty column under the
image and squeezes the blurb to about 200px. The stacked row matches the
artist card, which is already one full-width plate above its text.

### 4.8 Motion

Split every section heading into words and fade each word up with a stagger
when the heading enters the window. Use `IntersectionObserver`. Do not load a
library.

```css
.split-word {
  display: inline-block; opacity: 0; transform: translateY(0.4em);
  transition: opacity .5s ease, transform .5s ease;
}
.split-word.in { opacity: 1; transform: none; }
```

Stagger by adding the class per word on a timer, not with `transition-delay`:

```js
el.querySelectorAll('.split-word').forEach(function (w, i) {
  setTimeout(function () { w.classList.add('in'); }, i * 60);
});
```

Do not use `transition-delay` for the stagger. When the reveal fires on the
first paint, the delayed words keep a transition that never starts, and the
heading stops after its first word. The timer has no such failure.

Declare the `transition` on the base rule, not on the revealed state. A rule
that adds both the transition and the new value in one pass can skip the
animation.

Respect `prefers-reduced-motion: reduce`. Under that query, set every word to
full opacity with no transform and no transition.

### 4.9 The image problem, and how it was solved

The styleguide above needs photographs. The card and the event row are both
built around an image. The site had none.

Three options were on the table:

1. Ask each listed artist for one photograph and the right to publish it.
2. Use one full-bleed hero photograph and keep the cards text-only.
3. Keep the site text-only and drop the image slots.

The answer is 1 plus a fallback. Six of the seven listings now carry a real
image, published with the permission of the artist or the school. The last one
carries a motif (4.10) until a photograph arrives. The plate is the same shape
in both cases, so the grid holds one rhythm while the collection fills in.

Two rules stand. A photograph on a public website is not a license to
republish it, so ask first. Name the photographer when the name is known.

A survey of the seven listings found the real constraint. Only two listings
published a clean photograph. Two artists had no website at all. Two were on
Facebook only, behind a login. One school published a gallery of nineteen
frames, and every frame was a promotional flyer with a phone number and a QR
code across it. The other four images arrived by hand, from people the
maintainer meets.

A promotional banner is not a card image. Both banners offered here carried a
phone number, an email address, and a call-to-action button. A 4:3 crop of one
leaves a truncated phone number printed across the card. Crop the photograph
out of the banner, or use the logo, but never publish the banner whole. The
TheiTaal card is a crop of the one dancer in their banner who had no text over
her.

This is why the fallback is part of the system and not a patch. A grid that
assumed photographs would have failed on more than half of its cards on the
day it shipped.

### 4.10 Motifs

`assets/motifs/` holds five figures drawn from the Kathak vocabulary:

| File | Figure |
|---|---|
| `chakkar.svg` | Concentric rings around one still centre. The turn. |
| `ghungroo.svg` | Bells strung along two cords. |
| `teentaal.svg` | Sixteen beats. Sam ringed, the two tali filled, the khali hollow. |
| `tatkar.svg` | One bar per footwork syllable. Bar height follows the stress. |
| `chakradar.svg` | A spiral. One phrase unrolling three times over. |

Rules:

- Each file is black on transparent, and the CSS uses it as a `mask`, not as
  an image. The figure takes `--accent`, so it changes color with its section.
  A motif never carries a color of its own.
- One opacity, `.34`. The figure must read as a surface, not as an
  illustration competing with the name below it.
- The structure is information, not decoration. `teentaal.svg` marks the real
  sam, tali, and khali of the taal. `tatkar.svg` puts the tallest bar on the
  sam. Do not add a sixth motif that only looks like the others.
- A card picks by position in the grid, so no two neighbors repeat. An event
  picks by day of month, so an event keeps one motif for its whole life.

Five is deliberate. The grid never exceeds three columns at `--maxw`, and five
shares no factor with one, two, or three, so no motif ever sits directly above
another of the same kind.

### 4.11 Image widths

Every photograph ships in three widths, 400, 600 and 900, built by
`tools/make-image.py`. The `srcset` and `sizes` attributes in `index.html`
carry all three, so the browser downloads one.

The widths come from the plates, not from a habit:

| Plate | CSS width | 1x | 2x | 3x |
|---|---|---|---|---|
| Card, wide screen | 336 | 400 | 900 | 900 |
| Card, one column | ~331 | 400 | 900 | 900 |
| Event tile, wide screen | 240 | 400 | 600 | 900 |
| Event tile, narrow | ~350 | 400 | 900 | 900 |

The rule behind the table: a plate is small and fixed, so the file must be
small and fixed too. A 240 pixel tile served a 1000 pixel file wastes about
four fifths of the bytes it downloads, and no viewer ever sees the difference.
Measure the plate first, then pick the widths.

Give every `img` a `width`, a `height`, `loading="lazy"` and
`decoding="async"`. The plate already holds its own shape through
`aspect-ratio`, so the page never moves while an image arrives.
