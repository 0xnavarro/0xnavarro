#!/usr/bin/env python3
"""Build the static profile visuals (hero, method, path, sign-off) in both themes.

fontTools is used only to measure text so nothing overflows:
    pip install fonttools brotli && python3 scripts/build_assets.py
The daily build log is generated separately by scripts/build_log.py.
"""

from __future__ import annotations

import re
import sys
from functools import lru_cache

from fontTools.ttLib import TTFont

from brand import ASSETS, FONT_FILES, FONTS, THEMES, font_css, panel, svg, text, write

HEART = (
    "M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 1 0-7.78 7.78"
    "l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"
)
BRIDA_PATH = re.search(r' d="([^"]+)"', (ASSETS / "logos/brida-mark.svg").read_text()).group(1)


@lru_cache(maxsize=None)
def _font(key):
    font = TTFont(FONTS / FONT_FILES[key][3])
    return font.getBestCmap(), font["hmtx"], font["head"].unitsPerEm


def measure(s: str, key: str, size: float, spacing: float = 0) -> float:
    cmap, hmtx, upm = _font(key)
    width = 0
    for ch in s:
        glyph = cmap.get(ord(ch))
        if glyph is None:
            sys.exit(f"glyph missing for {ch!r} in {key}")
        width += hmtx[glyph][0]
    return width * size / upm + spacing * len(s)


def fits(s, key, size, limit, spacing=0):
    w = measure(s, key, size, spacing)
    if w > limit:
        sys.exit(f"text overflows ({w:.0f}px > {limit}px): {s!r}")
    return w


def vitalink_icon(x, y, size, uid):
    return (
        f'<g transform="translate({x:g} {y:g}) scale({size / 32:g})">'
        f'<defs><linearGradient id="vg{uid}" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="#22c55e"/><stop offset="1" stop-color="#3b82f6"/>'
        f'</linearGradient></defs><circle cx="16" cy="16" r="16" fill="url(#vg{uid})"/>'
        f'<g transform="translate(7 7) scale(0.75)"><path d="{HEART}" fill="none" stroke="#fff" '
        f'stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></g></g>'
    )


def brida_mark(x, y, size, fill):
    return (
        f'<g transform="translate({x:g} {y:g}) scale({size / 256:g})">'
        f'<path d="{BRIDA_PATH}" fill="{fill}" fill-rule="evenodd"/></g>'
    )


def brida_tile_at(x, y, size):
    """Brida's mark in white on a black tile, so it reads on both themes."""
    inset = size * 0.16
    return (
        f'<rect x="{x:g}" y="{y:g}" width="{size}" height="{size}" rx="{size * 0.24:g}" fill="#0A0A0A"/>'
        + brida_mark(x + inset, y + inset, size - 2 * inset, "#FFFFFF")
    )


def monogram(x, y, t, size=48):
    """The CN mark from the favicon on 0xnavarro.com."""
    return (
        f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size * 0.19:g}" '
        f'fill="{t["surface"]}" stroke="{t["border"]}" stroke-width="1.2"/>'
        + text(x + size / 2, y + size * 0.665, "CN", "serif", round(size * 0.5), t["text"], anchor="middle", spacing=-0.5)
        + f'<line x1="{x + size * 0.22:g}" y1="{y + size * 0.83:g}" x2="{x + size * 0.78:g}" '
        f'y2="{y + size * 0.83:g}" stroke="{t["accent"]}" stroke-width="1.6" stroke-linecap="round"/>'
    )


MOTION_OFF = "@media (prefers-reduced-motion: reduce){.flow,.pulse{animation:none}.flow{opacity:0}}"


