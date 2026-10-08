# AESE website structure

The website uses a fully English academic layout inspired by [ARPG at CU Boulder](https://arpg.colorado.edu/): a compact navigation bar, centred introduction, horizontal research features, project cards, circular researcher photographs and a simple publication section. Its own palette uses deep navy (`#071d41`), blue (`#234d8a`), white and pale blue backgrounds. No ARPG text, photographs or research claims are reused. All photographs are existing AESE resources. The static site runs on GitHub Pages without a database or JavaScript framework.

## Navigation and content hierarchy

- **Home**: centred group introduction over a five-photo background carousel, four research feature rows, selected project archive, resource cards, group leadership, PhD student portraits, expandable alumni, publication access and contact details. A deep-blue overlay keeps the white introduction readable over each photograph.
- **Research** (`research/`): four areas → ten themes → individual project pages. A searchable project directory brings together twenty recovered projects.
- **People** (`people/`): a searchable directory of forty-one recovered profiles, filterable by leadership, research associates, PhD students, collaborators and alumni. Existing category pages and profile addresses remain available.
- **Publications** (`publications/`): access to the official Imperial profile publication record supplied by the group. Bibliographic records are not invented or copied from the reference site.
- **Resources** (`resources/`): project catalogue, publication record, archived doctoral training information, opportunities, news and community roles. The existing material does not establish an AESE dataset catalogue, so this section uses available group resources.
- **News** (`news/`, linked from Resources and the footer): recognition, the archived DiveIn programme notice, research and opportunity entry points.
- **Contact**: location, group email and Google Maps.
- **Join the group**: general enquiries plus a clearly labelled historical studentship advertisement.

Existing page paths and legacy redirects are preserved. The seven originally unavailable pages remain clearly labelled archive entries. The research areas are editorial groupings of the existing themes; they do not add new research claims. People membership and biographies come from the captured original website and have not been independently refreshed.

## Editing

- Update `content/research.json` for overview theme descriptions, classification, project cards and selected homepage projects.
- Update `content/people.json` for directory names, images and category membership.
- Edit the HTML under `content/pages/` for page text and detail content.
- Shared layout is in `templates/`; `assets/css/modern.css` supplies base component styles and `assets/css/academic.css` supplies the academic layout and deep-blue palette. Controls are in `assets/js/modern.js`.
- Homepage collection markers `HOME_RESEARCH` and `HOME_PEOPLE` use the same research and people JSON records as the overview pages.
- Collection markers in page HTML are expanded by `site_content.py` during the normal `build_site.py` run.
- Run `build_site.py` after editing and submit the generated `site/` files together with the source changes.

The carousel supports previous/next controls, individual slide selection, pausing and reduced-motion preferences. Directories filter the already rendered HTML, so the complete content is available without JavaScript. Navigation supports keyboard focus, a mobile menu and a skip-to-content link.

One-time migration scripts and the previous design snapshot are under `.build/` and are not required to build or publish the website.
