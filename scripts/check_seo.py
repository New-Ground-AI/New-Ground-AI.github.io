"""Validate the built site's discovery and indexing settings (standard library only)."""

import argparse
from collections import deque
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urljoin, urlsplit
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET


ORIGIN = "https://new-ground-ai.github.io"
ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = {
    "/projects/project-template/",
    "/projects/ongoing-project-template/",
    "/publication/project-template/",
    "/people/your-slug/site/",
    "/people/member-template/",
}
REDIRECTS = {"/projects/": "/publication/"}
NOINDEX = {"/people/rui-song/site/talk/", "/people/rui-song/site/service/"}
VERIFICATION = "google64a57d41e321cf13.html"


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.canonicals = []
        self.links = []
        self.robots = []
        self.refreshes = []
        self.title = ""
        self.description = ""
        self._in_title = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self._in_title = True
        if tag == "link" and "canonical" in attrs.get("rel", "").lower().split():
            self.canonicals.append(attrs.get("href", ""))
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "meta":
            name = attrs.get("name", "").lower()
            if name in {"robots", "googlebot"}:
                self.robots.append(attrs.get("content", "").lower())
            if name == "description":
                self.description = attrs.get("content", "")
            if attrs.get("http-equiv", "").lower() == "refresh":
                self.refreshes.append(attrs.get("content", ""))

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def public_path(path):
    return path[:-10] if path.endswith("index.html") else path


def internal_path(base, href):
    url = urlsplit(urljoin(ORIGIN + base, href))
    if url.scheme in {"http", "https"} and url.netloc == urlsplit(ORIGIN).netloc:
        return public_path(unquote(url.path))
    return None


def required_urls():
    """Read the content sources so accidental broad excludes cannot pass."""
    urls = {"/", "/people/", "/publication/", "/join/"}
    sources = list((ROOT / "_people").glob("*.md"))
    sources += list((ROOT / "projects").glob("*/index.html"))
    sources += list((ROOT / "people").glob("*/site/**/index.html"))
    sources += list((ROOT / "_projects").glob("*.md"))
    for source in sources:
        if "template" in source.as_posix():
            continue
        text = source.read_text(encoding="utf-8-sig")
        front = text.split("---", 2)[1] if text.startswith("---") else ""
        if re.search(r"^published:\s*false\s*$", front, re.M):
            continue
        match = re.search(r"^permalink:\s*[\"']?(/[^\s\"']*)", front, re.M)
        if match:
            urls.add(match[1])
        elif source.parent.name == "_people":
            urls.add(f"/people/{source.stem}/")
        elif source.parent.name == "_projects":
            urls.add(f"/projects/{source.stem}/")
    return urls


def validate(destination):
    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    pages = {}
    for file in destination.rglob("*.html"):
        relative = file.relative_to(destination).as_posix()
        if relative == VERIFICATION:
            continue
        path = public_path("/" + relative)
        pages[path] = Page(file.read_text(encoding="utf-8-sig"))

    for path in TEMPLATES:
        check(path not in pages, f"Template was published: {path}")
    for path in required_urls():
        check(path in pages, f"Required source page is missing: {path}")

    indexed = set(pages) - set(REDIRECTS) - NOINDEX - {"/404.html"}
    for path, page in pages.items():
        if path == "/404.html":
            continue
        expected = ORIGIN + REDIRECTS.get(path, path)
        check(page.canonicals == [expected], f"{path}: expected exactly one canonical {expected}, got {page.canonicals}")
        is_noindex = any(set(re.split(r"[\s,]+", value)) & {"noindex", "none"} for value in page.robots)
        check(bool(is_noindex) == (path in NOINDEX), f"{path}: unexpected indexing policy (noindex={bool(is_noindex)})")
        check(bool(page.title.strip()), f"{path}: missing title")
        if path in indexed:
            check(bool(page.description.strip()), f"{path}: missing description")
            check(not page.refreshes, f"{path}: unexpected redirect")
        elif path in REDIRECTS:
            targets = [internal_path(path, match.group(1).strip(" \"'"))
                       for value in page.refreshes
                       if (match := re.search(r"url\s*=\s*(.+)$", value, re.I))]
            check(targets == [REDIRECTS[path]], f"{path}: incorrect redirect target {targets}")
        else:
            check(not page.refreshes, f"{path}: unexpected redirect")
        for href in page.links:
            target = internal_path(path, href)
            if target and target.startswith(("/people/", "/projects/")):
                if target.endswith("/") or target.endswith(".html"):
                    check(target in pages, f"{path}: broken content link {href}")

    sitemap = destination / "sitemap.xml"
    locations = []
    if sitemap.exists():
        try:
            document = ET.parse(sitemap)
            locations = [element.text or "" for element in document.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        except ET.ParseError as error:
            errors.append(f"Invalid sitemap XML: {error}")
    else:
        errors.append("Missing sitemap.xml")
    expected_locations = {ORIGIN + path for path in indexed}
    check(set(locations) == expected_locations,
          f"Sitemap mismatch: missing={sorted(expected_locations - set(locations))}, unexpected={sorted(set(locations) - expected_locations)}")
    check(len(locations) == len(set(locations)), "Sitemap contains duplicate URLs")

    robots = destination / "robots.txt"
    if robots.exists():
        text = robots.read_text(encoding="utf-8-sig")
        parser = RobotFileParser()
        parser.parse(text.splitlines())
        check(parser.site_maps() == [ORIGIN + "/sitemap.xml"], "robots.txt must declare the production sitemap")
        for path in indexed:
            check(parser.can_fetch("Googlebot", ORIGIN + path), f"robots.txt blocks {path}")
    else:
        errors.append("Missing robots.txt")

    verification = destination / VERIFICATION
    check(verification.exists() and verification.read_bytes() == (ROOT / VERIFICATION).read_bytes(),
          "Google verification file is missing or changed")

    # Follow ordinary HTML links, just as a crawler can; a sitemap alone must not
    # hide orphaned pages or navigation regressions.
    reached = set()
    queue = deque(["/"])
    while queue:
        path = queue.popleft()
        if path in reached or path not in pages:
            continue
        reached.add(path)
        queue.extend(target for href in pages[path].links
                     if (target := internal_path(path, href)) in pages and target not in reached)
    check(indexed <= reached, f"Pages unreachable through links from home: {sorted(indexed - reached)}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"SEO checks passed: {len(indexed)} indexable pages, sitemap, canonicals, navigation, robots and verification file.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", nargs="?", type=Path, default=ROOT / "_site")
    args = parser.parse_args()
    if not args.destination.is_dir():
        parser.error(f"Build directory does not exist: {args.destination}")
    sys.exit(validate(args.destination))
