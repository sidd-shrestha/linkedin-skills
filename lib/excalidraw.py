"""Generate Excalidraw diagram scenes + Pillow diagram renders.

Exports two things:
  1. ``.excalidraw`` JSON files — open in excalidraw.com or the desktop app
  2. Pillow-rendered images — embed directly in carousel PDFs without a browser

Diagram types:
  - flowchart   boxes + arrows in sequence
  - comparison  before / after side-by-side
  - framework   labelled pillars or nodes
  - timeline    vertical or horizontal steps
"""

from __future__ import annotations
import json
import os
import re
import uuid
from typing import Any, Optional

from PIL import Image, ImageDraw, ImageFont

from lib.carousel import _load_font, _clean_text

# ---------------------------------------------------------------------------
# Excalidraw JSON helpers
# ---------------------------------------------------------------------------

EXCALIDRAW_TEMPLATE: dict[str, Any] = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": [],
    "appState": {
        "gridSize": None,
        "viewBackgroundColor": "#ffffff",
    },
}

COLORS = {
    "accent": "#F5D952",
    "accent2": "#f0e8d8",
    "text": "#2c1810",
    "muted": "#aaa094",
    "blue": "#0A66C2",
}


def _el_id() -> str:
    return str(uuid.uuid4())[:8]


def _make_box(
    x: float, y: float, w: float, h: float,
    bg: str = "#ffffff",
    stroke: str = COLORS["text"],
    label: Optional[str] = None,
) -> list[dict]:
    els: list[dict] = []
    box = {
        "id": _el_id(),
        "type": "rectangle",
        "x": x, "y": y,
        "width": w, "height": h,
        "strokeColor": stroke,
        "backgroundColor": bg,
        "fillStyle": "solid",
        "strokeWidth": 2,
        "roughness": 0,
        "opacity": 100,
        "roundness": {"type": 3},
        "boundElements": [],
    }
    els.append(box)

    if label:
        tid = _el_id()
        bx = _el_id()
        text_el = {
            "id": tid,
            "type": "text",
            "x": x + w / 2,
            "y": y + h / 2 - 12,
            "width": w * 0.85,
            "height": 24,
            "text": label,
            "fontSize": 20,
            "fontFamily": 1,
            "textAlign": "center",
            "verticalAlign": "middle",
            "strokeColor": stroke,
            "containerId": bx,
            "roughness": 0,
            "opacity": 100,
        }
        box["boundElements"].append({"id": tid, "type": "text"})
        els.append(text_el)

    return els


def _make_arrow(x1: float, y1: float, x2: float, y2: float) -> dict:
    return {
        "id": _el_id(),
        "type": "arrow",
        "x": x1, "y": y1,
        "width": x2 - x1,
        "height": y2 - y1,
        "points": [[0, 0], [x2 - x1, y2 - y1]],
        "strokeColor": COLORS["accent"],
        "strokeWidth": 2,
        "roughness": 0,
        "opacity": 80,
        "roundness": {"type": 2},
        "startBinding": None,
        "endBinding": None,
    }


def _make_title_text(x: float, y: float, text: str, size: int = 28) -> dict:
    return {
        "id": _el_id(),
        "type": "text",
        "x": x, "y": y,
        "width": 800,
        "height": size + 8,
        "text": text,
        "fontSize": size,
        "fontFamily": 1,
        "textAlign": "left",
        "strokeColor": COLORS["text"],
        "roughness": 0,
        "opacity": 100,
    }


# ---------------------------------------------------------------------------
# Scene builders
# ---------------------------------------------------------------------------

def build_flowchart(
    steps: list[str],
    title: str = "",
) -> dict[str, Any]:
    """Build a horizontal flowchart. Each step becomes a box with arrows."""
    scene = dict(EXCALIDRAW_TEMPLATE)
    els: list[dict] = []
    y_center = 200
    box_w, box_h = 180, 60
    gap = 60

    if title:
        els.append(_make_title_text(60, 60, title))

    total_w = len(steps) * box_w + (len(steps) - 1) * gap
    start_x = max(60, (1080 - total_w) / 2)

    for i, step in enumerate(steps):
        x = start_x + i * (box_w + gap)
        els.extend(_make_box(x, y_center, box_w, box_h, label=step))

        if i < len(steps) - 1:
            ax = x + box_w
            ay = y_center + box_h / 2
            bx = ax + gap
            by = ay
            els.append(_make_arrow(ax, ay, bx, by))

    scene["elements"] = els
    return scene


