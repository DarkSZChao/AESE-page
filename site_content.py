"""Render the shared research and people collections using the standard library."""
from html import escape
import json
from pathlib import Path


def _link(path):
    return "{{ROOT}}" + path + "index.html"


def _image(path, alt, css=""):
    if not path:
        initials = "".join(word[0] for word in alt.split() if word and word not in {"Dr", "Mr", "Ms", "Prof."})[:2]
        return '<div class="no-photo" aria-hidden="true">' + escape(initials) + '</div>'
    return '<img src="{{ROOT}}' + escape(path, quote=True) + '" alt="' + escape(alt, quote=True) + '" loading="lazy" decoding="async"' + (' class="' + css + '"' if css else '') + '>'


def project_card(item, label="", research=False):
    css = "project-card research-card" if research else "project-card"
    return (
        '<article class="' + css + '" data-directory-item data-categories="' + escape(item.get("group", ""), quote=True) + '">'
        '<a class="project-card-image" href="' + _link(item["path"]) + '" tabindex="-1" aria-hidden="true">' + _image(item.get("image", ""), "") + '</a>'
        '<div class="project-card-copy"><span class="label">' + escape(label or item.get("theme", "Research")) + '</span>'
        '<h3><a href="' + _link(item["path"]) + '">' + escape(item["title"]) + '</a></h3>'
        '<p>' + escape(item.get("summary", "")) + '</p>'
        '<a class="text-link" href="' + _link(item["path"]) + '">Explore ' + ('theme' if research else 'project') + '<span aria-hidden="true">↗</span><span class="sr-only">: ' + escape(item["title"]) + '</span></a></div></article>'
    )


def people_card(person):
    return (
        '<article class="person-card" data-directory-item data-categories="' + '|'.join(person["groups"]) + '">'
        '<a class="person-card-image" href="' + _link(person["path"]) + '" tabindex="-1" aria-hidden="true">' + _image(person.get("image", ""), "") + '</a>'
        '<div class="person-card-copy"><h3><a href="' + _link(person["path"]) + '">' + escape(person["name"]) + '</a></h3>'
        '<p>' + escape(" · ".join(person["roles"])) + '</p></div></article>'
    )


def directory(items, filters, kind, initial="all"):
    singular, plural = ("person", "people") if kind == "people" else ("project", "projects")
    tabs = ''.join('<button type="button" data-filter="' + key + '" aria-pressed="' + str(key == initial).lower() + '">' + escape(label) + '</button>' for key, label in filters)
    cards = ''.join(people_card(item) if kind == "people" else project_card(item) for item in items)
    return (
        '<div data-directory data-initial-filter="' + initial + '" data-singular="' + singular + '" data-plural="' + plural + '">'
        '<div class="directory-toolbar"><div class="filter-tabs" role="group" aria-label="Filter ' + plural + '">' + tabs + '</div>'
        '<label class="directory-search"><span class="sr-only">Search ' + plural + '</span><input type="search" data-search placeholder="Search ' + plural + '…"></label></div>'
        '<p class="directory-count" data-result-count role="status" aria-live="polite">' + str(len(items)) + ' ' + plural + '</p>'
        '<div class="' + ('people-grid' if kind == "people" else 'project-grid') + '">' + cards + '</div>'
        '<p class="empty-directory" data-empty hidden>No results match your search. Try another name or keyword.</p></div>'
    )


def render_collections(content: str, input_dir: Path) -> str:
    if "{{HOME_" in content:
        research = json.loads((input_dir / "content/research.json").read_text(encoding="utf-8"))
        people = json.loads((input_dir / "content/people.json").read_text(encoding="utf-8"))["people"]
        rows = []
        for group in research["groups"]:
            themes = [item for item in research["themes"] if item["group"] == group["id"]]
            projects = [item for item in research["projects"] if item["group"] == group["id"]][:3]
            links = ''.join('<li><a href="' + _link(item["path"]) + '">' + escape(item["title"]) + '</a><span>' + escape(item.get("theme", "Research project")) + '</span></li>' for item in projects)
            rows.append('<article class="research-row"><a class="research-row-image" href="' + _link('research/') + '#' + group["id"] + '" aria-label="Explore ' + escape(group["title"], quote=True) + '">' + _image(themes[0]["image"], '') + '</a><div class="research-row-body"><h3><a href="' + _link('research/') + '#' + group["id"] + '">' + escape(group["title"]) + '</a></h3><p>' + escape(group["description"]) + '</p><a class="text-link" href="' + _link('research/') + '#' + group["id"] + '">Research themes &rarr;</a><ul class="research-row-links">' + links + '</ul></div></article>')
        content = content.replace("{{HOME_RESEARCH}}", ''.join(rows))
        students = [person for person in people if 'phd' in person['groups']]
        alumni = [person for person in people if 'alumni' in person['groups']]
        student_cards = ''.join(people_card(person) for person in students)
        alumni_links = ''.join('<li><a href="' + _link(person['path']) + '">' + escape(person['name']) + '</a></li>' for person in alumni)
        content = content.replace("{{HOME_PEOPLE}}", '<h3 class="subsection-title">PhD students</h3><div class="people-grid compact-people">' + student_cards + '</div><details class="alumni-disclosure"><summary>Alumni &amp; former members</summary><ul class="alumni-links">' + alumni_links + '</ul></details>')
    if "{{RESEARCH_" in content or "{{FEATURED_PROJECTS}}" in content:
        research = json.loads((input_dir / "content/research.json").read_text(encoding="utf-8"))
        groups = research["groups"]
        if "{{RESEARCH_SECTIONS}}" in content:
            sections = []
            for number, group in enumerate(groups, 1):
                themes = [item for item in research["themes"] if item["group"] == group["id"]]
                sections.append('<section class="topic-section" id="' + group["id"] + '"><div class="container"><div class="topic-header"><div><p class="eyebrow">Research area ' + str(number).zfill(2) + '</p><h2>' + escape(group["title"]) + '</h2></div><p>' + escape(group["description"]) + '</p></div><div class="project-grid">' + ''.join(project_card(item, "Research theme", True) for item in themes) + '</div></div></section>')
            content = content.replace("{{RESEARCH_SECTIONS}}", '\n'.join(sections))
        if "{{RESEARCH_PROJECTS}}" in content:
            filters = [("all", "All projects")] + [(group["id"], group["short_title"]) for group in groups]
            content = content.replace("{{RESEARCH_PROJECTS}}", directory(research["projects"], filters, "projects"))
        if "{{FEATURED_PROJECTS}}" in content:
            selected = [next(item for item in research["projects"] if item["path"] == path) for path in research["featured"]]
            content = content.replace("{{FEATURED_PROJECTS}}", ''.join(project_card(item) for item in selected))
    if "{{PEOPLE_DIRECTORY" in content:
        people = json.loads((input_dir / "content/people.json").read_text(encoding="utf-8"))
        filters = [("all", "Everyone")] + [(group["id"], group["title"]) for group in people["groups"]]
        content = content.replace("{{PEOPLE_DIRECTORY}}", directory(people["people"], filters, "people"))
        for group in people["groups"]:
            token = "{{PEOPLE_DIRECTORY:" + group["id"] + "}}"
            if token in content:
                subset = [person for person in people["people"] if group["id"] in person["groups"]]
                content = content.replace(token, directory(subset, [], "people"))
    return content
