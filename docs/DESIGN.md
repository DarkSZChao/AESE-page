# AESE website structure

The website uses a shared, fully English visual system: warm neutral backgrounds, Imperial-inspired navy, teal links, lime accents, generous spacing and restrained card layouts. All images are existing group resources. The site works as static HTML on GitHub Pages and requires no database or JavaScript framework.

## Navigation and content hierarchy

- **Home**: group introduction, five-photo carousel, four research areas, selected projects, group leadership, highlights and a contact invitation.
- **Research** (`research/`): four areas → ten themes → individual project pages. A searchable project directory brings together twenty recovered projects.
- **People** (`people/`): a searchable directory of forty-one recovered profiles, filterable by leadership, research associates, PhD students, collaborators and alumni. Existing category pages and profile addresses remain available.
- **Publications**: the Imperial profile publication list supplied by the group.
- **News** (`news/`): recognition, the archived DiveIn programme notice, research and opportunity entry points.
- **Contact**: location, group email and Google Maps.
- **Join the group**: general enquiries plus a clearly labelled historical studentship advertisement.

Existing page paths and legacy redirects are preserved. The seven originally unavailable pages remain clearly labelled archive entries. The research areas are editorial groupings of the existing themes; they do not add new research claims. People membership and biographies come from the captured original website and have not been independently refreshed.

## Editing

- Update `content/research.json` for overview theme descriptions, classification, project cards and selected homepage projects.
- Update `content/people.json` for directory names, images and category membership.
- Edit the HTML under `content/pages/` for page text and detail content.
- Shared layout is in `templates/`; styles and controls are in `assets/css/modern.css` and `assets/js/modern.js`.
- Collection markers in page HTML are expanded by `site_content.py` during the normal `build_site.py` run.
- Run `build_site.py` after editing and submit the generated `site/` files together with the source changes.

The carousel supports previous/next controls, individual slide selection, pausing and reduced-motion preferences. Directories filter the already rendered HTML, so the complete content is available without JavaScript. Navigation supports keyboard focus, a mobile menu and a skip-to-content link.

One-time migration scripts and the previous design snapshot are under `.build/` and are not required to build or publish the website.
