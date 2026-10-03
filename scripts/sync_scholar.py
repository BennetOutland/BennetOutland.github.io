#!/usr/bin/env python3
"""
Sync new publications from Google Scholar into content/publications/.

Reads the scholar profile URL and author display name from data/authors/me.yaml,
pulls the author's publication list via `scholarly`, and creates a new
content/publications/<slug>/index.md for any publication that isn't already
represented on the site (matched by normalized title). Existing publication
files are never modified or overwritten, so manual edits (forthcoming status,
venue, abstract tweaks, co-author formatting, etc.) always stick.

Entries whose venue looks like a non-paper record (software release, thesis,
dataset) are skipped via SKIP_VENUE_SUBSTRINGS below -- tune that list as
your Scholar profile accumulates other kinds of entries.

Run manually with:
    pip install -r scripts/requirements.txt
    python scripts/sync_scholar.py

Also wired up as a weekly scheduled GitHub Action
(.github/workflows/sync-scholar.yml) that opens a PR with any new entries
for review -- it never pushes straight to main, since Scholar's scraped
metadata (and the journal-vs-conference guess for bare arXiv preprints)
needs a human glance before publishing.
"""
import re
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path

import yaml
from scholarly import scholarly

ROOT = Path(__file__).resolve().parent.parent
AUTHORS_FILE = ROOT / "data" / "authors" / "me.yaml"
PUBLICATIONS_DIR = ROOT / "content" / "publications"

# Venue/citation substrings that mean "not a paper" -- skip these entries.
SKIP_VENUE_SUBSTRINGS = [
    "zenodo",
    "school of mines",  # thesis record
    "dissertation",
]


def normalize_title(title: str) -> str:
    title = unicodedata.normalize("NFKD", title)
    title = re.sub(r"[^a-z0-9 ]", "", title.lower())
    return re.sub(r"\s+", " ", title).strip()


def slugify(title: str) -> str:
    slug = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", slug.lower()).strip("-")
    return slug[:60].rstrip("-")


def existing_titles() -> set[str]:
    titles = set()
    for md in PUBLICATIONS_DIR.glob("*/index.md"):
        text = md.read_text()
        m = re.search(r'^title:\s*"(.+)"\s*$', text, re.MULTILINE)
        if m:
            titles.add(normalize_title(m.group(1)))
    return titles


def existing_slugs() -> set[str]:
    return {p.name for p in PUBLICATIONS_DIR.iterdir() if p.is_dir()}


def format_author(name: str, me_display: str) -> str:
    if name.strip().lower() == me_display.strip().lower():
        return "me"
    parts = name.strip().split()
    if len(parts) >= 2:
        return f"{parts[0][0]}. {' '.join(parts[1:])}"
    return name.strip()


def yaml_str(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def build_markdown(pub: dict, me_display: str) -> str:
    bib = pub["bib"]
    title = bib.get("title", "Untitled")
    authors_raw = bib.get("author", me_display)
    authors = [format_author(a, me_display) for a in authors_raw.split(" and ")]

    year = bib.get("pub_year")
    try:
        year = int(year)
    except (TypeError, ValueError):
        year = date.today().year
    pub_date = date(year, 1, 1)
    if pub_date > date.today():
        pub_date = date.today()
    date_str = pub_date.strftime("%Y-%m-%dT00:00:00Z")

    citation = (bib.get("citation") or "").lower()
    journal = bib.get("journal", "")
    is_arxiv_preprint = "arxiv" in citation or "arxiv" in journal.lower()

    # Scholar can't tell us the eventual target venue for a bare preprint --
    # default to "forthcoming journal article" and leave a TODO so a human
    # confirms (or flips to paper-conference) before this goes live.
    forthcoming_note = ""
    if is_arxiv_preprint:
        publication_types = '["article-journal"]'
        forthcoming = "true"
        publication = yaml_str("Forthcoming")
        forthcoming_note = (
            "\n# TODO: confirm target venue -- set publication_types to "
            '["paper-conference"] here if this is headed to a conference, '
            "and update `publication`/`forthcoming` once accepted."
        )
    else:
        publication_types = '["article-journal"]'
        forthcoming = "false"
        publication = yaml_str(journal or bib.get("citation", ""))

    abstract = bib.get("abstract", "").strip()
    summary = abstract
    if len(summary) > 220:
        cut = summary[:220].rsplit(" ", 1)[0]
        summary = cut + "…"

    lines = [
        "---",
        f"title: {yaml_str(title)}",
        "authors:",
    ]
    lines += [f"  - {a}" for a in authors]
    lines += [
        f'date: "{date_str}"',
        f'publishDate: "{date_str}"',
        f"publication_types: {publication_types}",
    ]
    if forthcoming == "true":
        lines.append("forthcoming: true")
    lines += [
        f"publication: {publication}",
        'publication_short: ""',
        f"abstract: {yaml_str(abstract)}",
        f"summary: {yaml_str(summary)}",
        "tags: []",
        "featured: false",
    ]
    pub_url = pub.get("pub_url")
    if pub_url:
        lines += ["links:", "  - name: arXiv" if "arxiv" in pub_url.lower() else "  - name: Link", f"    url: {yaml_str(pub_url)}"]
    lines.append("---")
    if forthcoming_note:
        lines.append(forthcoming_note.strip())
    lines.append("")
    return "\n".join(lines)


def main():
    if not AUTHORS_FILE.exists():
        print(f"Missing {AUTHORS_FILE}", file=sys.stderr)
        sys.exit(1)

    me = yaml.safe_load(AUTHORS_FILE.read_text())
    scholar_url = me.get("scholar", "")
    me_display = me.get("name", {}).get("display", "")
    m = re.search(r"user=([\w-]+)", scholar_url)
    if not m:
        print(f"Could not parse a Scholar user id out of {scholar_url!r}", file=sys.stderr)
        sys.exit(1)
    scholar_id = m.group(1)

    print(f"Fetching publications for Scholar id {scholar_id} ({me_display}) ...")
    author = scholarly.search_author_id(scholar_id)
    author = scholarly.fill(author, sections=["publications"])

    known_titles = existing_titles()
    known_slugs = existing_slugs()

    created = []
    skipped_existing = []
    skipped_venue = []

    for pub in author["publications"]:
        title = pub["bib"].get("title", "")
        norm = normalize_title(title)
        if norm in known_titles:
            skipped_existing.append(title)
            continue

        citation = pub["bib"].get("citation", "").lower()
        if any(s in citation for s in SKIP_VENUE_SUBSTRINGS):
            skipped_venue.append(title)
            continue

        pub = scholarly.fill(pub)  # fetch authors/abstract/pub_url
        md = build_markdown(pub, me_display)

        slug = slugify(title)
        if not slug:
            slug = f"publication-{len(created) + 1}"
        base_slug = slug
        n = 2
        while slug in known_slugs:
            slug = f"{base_slug}-{n}"
            n += 1
        known_slugs.add(slug)

        out_dir = PUBLICATIONS_DIR / slug
        out_dir.mkdir(parents=True, exist_ok=False)
        (out_dir / "index.md").write_text(md)
        created.append((title, slug))
        known_titles.add(norm)

    print(f"\nCreated {len(created)} new publication page(s):")
    for title, slug in created:
        print(f"  + {slug}/  ({title})")
    print(f"\nSkipped {len(skipped_existing)} already-present publication(s).")
    if skipped_venue:
        print(f"Skipped {len(skipped_venue)} non-paper Scholar entr(ies):")
        for title in skipped_venue:
            print(f"  - {title}")


if __name__ == "__main__":
    main()
