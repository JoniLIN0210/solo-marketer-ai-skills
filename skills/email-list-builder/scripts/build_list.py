#!/usr/bin/env python3
"""Build a campaign send list from a contact CSV with zero-leak checks.

Input CSV columns (header names, case-insensitive):
  email (required), name, company, segment, status, tags

A contact may appear on several rows. Rows are merged by normalised email,
and exclusions are checked against every row for that address.

Outputs (in --out):
  send_list.csv  contacts to email, ordered by segment priority
  excluded.csv   every excluded address with all reasons
  batches.csv    batch number for each address on the send list
  report.md      counts and the result of every leak check

Exit code 1 if any leak check fails.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import OrderedDict
from pathlib import Path

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")


def normalise(email: str) -> str:
    return (email or "").strip().lower()


def split_list(value: str) -> list[str]:
    return [v.strip().lower() for v in (value or "").replace(";", ",").split(",") if v.strip()]


def read_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return [{(k or "").strip().lower(): (v or "").strip() for k, v in row.items()} for row in reader]


def read_email_set(path: Path | None) -> set[str]:
    if path is None:
        return set()
    return {normalise(r.get("email", "")) for r in read_rows(path) if r.get("email")}


def merge_contacts(rows: list[dict]) -> "OrderedDict[str, dict]":
    merged: "OrderedDict[str, dict]" = OrderedDict()
    for row in rows:
        email = normalise(row.get("email", ""))
        if not email:
            continue
        c = merged.setdefault(email, {"email": email, "name": "", "company": "", "segments": [], "statuses": set(), "tags": set(), "rows": 0})
        c["rows"] += 1
        # Display fields: keep the latest non-empty value.
        for field in ("name", "company"):
            if row.get(field):
                c[field] = row[field]
        seg = row.get("segment", "").lower()
        if seg and seg not in c["segments"]:
            c["segments"].append(seg)
        c["statuses"].update(split_list(row.get("status", "")))
        c["tags"].update(split_list(row.get("tags", "")))
    return merged


def build(args: argparse.Namespace) -> int:
    contacts = merge_contacts(read_rows(Path(args.contacts)))
    blocklist = read_email_set(Path(args.blocklist) if args.blocklist else None)
    received = read_email_set(Path(args.already_received) if args.already_received else None)
    exclude_status = set(split_list(args.exclude_status))
    exclude_tags = set(split_list(args.exclude_tags))
    segments = split_list(args.segments)

    send, excluded = [], []
    for email, c in contacts.items():
        reasons = []
        if not EMAIL_RE.match(email):
            reasons.append("invalid_email")
        if email in blocklist:
            reasons.append("blocklist")
        if email in received:
            reasons.append("already_received")
        reasons += [f"status:{s}" for s in sorted(c["statuses"] & exclude_status)]
        reasons += [f"tag:{t}" for t in sorted(c["tags"] & exclude_tags)]
        if segments and not set(c["segments"]) & set(segments):
            reasons.append("out_of_scope")
        if reasons:
            excluded.append((c, reasons))
        else:
            send.append(c)

    def priority(c: dict) -> int:
        ranks = [segments.index(s) for s in c["segments"] if s in segments]
        return min(ranks) if ranks else len(segments)

    send.sort(key=priority)

    size = args.batch_size if args.batch_size and args.batch_size > 0 else max(len(send), 1)
    batches = [(i // size + 1, c["email"]) for i, c in enumerate(send)]

    # Leak checks: re-test the final list independently of the selection logic.
    final = [c["email"] for c in send]
    checks = OrderedDict()
    checks["block-list addresses on send list"] = sum(e in blocklist for e in final)
    checks["already-received addresses on send list"] = sum(e in received for e in final)
    checks["excluded statuses on send list"] = sum(bool(contacts[e]["statuses"] & exclude_status) for e in final)
    checks["excluded tags on send list"] = sum(bool(contacts[e]["tags"] & exclude_tags) for e in final)
    checks["invalid addresses on send list"] = sum(not EMAIL_RE.match(e) for e in final)
    checks["duplicate addresses on send list"] = len(final) - len(set(final))
    checks["addresses differing between send list and batches"] = len(set(final) ^ {e for _, e in batches})
    checks["batches over the size limit"] = sum(1 for b in {n for n, _ in batches} if sum(n == b for n, _ in batches) > size)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    with (out / "send_list.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["email", "name", "company", "segment"])
        for c in send:
            w.writerow([c["email"], c["name"], c["company"], ";".join(c["segments"])])
    with (out / "excluded.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["email", "company", "reasons"])
        for c, reasons in excluded:
            w.writerow([c["email"], c["company"], ";".join(reasons)])
    with (out / "batches.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["batch", "email"])
        w.writerows(batches)

    reason_counts: dict[str, int] = {}
    for _, reasons in excluded:
        for r in reasons:
            reason_counts[r] = reason_counts.get(r, 0) + 1
    seg_counts: dict[str, int] = {}
    for c in send:
        key = next((s for s in segments if s in c["segments"]), ";".join(c["segments"]) or "(none)")
        seg_counts[key] = seg_counts.get(key, 0) + 1

    passed = all(v == 0 for v in checks.values())
    lines = [
        "# Campaign list report",
        "",
        f"- Rows read: {sum(c['rows'] for c in contacts.values())}",
        f"- Unique addresses: {len(contacts)}",
        f"- Send list: {len(send)}",
        f"- Excluded: {len(excluded)}",
        f"- Batches: {len({n for n, _ in batches})} (size limit {size})",
        "",
        "## Send list by segment",
        "",
        *[f"- {k}: {v}" for k, v in seg_counts.items()],
        "",
        "## Exclusions by reason (a contact can have several)",
        "",
        *[f"- {k}: {v}" for k, v in sorted(reason_counts.items())],
        "",
        "## Leak checks (all must be 0)",
        "",
        *[f"- {'PASS' if v == 0 else 'FAIL'}: {k} = {v}" for k, v in checks.items()],
        "",
        f"**Result: {'ALL CHECKS PASSED' if passed else 'CHECKS FAILED - do not send'}**",
        "",
    ]
    (out / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 0 if passed else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--contacts", required=True, help="Master contact CSV")
    p.add_argument("--blocklist", help="CSV with an email column")
    p.add_argument("--already-received", help="CSV of addresses that already received this content")
    p.add_argument("--exclude-status", default="", help="Comma-separated status values that always exclude")
    p.add_argument("--exclude-tags", default="", help="Comma-separated tags that always exclude")
    p.add_argument("--segments", default="", help="Target segments in priority order; others are out of scope")
    p.add_argument("--batch-size", type=int, default=0, help="Maximum addresses per batch (0 = one batch)")
    p.add_argument("--out", required=True, help="Output folder")
    return build(p.parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
