# AESE website — local static edition

A static reproduction of the [AESE group website](https://wp.doc.ic.ac.uk/aese/), captured on 6 October 2026. It keeps the existing Academix design, navigation, photographs and historical content. Information has **not** been updated.

## Preview locally

Open this folder in PyCharm and **right-click `preview.py` → Run**. The script builds the website and opens **http://127.0.0.1:8000/**. Stop the run to stop the server. Python 3.10+ is sufficient; no additional packages, Node.js, WordPress or database are needed.

Preview settings are at the bottom of `preview.py`. Change `port` if 8000 is already in use. After editing source files, run `build_site.py` again and refresh the browser. You can also open `site/index.html` directly after building; internal links include `index.html` so they work without a server.

## Edit the website

| Location | Purpose |
| --- | --- |
| `content/pages/index.html` | Homepage content, slider and research cards |
| `content/pages/home/research/` | Research themes and project detail pages |
| `content/pages/home/people/` | People listings, alumni and vacancies |
| `content/pages/people/` | Individual profiles |
| `content/pages/home/find-us/index.html` | Find Us page |
| `content/pages.json` | Page paths, titles and legacy URL aliases |
| `templates/header.html` | Shared desktop and mobile navigation |
| `templates/footer.html` | Shared footer |
| `templates/head.html` | Shared theme styles and fonts |
| `templates/base.html` | Overall HTML layout |
| `templates/scripts.html` | Original theme scripts |
| `assets/css/static.css`, `assets/js/static.js` | Small static-site adaptations |
| `assets/legacy/` | Original theme files, images and icon fonts |
| `assets/fonts/`, `assets/external/` | Locally stored web fonts |
| `site/` | Generated website; edit the sources above, then rebuild |
| `.build/` | Disposable import caches, checks and preview logs; ignored by Git |

Use `{{ROOT}}` in source HTML for internal links and assets, for example:

```html
<a href="{{ROOT}}home/research/rf-shadowing/index.html">RF Sensing</a>
<img src="{{ROOT}}assets/legacy/wp-content/uploads/sites/143/2020/08/CogniSense.png" alt="CogniSense">
```

The builder replaces `{{ROOT}}` with the appropriate relative path at every page depth. To add a page, create its content HTML and add an entry to `content/pages.json`; add navigation links in the header or the relevant parent page. Rebuild with `build_site.py`.

The retained `kc-css-*` classes and inline styles control the original page layouts. Start by changing text, links or images within those containers. Shared layout changes belong in `assets/css/static.css`.

## Included content and known gaps

- **81 recovered pages**: homepage, 10 research themes, 20 projects, 41 profiles, 6 people/category pages, Find Us, DiveIn and news.
- **7 clearly labelled placeholder pages** for detail URLs that already returned 404 on the original site.
- **11 legacy URL redirects**; navigation links use their working local destinations.
- Theme scripts, images and fonts are served locally. External publication/personal/project links remain external; the Find Us Google Maps embed needs internet access.
- The homepage's appended WordPress error document was removed. A few unavailable, unused theme background images were disabled. Other historical content and layout quirks are retained.

See `docs/migration.json` for page provenance and the exact missing-page/resource inventory. Original university branding, photographs, content and vendor assets retain their respective ownership and notices.

## GitHub Pages later

The planned destination is `DarkSZChao/aese-page`. **No repository has been created, pushed or deployed.** The generated `site/` directory is ready for a future GitHub Pages deployment. It includes `.nojekyll` and uses relative links, including when served below `/aese-page/`. A deployment workflow can be added when publishing is requested.
