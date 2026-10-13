# New Ground AI website

GitHub Pages site for New Ground AI: **Advanced · Analytical · Adaptive · Adventurous · Aspiring**.

Shared look and feel lives in `assets/css/site.css`, `assets/js/site.js`, and `_includes/`. Visual tokens are documented in `brand-spec.md`.

## Content model

```text
Nav: Home · People · Publication

Projects:            on-going `_projects/*.md`  +  published `projects/<slug>/index.html`
People:              `_people/*.md`  →  Home / People cards  →  `/people/<slug>/`  →  optional `website`
```

- **On-going projects** use the shared Markdown layout and URLs `/projects/<slug>/`.
- **Published projects** are free HTML. YAML is only for directories (Projects, Publication, homepage ticker).
- **People intros** are Markdown in `_people/`. Portraits always open that page. A `website` field is linked from the intro, not from the card.
- Publication and the homepage ticker list pages with `status: published` and `listed: true`, newest `date` first.

## Update each section

Most page *introductions* are a short lead on that HTML page. Lists under them are generated from YAML — edit the source project or member, not the listing page.

### Home — `index.html`

| What you see | Where to edit |
| --- | --- |
| Eyebrow, `New Ground AI` title, five-A line | `.hero__copy` |
| Overview paragraph | `.hero__overview p` |
| Latest Publication ticker | Automatic: newest 5 published pages. Cards show **year, title, venue** (no authors). |
| Research themes | `_data/research_themes.yml` |
| People sentences | `.people-intro` |

To change ticker copy, edit the published project’s YAML (`title`, `year`, `venue`, `date`). To hide a paper from Home and Publication, set `listed: false`.

### People — `_people/`

Everyone has a **community intro** at `/people/<slug>/`, generated from `_people/<slug>.md`. Home and People portraits always open that page. A personal homepage — GitHub Pages or a folder on this site — is only a **Personal site** link on the intro. Do not list papers on the intro; keep it to portrait, facts, links, and a short bio.

| What you see | Where to edit |
| --- | --- |
| People page title and lead | `people/index.html` |
| Honeycomb | Every `_people/*.md` with `listed: true` |
| Community intro | `_people/<slug>.md` |

**Every member starts the same way.** Create `_people/<slug>.md` (for example `_people/ye-yuan.md`). Put a photo at `assets/images/people/<slug>.jpg` when you have one. Then choose A or B below for the personal site.

| Field | Required | What it does |
| --- | --- | --- |
| `title` | yes | Name on cards and the intro |
| `role` | yes | Role line (Ph.D. Candidate, …) |
| `institution` | yes | School / community line |
| `focus` | yes | Short research focus on the card |
| `listed` | yes | `true` to show in the People honeycomb |
| `portrait` | no | Path such as `/assets/images/people/ye-yuan.jpg` |
| `email` | no | Mailto link on the intro |
| `website` | no | Personal site — see A and B |
| `scholar` / `github` / `cv` | no | Extra links on the intro |
| Markdown body | no | Short biography under the facts |

#### A. They already have a GitHub (or other) homepage

Do **not** create a folder under `people/`. Only the Markdown file. Set `website` to the live URL.

```yaml
title: Ye Yuan
role: Ph.D. Candidate
institution: McGill University · Mila
focus: Generative AI · BBO · Agents
email: ye.yuan3@mail.mcgill.ca
portrait: /assets/images/people/ye-yuan.jpg
website: https://stevenyuan666.github.io/
scholar: https://scholar.google.com/citations?user=lemEc74AAAAJ
github: https://github.com/StevenYuan666
cv: https://stevenyuan666.github.io/assets/pdf/CV_Ye_YUAN_2026.pdf
listed: true
```

```text
Click portrait  →  /people/ye-yuan/                 (this community’s intro)
Personal site   →  https://stevenyuan666.github.io/ (their GitHub Pages)
```

Add `scholar`, `github`, or `cv` the same way if they have them. Omit any they do not have.

#### B. They will design a homepage in this repo

Still create `_people/<slug>.md`. Then add a **separate** HTML site under `people/<slug>/site/` so it does not collide with the intro at `/people/<slug>/`.

1. Copy `people/member-template/` to `people/<slug>/site/`.
2. In that folder’s `index.html`, set:

```yaml
layout: null
nav: people
permalink: /people/<slug>/site/
```

3. Design the page freely (own CSS, JS, layout). Shared community chrome is optional.
4. In `_people/<slug>.md`, set `website` to that **path**, not an `https://` URL:

```yaml
title: Example Name
role: Ph.D. Student
institution: McGill University · Mila
focus: Agents
portrait: /assets/images/people/example-name.jpg
website: /people/example-name/site/
listed: true
homepage: false
```

```text
Click portrait  →  /people/example-name/      (community intro)
Personal site   →  /people/example-name/site/ (their HTML in this repo)
```

Do not use `permalink: /people/<slug>/` on the custom HTML. That address is reserved for the Markdown intro.

#### C. No personal homepage yet

Omit `website`. Portraits still open the community intro; that page has no Personal site link. Add `website` later using A or B.

To add a member: `_people/<slug>.md` + optional portrait + A, B, or C.

### Research themes — homepage

The six homepage themes live in `_data/research_themes.yml`. Each item needs `id`, `title`, `lead`, and `summary`. They are not linked to separate pages.

### Publication — `publication/index.html`

| What you see | Where to edit |
| --- | --- |
| Directory title and lead | `.page-hero` |
| Paper cards | Automatic from published YAML. Cards show **year, title, venue, keywords** (same format as Home). |

Papers split into **Conferences & Journals & Workshops** and **arXiv Preprint**. A venue containing `arXiv` goes to preprints; set `publication_group: venue` or `publication_group: preprint` to override.

There is no separate publication database. Add or edit `projects/<slug>/index.html` instead.

### Projects — `projects/index.html`

| What you see | Where to edit |
| --- | --- |
| Directory title and lead | `.page-hero` |
| Filters and cards | Automatic from `_projects/` plus published HTML |

Search matches title, summary, area, keywords, members, authors, and venue.

### Shared chrome

| What you see | Where to edit |
| --- | --- |
| Header wordmark | `_includes/site-mark.html`, logo at `assets/images/brand/` |
| GitHub / Hugging Face | `_includes/site-presence.html` |
| Nav labels and order | `_includes/site-nav.html` |
| Footer line | `_includes/site-footer.html` |
| Browser tab icon | `_includes/head-icons.html` and `assets/images/brand/favicon.png` (transparent PNG) |

Site-wide five-A wording also appears in `_config.yml` (`description`) and the footer.

## Add an on-going project

Copy `_projects/ongoing-project-template.md` to `_projects/your-slug.md`. Keep the `Overview`, `Motivation`, and `Goals` headings.

```yaml
title: Project title
status: ongoing
research_area: BBO
research_area_slug: bbo
keywords:
  - Keyword
members:
  - Member name
summary: Short introduction used on cards.
```

The page is generated at `/projects/your-slug/`.

## Add a published project

Create `projects/your-slug/index.html`. `projects/project-template/` is a starting point (`listed: false`, so it stays out of catalogs).

Directories only read the YAML. The HTML body can be anything: custom CSS, Canvas, WebGL, video, or a layout that does not look like the rest of the site.

```yaml
layout: null
nav: projects
status: published
listed: true
date: 2026-05-26
permalink: /projects/your-slug/
title: Paper or project title
year: 2026
summary: Short introduction used on project cards.
research_area: Social Deduction
research_area_slug: social-deduction
authors:
  - First Author
members:
  - Community member on the card
venue: EMNLP 2026 Main Conference
publication_group: venue
keywords:
  - Keyword
```

| Field | Used by |
| --- | --- |
| `listed: true` | Home ticker, Publication, Projects catalog |
| `date` | Sort order (newest first) |
| `year` | Card year label |
| `venue` | Ticker (venue only) and Publication cards |
| `publication_group` | Optional. `preprint` or `venue`. If omitted, a venue containing `arXiv` is treated as a preprint |
| `authors` / `members` | Publication cards and project cards |
| `research_area_slug` | Projects area filter |

Set `listed: false` for drafts and templates.

## Local development

Ruby 3.4 and Bundler are required.

```powershell
bundle install
bundle exec jekyll serve --port 4000
```

Open `http://127.0.0.1:4000/`.

On Windows the file watcher often misses CSS and includes. If a change does not appear, rebuild:

```powershell
bundle exec jekyll build
```

Then refresh the browser (hard-refresh if the tab icon looks stale).

Restart `jekyll serve` after editing `_config.yml`. The watcher does not reload collections, so People can render empty until the server is restarted.

## Search discovery and indexing

The tracked root `sitemap.xml` is a Liquid template. Jekyll renders it into
`_site/sitemap.xml` at build time and deploys it at `/sitemap.xml`; `_site/` stays
untracked. `jekyll-sitemap` detects this template and does not replace it. The
production origin is set in `_config.yml`; `/robots.txt` allows crawling and
declares that sitemap.
Formal pages use `_includes/seo-canonical.html` once inside their `<head>`.
The homepage adds `WebSite` and `Organization` JSON-LD through
`_includes/home-identity.html`. Keep its name, logo, canonical URL, and verified
profiles consistent with the visible site. Its description comes from homepage
front matter. Shared Home and wordmark links point directly to `/`. Reveal
animations enhance content that is visible by default, including without JavaScript.
The `/projects/` redirect declares `/publication/` as its canonical and uses
`sitemap: false`. Google ownership verification stays published, unchanged,
and is omitted from the sitemap.

The template keeps the plugin's URL inclusion rules but only emits `<lastmod>`
when content supplies an explicit `last_modified_at` date. Update that field
only after a significant change to content, structured data, or links. If a
reliable modification date is unknown, omit it. Do not substitute a build time,
file checkout time, or the paper's publication date: those can falsely suggest
that unchanged pages were updated on every deployment.

A valid live sitemap does not guarantee that Google has fetched or processed
it. If Search Console reports "Couldn't fetch", inspect the sitemap's error
details and run its live URL test; a successful browser request alone does not
resolve Google's report. Follow the [official troubleshooting steps](https://support.google.com/webmasters/answer/7451001).

The sitemap lists HTML content pages, not resume PDFs. Rui Song's reserved Talk
and Service pages remain accessible but use `sitemap: false` and `noindex: true`.
When those sections contain real content, remove those two flags, link the pages
from navigation, and update the explicit `NOINDEX` allowlist in the checker.

`listed: false` only hides a page from content lists. It does **not** prevent
publication or indexing. The reusable project and member templates are excluded
from the build by their exact source paths in `_config.yml`. Copy a template to
a new slug to publish a real page; keep private drafts outside the published
source or explicitly exclude them.

Published papers keep their formal `title` for lists and the visible subtitle.
An optional `seo_title` supplies a concise browser/search title. Render authors
with `_includes/paper-authors.html`: exact profile names link automatically;
verified name variations belong in the member's `author_names` list. Authors
without a matching profile remain plain text. `equal_contributors` preserves
the paper's contribution markers.

After a production build, run:

```powershell
bundle exec jekyll build
python scripts/check_seo.py _site
```

The checker validates homepage identity metadata, sitemap coverage, canonical targets, indexing directives,
robots rules, content links, navigation from Home, and the verification file.
It derives required member/project URLs from source files instead of fixing a
member count. Pull requests run the same checks without deploying. Only a
successful build from `main` can deploy.

## Deployment

Push to `main` to run `.github/workflows/pages.yml`. The workflow builds the Jekyll source and deploys `_site` to GitHub Pages.

Do not commit `_site/`, `.agents/`, or `skills-lock.json`.
