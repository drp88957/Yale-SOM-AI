"""Build wiki-data.js from the Markdown pages so index.html can be opened directly.

Run after adding or editing pages:  python build.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
PAGE_FOLDERS = ["stories", "concepts", "books", "situations", "debates", "entities"]


def parse_frontmatter(text):
    """Split '---' frontmatter (simple key: value / [a, b] lists) from the body."""
    meta = {}
    if not text.startswith("---"):
        return meta, text
    _, header, body = text.split("---", 2)
    for line in header.strip().splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            value = [v.strip() for v in value[1:-1].split(",") if v.strip()]
        elif value.lower() in ("true", "false"):
            value = value.lower() == "true"
        meta[key.strip()] = value
    return meta, body.strip()


def load_pages():
    pages = []
    for folder in PAGE_FOLDERS:
        for path in sorted((ROOT / folder).glob("*.md")):
            meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
            title_match = re.search(r"^# (.+)$", body, re.MULTILINE)
            hook_match = re.search(r"\*\*One-line hook:\*\*\s*(.+)", body)
            source = meta.get("source", "")
            pages.append({
                "slug": path.stem,
                "folder": folder,
                "type": meta.get("type", folder.rstrip("s")),
                "title": title_match.group(1).strip() if title_match else path.stem,
                "hook": hook_match.group(1).strip() if hook_match else "",
                "source": source,
                "book": source.split("—")[0].strip() if source else "",
                "concepts": meta.get("concepts", []),
                "situations": meta.get("situations", []),
                "verified": meta.get("verified_by_deep", False),
                "body": body,
            })
    return pages


def load_library():
    """Read the category headings and book tables from books.md."""
    library, category = [], None
    for line in (ROOT / "books.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            category = line[3:].strip()
        row = re.match(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|$", line)
        if row and category:
            library.append({
                "num": int(row.group(1)),
                "title": row.group(2),
                "author": row.group(3),
                "category": category,
            })
    return library


def load_taxonomy():
    """Read allowed situations (grouped by ### theme) and concepts from taxonomy.md."""
    taxonomy = {"situationGroups": [], "concepts": []}
    section = None
    for line in (ROOT / "taxonomy.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = line[3:].strip().lower()
        elif line.startswith("### ") and section == "situations":
            taxonomy["situationGroups"].append({"name": line[4:].strip(), "items": []})
        item = re.match(r"^- (\S+) — (.+)$", line)
        if not item:
            continue
        entry = {"slug": item.group(1), "label": item.group(2).strip()}
        if section == "situations" and taxonomy["situationGroups"]:
            taxonomy["situationGroups"][-1]["items"].append(entry)
        elif section == "concepts":
            taxonomy["concepts"].append(entry)
    return taxonomy


def norm(title):
    """Match book names loosely, the same way index.html does."""
    return re.sub(r"[^a-z0-9]", "", re.sub(r"^the\s+", "", title.lower()))


def check_tags(pages, taxonomy, library):
    situations = {i["slug"] for g in taxonomy["situationGroups"] for i in g["items"]}
    concepts = {c["slug"] for c in taxonomy["concepts"]}
    titles = {norm(b["title"]) for b in library}
    for p in pages:
        for s in p["situations"]:
            if s not in situations:
                print(f"  WARNING {p['slug']}: situation '{s}' is not in taxonomy.md")
        for c in p["concepts"]:
            if c not in concepts:
                print(f"  WARNING {p['slug']}: concept '{c}' is not in taxonomy.md")
        book = norm(p["book"])
        if book and not any(t == book or t.startswith(book) or book.startswith(t) for t in titles):
            print(f"  WARNING {p['slug']}: book '{p['book']}' is not in books.md")


if __name__ == "__main__":
    data = {"pages": load_pages(), "library": load_library(), "taxonomy": load_taxonomy()}
    check_tags(data["pages"], data["taxonomy"], data["library"])
    out = ROOT / "wiki-data.js"
    out.write_text("window.WIKI = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n",
                   encoding="utf-8")
    print(f"Built {out.name}: {len(data['pages'])} pages, {len(data['library'])} books")
