#!/usr/bin/env python3
"""Render the build log: the last year of GitHub contributions as a heatmap.

Standard library only. Reads GITHUB_TOKEN (or GH_TOKEN) and writes
assets/build-log-dark.svg and assets/build-log-light.svg. The counts are the
ones GitHub shows on the public profile, private contributions included.

    python3 scripts/build_log.py            # fetch and write
    python3 scripts/build_log.py --check    # fetch and print, write nothing
    python3 scripts/build_log.py --from calendar.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from datetime import date

from brand import THEMES, font_css, panel, svg, text, write

LOGIN = "0xnavarro"
QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date weekday contributionCount contributionLevel } }
      }
    }
  }
}
"""
LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def fetch() -> dict:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        sys.exit("GITHUB_TOKEN or GH_TOKEN is required")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "profile-build-log"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if payload.get("errors"):
        sys.exit(f"GraphQL errors: {payload['errors']}")
    return payload


def calendar(payload: dict) -> dict:
    return payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def stats(cal: dict) -> dict:
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    streak = 0
    for d in reversed(days):
        if d["contributionCount"] > 0:
            streak += 1
        elif d is days[-1]:
            continue  # today may simply not have started yet
        else:
            break
    return {
        "total": cal["totalContributions"],
        "active": sum(1 for d in days if d["contributionCount"] > 0),
        "days": len(days),
        "streak": streak,
        "last": days[-1]["date"],
    }


def render(cal: dict, s: dict, theme: str) -> str:
    t = THEMES[theme]
    W, H = 1000, 356
    x0, y0, pitch, cell = 56, 214, 16.75, 13.25
    updated = date.fromisoformat(s["last"])
    body = [panel(W, H, t)]
    body.append(text(56, 64, "BUILD LOG · LAST 12 MONTHS", "mono", 13, t["muted"], spacing=2.6))
    body.append(
        text(944, 64, f"UPDATED {updated.day} {MONTHS[updated.month - 1].upper()} {updated.year}",
             "mono", 13, t["muted"], anchor="end", spacing=2.6)
    )
    body.append(text(52, 146, f"{s['total']:,}", "serif", 78, t["text"], spacing=-1))
    body.append(text(944, 128, f"{s['streak']}", "serif", 44, t["text"], anchor="end"))
    body.append(text(944, 154, "day streak", "sans", 16, t["muted"], anchor="end", weight=400))
    body.append(text(800, 128, f"{s['active']}", "serif", 44, t["text"], anchor="end"))
    body.append(text(800, 154, f"active days of {s['days']}", "sans", 16, t["muted"], anchor="end", weight=400))
    body.append(
        text(56, 184, "contributions in the last year, most of them in private company repositories.",
             "sans", 19, t["text2"], weight=400)
    )

    last_month = None
    for col, week in enumerate(cal["weeks"]):
        x = x0 + col * pitch
        first = week["contributionDays"][0]["date"]
        month = int(first[5:7])
        if month != last_month and col < len(cal["weeks"]) - 2:
            if last_month is not None:
                body.append(text(x, y0 + 7 * pitch + 18, MONTHS[month - 1], "mono", 11, t["muted"]))
            last_month = month
        for day in week["contributionDays"]:
            y = y0 + day["weekday"] * pitch
            fill = t["heat"][LEVELS.get(day["contributionLevel"], 0)]
            body.append(
                f'<rect x="{x:.2f}" y="{y:.2f}" width="{cell}" height="{cell}" rx="3" fill="{fill}">'
                f'<title>{day["date"]}: {day["contributionCount"]}</title></rect>'
            )

    desc = (
        f"{s['total']:,} GitHub contributions in the last year, most of them in private company "
        f"repositories. Active on {s['active']} of {s['days']} days; current streak {s['streak']} days. "
        f"Updated {s['last']}."
    )
    return svg(W, H, "Build log", desc, font_css("serif", "sans-400", "mono"), "".join(body))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="print the numbers, write nothing")
    parser.add_argument("--from", dest="source", help="read a saved GraphQL response instead of fetching")
    args = parser.parse_args()

    payload = json.load(open(args.source)) if args.source else fetch()
    cal = calendar(payload)
    s = stats(cal)
    print(json.dumps(s))
    if s["total"] <= 0 or s["days"] < 300:
        sys.exit("calendar looks incomplete; not writing")
    if args.check:
        return
    for theme in THEMES:
        write(f"build-log-{theme}.svg", render(cal, s, theme))


if __name__ == "__main__":
    main()