def hero(theme):
    t = THEMES[theme]
    W, H = 1000, 452
    name = "Carlos Navarro"
    line = "Building technology companies in complex markets."
    sub = "I build the companies and write the software behind them."
    fits(name, "serif", 100, 640, -1)
    fits(line, "sans-500", 27, 760)
    fits(sub, "sans-400", 20, 640)

    body = [panel(W, H, t), monogram(56, 52, t)]
    body.append(text(944, 82, "FOUNDER · BUILDER · CEO", "mono", 13, t["muted"], anchor="end", spacing=2.6))
    body.append(text(52, 232, name, "serif", 100, t["text"], spacing=-1))
    body.append(text(56, 282, line, "sans", 27, t["text"], weight=500))
    body.append(text(56, 318, sub, "sans", 20, t["muted"], weight=400))

    # Ventures, as chips with each company's own mark.
    x, y, h = 56, 352, 46
    for kind, label, role in (("vitalink", "Vitalink", "Co-founder, CEO & CTO"), ("brida", "Brida", "Founder & CEO")):
        nw = measure(label, "sans-600", 19)
        rw = measure(role, "sans-400", 19)
        w = 14 + 24 + 11 + nw + 9 + rw + 20
        body.append(
            f'<rect x="{x:g}" y="{y}" width="{w:.1f}" height="{h}" rx="{h / 2:g}" '
            f'fill="{t["surface"]}" stroke="{t["border"]}" stroke-width="1.2"/>'
        )
        if kind == "vitalink":
            body.append(vitalink_icon(x + 14, y + 11, 24, theme))
        else:
            body.append(brida_tile_at(x + 14, y + 11, 24))
        body.append(text(x + 49, y + 29.5, label, "sans", 19, t["text"], weight=600))
        body.append(text(x + 49 + nw + 9, y + 29.5, role, "sans", 19, t["muted"], weight=400))
        x += w + 12

    # A decision travelling through a grid until it becomes work.
    gx, gy, step = 728, 112, 36
    dots = [
        f'<circle cx="{gx + c * step}" cy="{gy + r * step}" r="1.7" fill="{t["strong"]}"/>'
        for r in range(4)
        for c in range(7)
    ]
    route = [(0, 3), (2, 3), (2, 2), (4, 2), (4, 1), (6, 1), (6, 0)]
    pts = " ".join(f"{gx + c * step},{gy + r * step}" for c, r in route)
    length = sum(
        abs(route[i + 1][0] - route[i][0]) * step + abs(route[i + 1][1] - route[i][1]) * step
        for i in range(len(route) - 1)
    )
    ex, ey = gx + 6 * step, gy
    body += dots
    body.append(
        f'<polyline points="{pts}" fill="none" stroke="{t["accent"]}" stroke-opacity="0.55" '
        f'stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"/>'
    )
    body.append(
        f'<polyline class="flow" points="{pts}" fill="none" stroke="{t["accent"]}" stroke-width="2.6" '
        f'stroke-linecap="round" stroke-dasharray="30 {length}"/>'
    )
    for c, r in ((2, 2), (4, 1)):
        body.append(
            f'<circle cx="{gx + c * step}" cy="{gy + r * step}" r="3.6" fill="{t["bg"]}" '
            f'stroke="{t["accent"]}" stroke-width="1.6"/>'
        )
    body.append(f'<circle cx="{gx}" cy="{gy + 3 * step}" r="5.5" fill="{t["bg"]}" stroke="{t["accent"]}" stroke-width="1.8"/>')
    body.append(f'<circle class="pulse" cx="{ex}" cy="{ey}" r="12" fill="{t["accent"]}" opacity="0.16"/>')
    body.append(f'<circle cx="{ex}" cy="{ey}" r="5.5" fill="{t["accent"]}"/>')

    css = (
        font_css("serif", "sans-400", "sans-500", "sans-600", "mono")
        + f"@keyframes flow{{0%{{stroke-dashoffset:30}}72%,100%{{stroke-dashoffset:-{length}}}}}"
        + ".flow{animation:flow 5.2s cubic-bezier(.55,.1,.35,1) infinite}"
        + "@keyframes pulse{0%,66%{opacity:.16}78%{opacity:.5}100%{opacity:.16}}"
        + ".pulse{animation:pulse 5.2s ease-out infinite}"
        + MOTION_OFF
    )
    return svg(
        W, H,
        "Carlos Navarro",
        "Founder, builder, CEO. Building technology companies in complex markets. I build the companies and write the software behind them. Co-founder, CEO and CTO of Vitalink; founder and CEO of Brida.",
        css, "".join(body),
    )


