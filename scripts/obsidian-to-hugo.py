#!/usr/bin/env python3
"""Copy Obsidian notes tagged for Hugo publication with archetype frontmatter."""

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

VAULT_DIR = Path.home() / "src/github.com/mccurdyc/obsidian.md"
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
ARCHETYPES_DIR = REPO_ROOT / "archetypes"

KINDS = {
    "posts": {
        "tag": "public",
        "content_dir": "content/posts",
        "archetype": "posts.md",
        "trigger_tag": "public",
    },
    "books": {
        "tag": "book",
        "content_dir": "content/books",
        "archetype": "books.md",
        "trigger_tag": "book",
    },
}


def slugify(text: str) -> str:
    """Convert a string to a lowercase, hyphen-separated slug."""
    lowered = text.lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", lowered)
    collapsed = re.sub(r"-+", "-", normalized)
    return collapsed.strip("-")


def title_case(text: str) -> str:
    """Return a title-cased version of the string."""
    return " ".join(word.capitalize() for word in text.split())


def parse_obsidian_date(value: str) -> str:
    """Parse an Obsidian 'date created' string to RFC 3339 local time."""
    # e.g., "Saturday, September 26th 2026, 10:45:49 pm"
    cleaned = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", value)
    dt = datetime.strptime(cleaned, "%A, %B %d %Y, %I:%M:%S %p")
    ts = dt.timestamp()
    t = time.localtime(ts)
    offset_seconds = t.tm_gmtoff
    offset_hours, rem = divmod(offset_seconds, 3600)
    offset_minutes = abs(rem) // 60
    sign = "+" if offset_hours >= 0 else "-"
    offset_str = f"{sign}{abs(offset_hours):02d}:{offset_minutes:02d}"
    local_dt = datetime.fromtimestamp(ts)
    return local_dt.strftime("%Y-%m-%dT%H:%M:%S") + offset_str


def parse_utc_timestamp(value: str) -> str:
    """Format an ISO 8601 UTC timestamp as local RFC 3339."""
    # Truncate sub-second precision if present.
    cleaned = re.sub(r"\.\d+", "", value)
    dt = datetime.strptime(cleaned, "%Y-%m-%dT%H:%M:%S")
    ts = dt.replace(tzinfo=datetime.now().astimezone().tzinfo).timestamp()
    t = time.localtime(ts)
    offset_seconds = t.tm_gmtoff
    offset_hours, rem = divmod(offset_seconds, 3600)
    offset_minutes = abs(rem) // 60
    sign = "+" if offset_hours >= 0 else "-"
    offset_str = f"{sign}{abs(offset_hours):02d}:{offset_minutes:02d}"
    local_dt = datetime.fromtimestamp(ts)
    return local_dt.strftime("%Y-%m-%dT%H:%M:%S") + offset_str


def parse_yaml_scalar(text: str):
    """Parse a single YAML scalar value."""
    text = text.strip()
    if text == "true":
        return True
    if text == "false":
        return False
    if text in ("null", "~"):
        return None
    if (text.startswith('"') and text.endswith('"')) or (
        text.startswith("'") and text.endswith("'")
    ):
        return text[1:-1]
    try:
        if "." in text:
            return float(text)
        return int(text)
    except ValueError:
        return text


def parse_yaml_flow_list(text: str) -> list:
    """Parse a YAML flow-style list."""
    inner = text[1:-1].strip()
    if not inner:
        return []
    items = []
    current = ""
    in_string = False
    string_char = None
    for ch in inner:
        if ch in ('"', "'") and (not in_string or string_char == ch):
            in_string = not in_string
            if in_string:
                string_char = ch
            else:
                string_char = None
        if ch == "," and not in_string:
            items.append(current.strip())
            current = ""
        else:
            current += ch
    if current.strip():
        items.append(current.strip())
    return [parse_yaml_scalar(item) for item in items if item.strip()]


def parse_simple_yaml(text: str) -> dict:
    """Parse a small subset of YAML used by the archetype frontmatter."""
    lines = text.splitlines()
    result = {}
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        if ":" not in stripped:
            i += 1
            continue
        key, rest = stripped.split(":", 1)
        key = key.strip()
        rest = rest.strip()
        if not rest:
            i += 1
            children = []
            while i < n:
                child = lines[i]
                if not child.strip():
                    i += 1
                    continue
                if child.lstrip() == child:
                    break
                children.append(child.lstrip())
                i += 1
            if children and all(c.startswith("- ") for c in children):
                result[key] = [
                    parse_yaml_scalar(c[2:].strip()) for c in children
                ]
            elif children:
                result[key] = parse_simple_yaml("\n".join(children))
            else:
                result[key] = {}
        elif rest.startswith("[") and rest.endswith("]"):
            result[key] = parse_yaml_flow_list(rest)
            i += 1
        else:
            result[key] = parse_yaml_scalar(rest)
            i += 1
    return result


