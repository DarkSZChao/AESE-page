"""Build the static website. Run this file directly in PyCharm."""

from __future__ import annotations

import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil

from site_content import render_collections


def _inside(directory: Path, relative_path: str) -> Path:
    if not isinstance(relative_path, str) or "\\" in relative_path:
        raise ValueError(f"Invalid relative path: {relative_path!r}")
    if relative_path.startswith("/") or any(
        part in {".", ".."} or ":" in part
        for part in relative_path.split("/")
    ):
        raise ValueError(f"Unsafe relative path: {relative_path!r}")
    destination = (directory / relative_path).resolve()
    if not destination.is_relative_to(directory.resolve()):
        raise ValueError(f"Path leaves its directory: {relative_path!r}")
    return destination


def _page_path(value: str) -> str:
    if not isinstance(value, str) or any(character in value for character in "\\:?#"):
        raise ValueError(f"Invalid page path: {value!r}")
    if value.startswith("/") or "//" in value:
        raise ValueError(f"Invalid page path: {value!r}")
    parts = value.rstrip("/").split("/") if value else []
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError(f"Invalid page path: {value!r}")
    if parts and parts[0] == "assets":
        raise ValueError("Page paths cannot use the reserved assets directory.")
    return "/".join(parts) + ("/" if parts else "")


def _root_prefix(page_path: str) -> str:
    return "../" * page_path.count("/") if page_path else "./"


class _NavigationParser(HTMLParser):
    """Locate menu list items without reformatting the original HTML."""

    def __init__(self, source: str, current_path: str):
        super().__init__(convert_charrefs=True)
        source = re.sub(r"\s+aria-current\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s>]+)", "", source, flags=re.I)
        self.source = source
        self.current_path = current_path
        self.section = (
            "research" if current_path.startswith(("home/research/", "research/"))
            else "people" if current_path.startswith(("people/", "home/people/"))
            else ""
        )
        self.offsets = [0]
        for match in re.finditer("\n", source):
            self.offsets.append(match.end())
        self.items: list[dict] = []
        self.stack: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        if tag == "li":
            line, column = self.getpos()
            classes = dict(attrs).get("class") or ""
            item = {
                "start": self.offsets[line - 1] + column,
                "tag": self.get_starttag_text(),
                "classes": [
                    name for name in classes.split()
                    if name != "active" and not name.startswith(("current-menu-", "current_page_"))
                ],
            }
            self.items.append(item)
            self.stack.append(item)
        elif tag == "a" and self.stack:
            href = dict(attrs).get("href") or ""
            if not href.startswith("{{ROOT}}"):
                return
            target = href[len("{{ROOT}}") :].split("#", 1)[0].split("?", 1)[0]
            if target.endswith("index.html"):
                target = target[:-len("index.html")]
            section = (
                "research" if target.startswith(("home/research/", "research/"))
                else "people" if target.startswith(("people/", "home/people/"))
                else ""
            )
            if len(self.stack) > 1 and section and section == self.section:
                self.stack[0]["classes"].extend(["active", "current-menu-ancestor", "current_page_ancestor"])
            exact_match = target.rstrip("/") == self.current_path.rstrip("/")
            ancestor_match = bool(target) and self.current_path.startswith(target.rstrip("/") + "/")
            if target in {"research/", "people/"} and section == self.section:
                ancestor_match = not exact_match
            if target == "news/" and self.current_path.startswith(("events/", "introducing-the-cdt-phd-programme/")):
                ancestor_match = True
            if not exact_match and not ancestor_match:
                return
            self.stack[-1]["classes"].extend(
                ["active", "current-menu-item", "current_page_item"] if exact_match
                else ["active", "current-menu-ancestor", "current_page_ancestor"]
            )
            for ancestor in self.stack[:-1]:
                ancestor["classes"].extend(["active", "current-menu-ancestor", "current_page_ancestor"])
            if len(self.stack) > 1:
                self.stack[-2]["classes"].extend(["current-menu-parent", "current_page_parent"])

    def handle_endtag(self, tag: str):
        if tag == "li" and self.stack:
            self.stack.pop()

    def render(self) -> str:
        self.feed(self.source)
        result = self.source
        class_pattern = re.compile(r"\bclass\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s>]+)", re.I)
        for item in reversed(self.items):
            classes = " ".join(dict.fromkeys(item["classes"]))
            attribute = f'class="{html.escape(classes, quote=True)}"'
            original = item["tag"]
            if class_pattern.search(original):
                replacement = class_pattern.sub(lambda _: attribute, original, count=1)
            elif classes:
                replacement = original[:-1] + " " + attribute + ">"
            else:
                continue
            start = item["start"]
            result = result[:start] + replacement + result[start + len(original):]
        return result


