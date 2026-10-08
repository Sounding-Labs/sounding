#!/usr/bin/env python3
"""Check local Markdown destinations without fetching any URL."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


def prose(text):
    """Mask code and comments, retaining newlines for useful diagnostics."""
    lines = []
    fence = None
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if marker and fence is None:
            fence = marker.group(1)
            lines.append("\n" if line.endswith("\n") else "")
        elif fence:
            if marker and marker.group(1)[0] == fence[0] and len(marker.group(1)) >= len(fence):
                fence = None
            lines.append("\n" if line.endswith("\n") else "")
        else:
            lines.append(line)
    text = "".join(lines)
    mask = lambda m: "\n" * m.group(0).count("\n")
    text = re.sub(r"<!--.*?-->", mask, text, flags=re.DOTALL)
    return re.sub(r"(`+)(?!`)(.*?)(?<!`)\1(?!`)", mask, text, flags=re.DOTALL)


def destination(text, start):
    """Read an inline/reference target, including escapes and nested parentheses."""
    while start < len(text) and text[start].isspace():
        start += 1
    if start == len(text):
        return ""
    angle = text[start] == "<"
    if angle:
        start += 1
    result = []
    depth = 0
    while start < len(text):
        char = text[start]
        if char == "\\" and start + 1 < len(text):
            result.append(text[start + 1])
            start += 2
            continue
        if angle:
            if char == ">":
                break
        elif char.isspace() or (char == ")" and depth == 0):
            break
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        result.append(char)
        start += 1
    return "".join(result)


class HTMLLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        key = "href" if tag == "a" else "src" if tag == "img" else None
        for name, value in attrs:
            if name == key and value:
                self.links.append((self.getpos()[0], value))


def targets(text):
    text = prose(text)
    for match in re.finditer(r"(?<!\\)\]\(", text):
        yield text.count("\n", 0, match.start()) + 1, destination(text, match.end())
    for match in re.finditer(r"^ {0,3}\[(?!\^)[^\]\n]+\]:[ \t]*", text, re.MULTILINE):
        yield text.count("\n", 0, match.start()) + 1, destination(text, match.end())
    html = HTMLLinks()
    html.feed(text)
    yield from html.links


def check(root):
    root = Path(root).resolve()
    broken = []
    files = sorted(p for p in root.rglob("*.md") if ".git" not in p.relative_to(root).parts)
    checked = 0
    for source in files:
        for line, target in targets(source.read_text(encoding="utf-8")):
            if not target or target.startswith("#"):
                continue
            if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target) or target.startswith("//"):
                continue
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            path = unquote(url.path)
            if not path:
                continue
            checked += 1
            resolved = (root / path.lstrip("/")) if path.startswith("/") else (source.parent / path)
            if not resolved.exists():
                broken.append((source.relative_to(root).as_posix(), line, target))
    return len(files), checked, broken


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    root = parser.parse_args(argv).root
    if not root.is_dir():
        parser.error("root must be an existing directory")
    files, checked, broken = check(root)
    for source, line, target in broken:
        print(f"{source}:{line}: broken relative link: {target}", file=sys.stderr)
    if broken:
        print(f"{len(broken)} broken links in {files} Markdown files", file=sys.stderr)
        return 1
    print(f"Checked {checked} relative links in {files} Markdown files; no broken links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