def dump_yaml_value(value) -> str:
    """Serialize a simple YAML value."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value)
    if isinstance(value, list):
        if not value:
            return "[]"
        return "[" + ", ".join(dump_yaml_value(item) for item in value) + "]"
    raise ValueError(f"unsupported YAML value type: {type(value)}")


def dump_simple_yaml(data: dict) -> str:
    """Serialize a simple YAML mapping."""
    lines = []
    for key, value in data.items():
        lines.append(f"{key}: {dump_yaml_value(value)}")
    return "\n".join(lines)


def extract_frontmatter(text: str) -> str:
    """Return the YAML frontmatter from a markdown file."""
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    if end == -1:
        return ""
    return text[3:end].strip()


def render_archetype(archetype_path: Path, name: str, date_str: str) -> dict:
    """Render an archetype template and parse its frontmatter."""
    text = archetype_path.read_text()
    frontmatter = extract_frontmatter(text)
    title = title_case(name.replace("-", " "))
    rendered = (
        frontmatter
        .replace("{{ .Name }}", name)
        .replace('"{{ replace .Name "-" " " | title }}"', json.dumps(title))
        .replace("{{ replace .Name \"-\" \" \" | title }}", title)
        .replace("{{ .Date }}", date_str)
    )
    return parse_simple_yaml(rendered)


def list_notes(tag: str) -> list[dict]:
    """List Obsidian notes tagged with the given tag."""
    result = subprocess.run(
        ["zk", "list", "--tag", tag, "--format", "json", "-q"],
        cwd=VAULT_DIR,
        capture_output=True,
        text=True,
        check=True,
    )
    if not result.stdout.strip():
        return []
    return json.loads(result.stdout)


def build_frontmatter(
    kind: str,
    archetype_path: Path,
    note: dict,
    slug: str,
) -> dict:
    """Merge note metadata into the rendered archetype frontmatter."""
    config = KINDS[kind]
    trigger = config["trigger_tag"]
    metadata = note.get("metadata", {})

    date_value = metadata.get("date created", "")
    if date_value:
        date_str = parse_obsidian_date(date_value)
    else:
        date_str = parse_utc_timestamp(note.get("created", ""))

    archetype_fm = render_archetype(archetype_path, slug, date_str)

    # Start from archetype defaults and overlay note values.
    frontmatter = dict(archetype_fm)
    frontmatter["title"] = note.get("title", title_case(slug.replace("-", " ")))
    frontmatter["date"] = date_str

    note_tags = [t for t in note.get("tags", []) if t != trigger]

    if kind == "posts":
        frontmatter["tags"] = note_tags
    elif kind == "books":
        frontmatter["book-tags"] = ["book"] + note_tags
        frontmatter["books"] = [frontmatter["title"]]
        frontmatter["image"] = f"/images/book-covers/{slug}/cover.jpg"

    # Drop Obsidian-specific keys if the archetype somehow included them.
    for key in ("date created", "date modified"):
        frontmatter.pop(key, None)

    return frontmatter


def process_kind(kind: str, dry_run: bool = False) -> int:
    """Process all Obsidian notes tagged for the given kind."""
    config = KINDS[kind]
    tag = config["tag"]
    content_dir = REPO_ROOT / config["content_dir"]
    archetype_path = ARCHETYPES_DIR / config["archetype"]

    if not archetype_path.exists():
        print(f"error: missing archetype {archetype_path}", file=sys.stderr)
        return 1

    notes = list_notes(tag)
    if not notes:
        print(f"No notes tagged #{tag} found.")
        return 0

    if not dry_run:
        content_dir.mkdir(parents=True, exist_ok=True)

    copied = 0
    for note in notes:
        rel_path = note["path"]
        title = note.get("title", "")

        if kind == "posts":
            slug = slugify(rel_path.removesuffix(".md"))
        else:
            slug = slugify(title)

        if not slug:
            print(f"Warning: empty slug for {rel_path}", file=sys.stderr)
            continue

        dest_file = content_dir / f"{slug}.md"
        frontmatter = build_frontmatter(kind, archetype_path, note, slug)
        body = note.get("body", "").rstrip()
        output = f"---\n{dump_simple_yaml(frontmatter)}\n---\n\n{body}\n"

        if dry_run:
            print(f"[dry-run] {rel_path} -> {dest_file}")
        else:
            dest_file.write_text(output)
            print(f"{rel_path} -> {dest_file}")
        copied += 1

    print(f"{'Would copy' if dry_run else 'Copied'} {copied} note(s) to {content_dir}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Copy Obsidian notes into Hugo content with archetype frontmatter.",
    )
    parser.add_argument(
        "kind",
        choices=list(KINDS.keys()),
        help="Content kind to generate.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be copied without writing files.",
    )
    args = parser.parse_args()

    return process_kind(args.kind, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