def _write_text(output_path: Path, text: str):
    if output_path.is_file() and output_path.read_text(encoding="utf-8") == text:
        return
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8", newline="\n")


def build_site(input_dir: Path, output_dir: Path) -> dict[str, int]:
    input_dir = Path(input_dir).resolve()
    output_dir = Path(output_dir).resolve()
    if input_dir == output_dir or input_dir.is_relative_to(output_dir):
        raise ValueError("The output directory must not contain the source directory.")
    manifest = json.loads(_inside(input_dir, "content/pages.json").read_text(encoding="utf-8"))
    pages = manifest["pages"]
    aliases = manifest.get("aliases", {})
    if not isinstance(pages, list) or not isinstance(aliases, dict):
        raise ValueError("The manifest must contain a pages list and an aliases object.")

    templates = {
        name: _inside(input_dir, f"templates/{name}.html").read_text(encoding="utf-8")
        for name in ("base", "head", "header", "footer", "scripts")
    }
    prepared_pages = []
    page_paths = set()
    for page in pages:
        page_path = _page_path(page["path"])
        if page_path in page_paths:
            raise ValueError(f"Duplicate page path: {page_path!r}")
        page_paths.add(page_path)
        content_path = _inside(input_dir, page["content"])
        if not content_path.is_relative_to(_inside(input_dir, "content")):
            raise ValueError("Page content must be inside the content directory.")
        prepared_pages.append((page_path, page, content_path.read_text(encoding="utf-8")))

    prepared_aliases = {}
    for source, target in aliases.items():
        source, target = _page_path(source), _page_path(target)
        if source in page_paths or source in prepared_aliases:
            raise ValueError(f"Alias conflicts with an existing page: {source!r}")
        if target not in page_paths:
            raise ValueError(f"Alias target does not exist: {target!r}")
        prepared_aliases[source] = target

    output_dir.mkdir(parents=True, exist_ok=True)
    for page_path, page, content in prepared_pages:
        rendered = templates["base"]
        replacements = {
            "HEAD": templates["head"],
            "HEADER": _NavigationParser(templates["header"], page_path).render(),
            "CONTENT": render_collections(content, input_dir),
            "FOOTER": templates["footer"],
            "SCRIPTS": templates["scripts"],
        }
        for token, value in replacements.items():
            rendered = rendered.replace("{{" + token + "}}", value)
        rendered = rendered.replace("{{TITLE}}", html.escape(page["title"]))
        rendered = rendered.replace("{{BODY_CLASS}}", html.escape(page.get("body_class", ""), quote=True))
        rendered = rendered.replace("{{ROOT}}", _root_prefix(page_path))
        _write_text(_inside(output_dir, page_path + "index.html"), rendered)

    for source, target in prepared_aliases.items():
        href = html.escape(_root_prefix(source) + target + "index.html", quote=True)
        redirect = (
            '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            f'<meta http-equiv="refresh" content="0; url={href}">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Page moved</title></head><body>'
            f'<p>This page has moved. <a href="{href}">Continue to the page</a>.</p>'
            '</body></html>\n'
        )
        _write_text(_inside(output_dir, source + "index.html"), redirect)

    asset_count = copied_count = 0
    input_assets = _inside(input_dir, "assets")
    if input_assets.is_dir():
        for source in sorted(input_assets.rglob("*")):
            if not source.is_file():
                continue
            if not source.resolve().is_relative_to(input_assets):
                raise ValueError(f"Asset leaves the assets directory: {source}")
            relative_path = source.relative_to(input_assets).as_posix()
            destination = _inside(output_dir, "assets/" + relative_path)
            asset_count += 1
            source_stat = source.stat()
            if destination.is_file():
                destination_stat = destination.stat()
                if (source_stat.st_size, source_stat.st_mtime_ns) == (
                    destination_stat.st_size, destination_stat.st_mtime_ns
                ):
                    continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            copied_count += 1

    _write_text(_inside(output_dir, ".nojekyll"), "")
    _write_text(
        _inside(output_dir, "404.html"),
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>Page not found</title></head><body>'
        '<h1>Page not found</h1><p>The requested page could not be found.</p>'
        '<p><a href="./index.html">Return to the home page</a></p></body></html>\n',
    )
    result = {"pages": len(prepared_pages), "aliases": len(prepared_aliases), "assets": asset_count, "copied_assets": copied_count}
    print(
        f"Built {result['pages']} pages, {result['aliases']} redirects and "
        f"{asset_count} assets ({copied_count} copied): {output_dir}"
    )
    return result


if __name__ == "__main__":
    input_dir = Path(__file__).resolve().parent
    output_dir = input_dir / "site"

    build_site(input_dir, output_dir)