def build_comparison(
    left_title: str,
    left_items: list[str],
    right_title: str,
    right_items: list[str],
    heading: str = "",
) -> dict[str, Any]:
    """Build a before/after comparison layout."""
    scene = dict(EXCALIDRAW_TEMPLATE)
    els: list[dict] = []

    if heading:
        els.append(_make_title_text(60, 60, heading))

    col_w = 320
    col_h = 50
    start_y = 160
    center_x = 540

    # left column
    lx = center_x - col_w - 40
    els.extend(_make_box(lx, start_y, col_w, 50, bg=COLORS["accent2"],
                          label=left_title, stroke=COLORS["accent"]))
    for i, item in enumerate(left_items):
        y = start_y + 70 + i * (col_h + 16)
        els.extend(_make_box(lx, y, col_w, col_h, label=item))

    # arrow
    arrow_x1 = center_x - 20
    arrow_y1 = start_y + 25
    arrow_x2 = center_x + 20
    els.append(_make_arrow(arrow_x1, arrow_y1, arrow_x2, arrow_y1))

    # right column
    rx = center_x + 40
    els.extend(_make_box(rx, start_y, col_w, 50, bg=COLORS["accent"],
                          label=right_title, stroke=COLORS["text"]))
    for i, item in enumerate(right_items):
        y = start_y + 70 + i * (col_h + 16)
        els.extend(_make_box(rx, y, col_w, col_h, label=item))

    scene["elements"] = els
    return scene


