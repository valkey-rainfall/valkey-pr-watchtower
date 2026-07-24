#!/usr/bin/env python3
"""
dump_enriched.py — fetch open PRs and dump the Stage-1 enrichment as JSON.

Usage:
    python scripts/dump_enriched.py [--limit N] [--out data/enriched.json]

Uses GITHUB_TOKEN if present (5000 req/hr); otherwise falls back to
unauthenticated public reads (60 req/hr) — fine for small --limit spot-checks.
"""
import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.parse
import urllib.error

from enrich import enrich_all

REPO = "valkey-io/valkey"
BASE = "https://api.github.com"


def gh_get(path, params=None):
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "valkey-pr-watchtower/enrich")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code in (403, 429) and attempt < 2:
                wait = int(e.headers.get("Retry-After", 15))
                print(f"  rate limited ({e.code}), sleeping {wait}s", file=sys.stderr)
                time.sleep(wait)
            else:
                raise


def gh_paginate(path, params=None):
    params = dict(params or {})
    params.setdefault("per_page", 100)
    results, page = [], 1
    while True:
        params["page"] = page
        data = gh_get(path, params)
        if not data:
            break
        results.extend(data)
        if len(data) < params["per_page"]:
            break
        page += 1
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=5, help="max PRs to enrich")
    ap.add_argument("--out", default=None, help="write enriched JSON here")
    ap.add_argument("--page-only", action="store_true",
                    help="fetch only the first page of open PRs (spot-check)")
    args = ap.parse_args()

    print("Fetching open PRs...", file=sys.stderr)
    if args.page_only:
        prs = gh_get(f"/repos/{REPO}/pulls", {"state": "open", "per_page": 100}) or []
    else:
        prs = gh_paginate(f"/repos/{REPO}/pulls", {"state": "open"})
    print(f"  {len(prs)} open PRs.", file=sys.stderr)

    # Sample across the age range: oldest + newest non-draft, non-bot PRs.
    candidates = [p for p in prs
                  if not p.get("draft")
                  and not (p.get("user") or {}).get("login", "").endswith("[bot]")]
    candidates.sort(key=lambda p: p["created_at"])
    if args.limit and len(candidates) > args.limit:
        half = args.limit // 2
        sample = candidates[:args.limit - half] + candidates[-half:] if half else candidates[:args.limit]
    else:
        sample = candidates

    def progress(num, count):
        print(f"  enriched #{num} ({count}/{len(sample)})", file=sys.stderr)

    enriched = enrich_all(sample, gh_get, gh_paginate, repo=REPO, progress=progress)

    if args.out:
        with open(args.out, "w") as f:
            json.dump(enriched, f, indent=2)
        print(f"Wrote {args.out}", file=sys.stderr)

    # Spot-check table
    print(f"\n{'PR':>6} {'author':<16} {'review':<18} {'CI':<14} "
          f"{'merge':<9} {'last_author':<20} {'last_reviewer':<20}")
    for num, e in enriched.items():
        ch = e["checks"]
        ci = f"{ch['verdict']} {ch['success']}/{ch['total']}" if ch["total"] else "no checks"
        print(f"{num:>6} {e['author_login'][:15]:<16} {e['review_state']:<18} "
              f"{ci:<14} {str(e['mergeable_state'])[:8]:<9} "
              f"{str(e['last_author_at'])[:19]:<20} {str(e['last_reviewer_at'])[:19]:<20}")


if __name__ == "__main__":
    main()
