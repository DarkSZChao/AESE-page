# AESE group website

A fully English static website based on the [AESE group website](https://wp.doc.ic.ac.uk/aese/), captured on 6 October 2026. Its academic layout takes inspiration from [ARPG](https://arpg.colorado.edu/), with an independent deep-blue palette and AESE's own content. Main sections are Research, People, Publications, Resources and Contact. Historical research information and biographies have **not** been independently updated.

## Preview locally

Open this folder in PyCharm and **right-click `preview.py` → Run**. The script builds the website and opens **http://127.0.0.1:8000/**. Stop the run to stop the server. Python 3.10+ is sufficient; no additional packages, Node.js, WordPress or database are needed.

Preview settings are at the bottom of `preview.py`. Change `port` if 8000 is already in use. After editing source files, run `build_site.py` again and refresh the browser. You can also open `site/index.html` directly after building; internal links include `index.html` so they work without a server.

## Edit the website

| Location | Purpose |
| --- | --- |
| `content/pages/index.html` | Homepage introduction, carousel and featured sections |
| `content/pages/research/index.html` | Research overview and searchable project directory |
| `content/pages/people/index.html` | Searchable, filterable people directory |
| `content/pages/news/index.html` | Recognition and archived announcements |
| `content/pages/publications/index.html` | Official Imperial publication record access |
| `content/pages/resources/index.html` | Group resources and programme entry points |
| `content/research.json` | Research groupings, theme cards and project directory |
| `content/people.json` | People directory and category membership |
| `content/pages/home/research/` | Research themes and project detail pages |
| `content/pages/home/people/` | People listings, alumni and vacancies |
| `content/pages/people/` | Individual profiles |
| `content/pages/home/find-us/index.html` | Find Us page |
| `content/pages.json` | Page paths, titles and legacy URL aliases |
| `templates/header.html` | Shared desktop and mobile navigation |
| `templates/footer.html` | Shared footer |
| `templates/head.html` | Shared metadata and favicon |
| `templates/base.html` | Overall HTML layout |
| `templates/scripts.html` | Shared modern controls |
| `assets/css/modern.css`, `assets/js/modern.js` | Responsive visual system, carousel, menus and filtering |
| `assets/css/academic.css` | Academic layout, circular portraits and deep-blue palette |
| `assets/images/home/` | Added group robot photographs |
| `assets/legacy/` | Preserved original images and vendor resources |
| `assets/fonts/`, `assets/external/` | Locally stored web fonts |
| `site/` | Generated website; edit the sources above, then rebuild |
| `site_content.py` | Expands collection markers into static directory cards |
| `.build/` | Import caches, checks, previous design snapshot and preview logs; ignored by Git |

Use `{{ROOT}}` in source HTML for internal links and assets, for example:

```html
<a href="{{ROOT}}home/research/rf-shadowing/index.html">RF Sensing</a>
<img src="{{ROOT}}assets/legacy/wp-content/uploads/sites/143/2020/08/CogniSense.png" alt="CogniSense">
```

The builder replaces `{{ROOT}}` with the appropriate relative path at every page depth. To add a page, create its content HTML and add an entry to `content/pages.json`; add navigation links in the header or the relevant parent page. Rebuild with `build_site.py`.

Shared base components are in `assets/css/modern.css`; the current academic layout and palette are in `assets/css/academic.css`. Directory cards and homepage research/people sections are generated from the two JSON collections by `site_content.py`. The normal build requires only the Python standard library; one-time migration scripts under `.build/` are not needed. See [docs/DESIGN.md](docs/DESIGN.md) for the content hierarchy and editing guide.

## Included content and known gaps

- **93 content pages**: 81 recovered pages, 7 archive placeholders and 5 new overview pages. The research overview groups 10 themes into 4 areas and includes 20 projects; the people directory includes 41 recovered profiles.
- **7 clearly labelled placeholder pages** for detail URLs that already returned 404 on the original site.
- **11 legacy URL redirects**; navigation links use their working local destinations.
- The new design uses local styles, scripts, photographs and system fonts. External publication/personal/project links remain external; the contact Google Maps embed needs internet access.
- Historical announcements are labelled as archived. The old studentship notice remains in an expandable archive section on the opportunities page.

See `docs/migration.json` for page provenance and the exact missing-page/resource inventory. Original university branding, photographs, content and vendor assets retain their respective ownership and notices.

## GitHub Pages

The repository is `DarkSZChao/AESE-page`. Its Pages workflow publishes the generated `site/` directory. Run `build_site.py` after source edits, then commit both the sources and generated output. The website includes `.nojekyll` and uses relative links for project Pages hosting. The modern redesign is prepared locally; committing and pushing are left to the repository owner.