def build_framework(
    items: list[tuple[str, str]],
    title: str = "",
) -> dict[str, Any]:
    """Build a pillar / node framework (e.g. 3 rounded boxes stacked or side-by-side)."""
    scene = dict(EXCALIDRAW_TEMPLATE)
    els: list[dict] = []

    if title:
        els.append(_make_title_text(60, 60, title))

    n = len(items)
    box_w = min(260, (800 - (n - 1) * 20) // n)
    box_h = 200
    gap = (800 - n * box_w) // (n - 1) if n > 1 else 0
    start_x = (1080 - (n * box_w + (n - 1) * gap)) / 2
    y_center = 200

    for i, (header, body) in enumerate(items):
        x = start_x + i * (box_w + gap)
        els.extend(_make_box(x, y_center, box_w, 50, bg=COLORS["accent"],
                              label=header, stroke=COLORS["text"]))
        if body:
            lines = body.split("\n")
            for j, line in enumerate(lines):
                ly = y_center + 60 + j * 36
                els.extend(_make_box(x, ly, box_w, 32, bg=COLORS["accent2"],
                                      label=line, stroke=COLORS["muted"]))

    scene["elements"] = els
    return scene


def save_scene(scene: dict[str, Any], path: str):
    """Save an Excalidraw scene dict as a ``.excalidraw`` JSON file."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(scene, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Pillow diagram rendering (for carousel inclusion without a browser)
# ---------------------------------------------------------------------------

def _draw_rounded_box(
    draw: ImageDraw.ImageDraw,
    x: int, y: int, w: int, h: int,
    fill: str, outline: str,
):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=fill, outline=outline, width=2)


def render_flowchart(
    steps: list[str],
    theme: dict,
    heading: str = "",
) -> Image.Image:
    """Render a flowchart as a Pillow image for carousel use."""
    img = Image.new("RGB", (1080, 1080), theme["bg"])
    draw = ImageDraw.Draw(img)
    title_f = _load_font(36)
    font = _load_font(28)
    small_font = _load_font(22)
    accent = theme["accent"]
    text_c = theme["text"]

    y_offset = 100
    if heading:
        draw.text((60, y_offset), heading, fill=text_c, font=title_f)
        uw = min(len(heading) * 20, 200)
        draw.rectangle([60, y_offset + 42, 60 + uw, y_offset + 46], fill=accent)
        y_offset += 80

    box_w, box_h = 180, 60
    gap = 50
    total_w = len(steps) * box_w + (len(steps) - 1) * gap
    start_x = max(40, (1080 - total_w) // 2)
    y_center = y_offset + 180

    for i, step in enumerate(steps):
        x = start_x + i * (box_w + gap)
        _draw_rounded_box(draw, x, y_center, box_w, box_h,
                          fill=theme["accent2"], outline=accent)
        tw = small_font.getbbox(str(i + 1))[2]
        draw.text((x + 10, y_center + 4), str(i + 1), fill=accent, font=small_font)
        draw.text((x + 10 + tw + 8, y_center + 6), step, fill=text_c, font=small_font)

        if i < len(steps) - 1:
            ax = x + box_w + 4
            ay = y_center + box_h // 2
            bx = ax + gap - 8
            draw.line([(ax, ay), (bx, ay)], fill=accent, width=3)
            # arrowhead
            draw.polygon([(bx, ay), (bx - 10, ay - 6), (bx - 10, ay + 6)], fill=accent)

    return img


def render_comparison(
    left_title: str,
    left_items: list[str],
    right_title: str,
    right_items: list[str],
    theme: dict,
) -> Image.Image:
    """Render a before/after comparison as a Pillow image."""
    img = Image.new("RGB", (1080, 1080), theme["bg"])
    draw = ImageDraw.Draw(img)
    font = _load_font(26)
    title_f = _load_font(34)
    accent = theme["accent"]
    text_c = theme["text"]

    col_w = 360
    col_h = 45
    start_y = 300
    center_x = 540

    def draw_col(x, t, items):
        _draw_rounded_box(draw, x, start_y, col_w, 55,
                          fill=accent, outline=accent)
        draw.text((x + 20, start_y + 12), t, fill=theme["bg"], font=title_f)
        for i, item in enumerate(items):
            y = start_y + 80 + i * (col_h + 12)
            _draw_rounded_box(draw, x, y, col_w, col_h,
                              fill=theme["accent2"], outline=accent)
            draw.text((x + 16, y + 10), item, fill=text_c, font=font)

    draw_col(center_x - col_w - 30, left_title, left_items)
    draw_col(center_x + 30, right_title, right_items)

    ax = center_x - 10
    ay = start_y + 27
    bx = center_x + 10
    draw.line([(ax, ay), (bx, ay)], fill=accent, width=3)
    draw.polygon([(bx, ay), (bx - 10, ay - 6), (bx - 10, ay + 6)], fill=accent)

    return img


def render_framework(
    items: list[tuple[str, str]],
    theme: dict,
) -> Image.Image:
    """Render a node framework as a Pillow image."""
    img = Image.new("RGB", (1080, 1080), theme["bg"])
    draw = ImageDraw.Draw(img)
    font = _load_font(24)
    hdr_f = _load_font(28)
    accent = theme["accent"]
    text_c = theme["text"]

    n = len(items)
    box_w = min(260, (900 - (n - 1) * 20) // n)
    gap = (900 - n * box_w) // (n - 1) if n > 1 else 0
    start_x = (1080 - (n * box_w + (n - 1) * gap)) // 2
    y_top = 300

    for i, (header, body) in enumerate(items):
        x = start_x + i * (box_w + gap)
        _draw_rounded_box(draw, x, y_top, box_w, 50,
                          fill=accent, outline=accent)
        draw.text((x + 16, y_top + 10), header, fill=theme["bg"], font=hdr_f)

        lines = body.split("\n")
        for j, line in enumerate(lines):
            ly = y_top + 65 + j * 38
            _draw_rounded_box(draw, x, ly, box_w, 32,
                              fill=theme["accent2"], outline=accent)
            draw.text((x + 12, ly + 5), line, fill=text_c, font=font)

    return img
