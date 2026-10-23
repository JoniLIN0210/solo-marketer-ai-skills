#!/usr/bin/env python3
"""Scan a folder for terms that must not be published.

Keep the terms file OUTSIDE the repository: it usually contains the very
names you are trying to keep out.

Terms file format: one term per line. Lines starting with "#" are comments.
Prefix a term with "soft:" to report it as a warning instead of a failure.

Usage:
  python3 tools/sanitize_check.py --terms ../private/terms.txt [--root .]

Exit code 1 if any hard term is found.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SKIP_DIRS = {".git", "__pycache__", "node_modules"}
TEXT_SUFFIXES = {".md", ".txt", ".csv", ".py", ".json", ".yml", ".yaml", ".toml", ".html", ".js", ""}


def load_terms(path: Path) -> tuple[list[str], list[str]]:
    hard, soft = [], []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.lower().startswith("soft:"):
            soft.append(line[5:].strip())
        else:
            hard.append(line)
    return hard, soft


def scan(root: Path, terms: list[str]) -> list[tuple[str, int, str, str]]:
    hits = []
    for path in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in path.parts) or not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            hits.append((str(path.relative_to(root)), 0, "(binary file - check by hand)", ""))
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for n, line in enumerate(text.splitlines(), 1):
            low = line.lower()
            for term in terms:
                if term.lower() in low:
                    hits.append((str(path.relative_to(root)), n, term, line.strip()[:120]))
    return hits


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--terms", required=True)
    p.add_argument("--root", default=".")
    a = p.parse_args(argv)
    root = Path(a.root).resolve()
    hard, soft = load_terms(Path(a.terms))
    hard_hits, soft_hits = scan(root, hard), scan(root, soft)
    for label, hits in (("FAIL", hard_hits), ("WARN", soft_hits)):
        for f, n, term, line in hits:
            print(f"{label} {f}:{n} [{term}] {line}")
    print(f"\nHard hits: {len(hard_hits)}   Soft hits: {len(soft_hits)}")
    return 1 if hard_hits else 0


if __name__ == "__main__":
    sys.exit(main())