METHOD = [
    ("01", "Spec", "written requirement"),
    ("02", "Plan", "reviewed before code"),
    ("03", "Build", "agents in worktrees"),
    ("04", "Gate", "tests · CI · review"),
    ("05", "Ship", "deploy · observe"),
]


def method(theme):
    t = THEMES[theme]
    W, H = 1000, 220
    xs = [116 + i * 192 for i in range(len(METHOD))]
    line_y = 102
    length = xs[-1] - xs[0]
    body = [panel(W, H, t)]
    body.append(f'<line x1="{xs[0]}" y1="{line_y}" x2="{xs[-1]}" y2="{line_y}" stroke="{t["border"]}" stroke-width="2"/>')
    body.append(
        f'<line class="flow" x1="{xs[0]}" y1="{line_y}" x2="{xs[-1]}" y2="{line_y}" stroke="{t["accent"]}" '
        f'stroke-width="2.6" stroke-linecap="round" stroke-dasharray="70 {length}"/>'
    )
    for i, (x, (num, label, sub)) in enumerate(zip(xs, METHOD)):
        fits(sub, "sans-400", 17, 184)
        last = i == len(METHOD) - 1
        body.append(text(x, 62, num, "mono", 13, t["muted"], anchor="middle", spacing=2))
        body.append(
            f'<circle cx="{x}" cy="{line_y}" r="8" fill="{t["accent"] if last else t["bg"]}" '
            f'stroke="{t["accent"]}" stroke-width="2"/>'
        )
        body.append(text(x, 158, label, "serif", 36, t["text"], anchor="middle"))
        body.append(text(x, 188, sub, "sans", 17, t["muted"], anchor="middle", weight=400))
    css = (
        font_css("serif", "sans-400", "mono")
        + f"@keyframes flow{{0%{{stroke-dashoffset:70}}80%,100%{{stroke-dashoffset:-{length}}}}}"
        + ".flow{animation:flow 6s cubic-bezier(.55,.1,.35,1) infinite}"
        + MOTION_OFF
    )
    desc = "How I build: " + "; ".join(f"{label} ({sub})" for _, label, sub in METHOD) + "."
    return svg(W, H, "How I build", desc, css, "".join(body))


PATH = [
    # year, title, role, proof tags, current. Source: Carlos's LinkedIn profile and essays.
    ("2026", "Brida", "Founder & CEO · build your company by talking",
     ["Agents on company data", "MCP", "Open evaluation research"], True),
    ("2025", "Vitalink", "Co-founder, CEO & CTO · the action layer for healthcare",
     ["Expediente + agent", "Credential", "Pay", "Patient agent"], True),
    ("2024", "ADSA", "Autonomous data-science agents on o1 and Claude 3.5 Sonnet",
     ["71st of 2,461 on Kaggle", "Whitepaper"], False),
    ("2023", "Head of IT Systems, Insigna Médica", "Hospital IT, BI and operations in Mexico City, to mid-2026",
     ["Where I saw the cash-pay problem"], False),
    ("2022", "Maria", "A GPT-3 assistant inside WhatsApp, built over Christmas",
     ["20,000+ users", "Word of mouth"], False),
    ("", "Atenea Labs", "Founded my AI lab, today the holding behind my companies", [], False),
    ("", "CTO, Casa-Facil.com", "Zurich, Switzerland", [], False),
    ("2020", "Rigfarm", "First company: built and sold crypto-mining rigs in Europe",
     ["Closed when Ethereum left proof-of-work"], False),
    ("2016", "Vía Inteligente", "First tech job: footfall analytics with connected hardware",
     ["Data systems", "Software architecture"], False),
    ("2015", "Chess", "Professional player and coach, 2000 FIDE",
     ["Castilla-La Mancha U18 champion", "Andrés Iniesta award"], False),
]


