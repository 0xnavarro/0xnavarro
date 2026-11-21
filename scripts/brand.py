"""Shared brand tokens and SVG helpers for the 0xnavarro profile.

Colours and type follow https://www.0xnavarro.com: ink, cream and bronze,
Instrument Serif for display and Inter for text. Standard library only, so the
daily GitHub Action can import it without installing anything.
"""

from __future__ import annotations

import base64
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONTS = ASSETS / "fonts"

THEMES = {
    "dark": {
        "bg": "#0F1115",
        "surface": "#161A20",
        "border": "#2A2F37",
        "strong": "#343B45",
        "text": "#F5F1E8",
        "text2": "#B8B1A6",
        "muted": "#8F897F",
        "accent": "#A48B73",
        "heat": ["#1B2027", "#3B342D", "#5F5245", "#8F7963", "#CDB396"],
    },
    "light": {
        "bg": "#F5F1E8",
        "surface": "#EDE7DB",
        "border": "#DCD3C3",
        "strong": "#C9BEAB",
        "text": "#0F1115",
        "text2": "#45413B",
        "muted": "#6B655C",
        "accent": "#7A6552",
        "heat": ["#E6DFD1", "#D5C6B0", "#B79F86", "#8F7963", "#5A4838"],
    },
}

FONT_FILES = {
    "serif": ("IS", "normal", 400, "InstrumentSerif-Regular.subset.woff2"),
    "serif-italic": ("IS", "italic", 400, "InstrumentSerif-Italic.subset.woff2"),
    "sans-400": ("Inter", "normal", 400, "Inter-400.subset.woff2"),
    "sans-500": ("Inter", "normal", 500, "Inter-500.subset.woff2"),
    "sans-600": ("Inter", "normal", 600, "Inter-600.subset.woff2"),
    "mono": ("JBM", "normal", 500, "JetBrainsMono-500.subset.woff2"),
}

STACKS = (
    ".serif{font-family:'IS',Georgia,'Times New Roman',serif;font-weight:400}"
    ".sans{font-family:'Inter',-apple-system,'Segoe UI',Helvetica,Arial,sans-serif}"
    ".mono{font-family:'JBM',ui-monospace,SFMono-Regular,Menlo,monospace;font-weight:500}"
)


def font_css(*keys: str) -> str:
    rules = []
    for key in keys:
        family, style, weight, filename = FONT_FILES[key]
        data = base64.b64encode((FONTS / filename).read_bytes()).decode("ascii")
        rules.append(
            f"@font-face{{font-family:'{family}';font-style:{style};font-weight:{weight};"
            f"src:url(data:font/woff2;base64,{data}) format('woff2')}}"
        )
    return "".join(rules) + STACKS


def text(x, y, content, cls, size, fill, anchor="start", weight=None, spacing=None, extra=""):
    attrs = [f'x="{x:g}"', f'y="{y:g}"', f'class="{cls}"', f'font-size="{size}"', f'fill="{fill}"']
    if anchor != "start":
        attrs.append(f'text-anchor="{anchor}"')
    if weight:
        attrs.append(f'font-weight="{weight}"')
    if spacing:
        attrs.append(f'letter-spacing="{spacing}"')
    if extra:
        attrs.append(extra)
    return f"<text {' '.join(attrs)}>{escape(content)}</text>"


def panel(width, height, t):
    return (
        f'<rect x="0.75" y="0.75" width="{width - 1.5}" height="{height - 1.5}" rx="20" '
        f'fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="1.5"/>'
    )


def svg(width, height, title, desc, css, body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="t d">'
        f'<title id="t">{escape(title)}</title><desc id="d">{escape(desc)}</desc>'
        f"<style>{css}</style>{body}</svg>\n"
    )


def write(name: str, content: str) -> Path:
    path = ASSETS / name
    path.write_text(content, encoding="utf-8")
    return path
