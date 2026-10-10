#!/usr/bin/env python3
"""Fail when a relative Markdown link points at something that is not there.

Every `*.md` in the repository is walked, each relative link is resolved
against the directory of the file that carries it, and the ones that do not
resolve are printed with the file, the line and the target. Absolute URLs and
in-page anchors are skipped rather than resolved: they need the network or a
heading, neither of which a job that must run offline can be asked to prove.

Nothing here reaches out. The check is a filesystem walk, so it is deterministic
and identical on a pull request, on main and on a developer's machine.
"""

from __future__ import annotations

import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Fenced blocks and inline code are not links, whatever they look like.
FENCE = re.compile(r"^(\s*)(```|~~~)", re.MULTILINE)
INLINE_CODE = re.compile(r"`[^`\n]*`")
# [text](target "title"), [text](<target>), [text](target).
LINK = re.compile(r"\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)")
SKIP_SCHEMES = ("http://", "https://", "mailto:", "ftp://", "//")


def strip_code(text: str) -> str:
    """Blank out code so its contents are never mistaken for a link."""
    lines: list[str] = []
    fence: str | None = None
    for line in text.splitlines(keepends=True):
        m = FENCE.match(line)
        if m:
            marker = m.group(2)
            if fence is None:
                fence = marker
                lines.append(line)
                continue
            if marker == fence:
                fence = None
                lines.append(line)
                continue
        if fence is not None:
            # Keep line numbers stable by replacing the body, not dropping it.
            lines.append(re.sub(r"\S", " ", line))
            continue
        lines.append(INLINE_CODE.sub(lambda m: " " * len(m.group(0)), line))
    return "".join(lines)


def is_skippable(target: str) -> bool:
    if not target or target.startswith("#"):
        return True
    return target.lower().startswith(SKIP_SCHEMES)


def main() -> int:
    broken: list[str] = []
    checked = 0

    for path in sorted(ROOT.rglob("*.md")):
        rel = path.relative_to(ROOT)
        if any(part in {".git", "node_modules", "vendor"} for part in rel.parts):
            continue
        text = strip_code(path.read_text(encoding="utf-8", errors="replace"))

        for lineno, line in enumerate(text.splitlines(), start=1):
            for match in LINK.finditer(line):
                raw = urllib.parse.unquote(match.group(1))
                if is_skippable(raw):
                    continue
                # A fragment carries no path; a query carries no path either.
                target = raw.split("#", 1)[0].split("?", 1)[0]
                if not target:
                    continue
                checked += 1
                resolved = (path.parent / target).resolve()
                try:
                    resolved.relative_to(ROOT)
                except ValueError:
                    broken.append(f"{rel}:{lineno}: {raw} -> escapes the repository")
                    continue
                if not resolved.exists():
                    broken.append(
                        f"{rel}:{lineno}: {raw} -> {resolved.relative_to(ROOT)} does not exist"
                    )

    if broken:
        print("Broken relative links:")
        for entry in broken:
            print(f"  {entry}")
        print(f"\n{len(broken)} broken, {checked} relative links checked.")
        return 1

    print(f"All relative links resolve ({checked} checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