def pill(x, y, label, t):
    label = label.upper()
    w = measure(label, "mono", 12.5, 1.3) + 26
    return w, (
        f'<rect x="{x:g}" y="{y:g}" width="{w:.1f}" height="28" rx="14" fill="{t["surface"]}" '
        f'stroke="{t["border"]}" stroke-width="1.1"/>'
        + text(x + 13, y + 18.5, label, "mono", 12.5, t["text2"], spacing=1.3)
    )


def path(theme):
    t = THEMES[theme]
    W = 1000
    line_x, text_x, right = 204, 240, 944
    top = 76
    ys, y = [], top
    for _, _, _, tags, _ in PATH:
        ys.append(y)
        y += 138 if tags else 104
    H = ys[-1] + (112 if PATH[-1][3] else 70)
    body = [panel(W, H, t)]
    body.append(
        f'<line x1="{line_x}" y1="{ys[0]}" x2="{line_x}" y2="{ys[-1]}" stroke="{t["border"]}" stroke-width="2"/>'
    )
    for y, (year, title, role, tags, now) in zip(ys, PATH):
        fits(title, "sans-600", 30, right - text_x)
        fits(role, "sans-400", 22, right - text_x)
        if year:
            body.append(text(170, y + 15, year, "serif", 44, t["accent"], anchor="end"))
        if now:
            body.append(text(170, y + 40, "TO NOW", "mono", 11.5, t["muted"], anchor="end", spacing=2))
            body.append(f'<circle cx="{line_x}" cy="{y}" r="15" fill="{t["accent"]}" opacity="0.16"/>')
        body.append(
            f'<circle cx="{line_x}" cy="{y}" r="8" fill="{t["accent"] if now else t["bg"]}" '
            f'stroke="{t["accent"]}" stroke-width="2"/>'
        )
        body.append(text(text_x, y + 10, title, "sans", 30, t["text"], weight=600))
        body.append(text(text_x, y + 44, role, "sans", 22, t["text2"], weight=400))
        x = text_x
        for tag in tags:
            w, svg_pill = pill(x, y + 62, tag, t)
            if x + w > right:
                raise SystemExit(f"tags overflow on {title}")
            body.append(svg_pill)
            x += w + 10
    desc = "My path, newest first: " + "; ".join(
        f"{year + ': ' if year else ''}{title}, {role}" + (f" ({', '.join(tags)})" if tags else "")
        for year, title, role, tags, _ in PATH
    ) + "."
    return svg(W, H, "Path", desc, font_css("serif", "sans-400", "sans-600", "mono"), "".join(body))


def signoff(theme):
    t = THEMES[theme]
    W, H = 1000, 150
    line = "Agents do the work. People own the decisions."
    fits(line, "serif-italic", 34, 900)
    body = [monogram(W / 2 - 22, 8, t, size=44)]
    body.append(text(W / 2, 112, line, "serif", 34, t["text2"], anchor="middle", extra='font-style="italic"'))
    return svg(W, H, "Sign-off", line, font_css("serif", "serif-italic"), "".join(body))


def brida_tile():
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32" role="img" aria-label="Brida">'
        + brida_tile_at(0, 0, 32) + "</svg>\n"
    )


def main():
    write("logos/brida-tile.svg", brida_tile())
    for theme in THEMES:
        for name, fn in (("hero", hero), ("method", method), ("path", path), ("signoff", signoff)):
            out = write(f"{name}-{theme}.svg", fn(theme))
            print(f"{out.relative_to(ASSETS.parent)}  {out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
