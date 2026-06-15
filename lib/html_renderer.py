"""Playwright-based carousel renderer for LinkedIn Document Carousels.

Generates PDFs by rendering slides as HTML and converting via headless
Chromium. Keeps vector text, supports modern CSS, and produces pixel-perfect
1080x1080 pages.

Usage (indirectly via carousel.py):
    from lib.carousel import generate_carousel
    generate_carousel(post_text, renderer="playwright")
"""

from __future__ import annotations
import asyncio
import os
import re
import tempfile
from pathlib import Path
from typing import Optional

from PIL import Image
from jinja2 import Environment, FileSystemLoader

from lib.carousel import CANVAS_W, CANVAS_H, THEMES


TEMPLATE_DIR = Path(__file__).parent / "templates"
_TEMPLATE_ENV = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
_TEMPLATE = _TEMPLATE_ENV.get_template("slide.html")

PARA_SPLIT = re.compile(r"\n\s*\n")

CTA_EMOJI_MAP = {
    "comment": "\U0001f4ac",
    "thoughts": "\U0001f914",
    "agree": "\U0001f44d",
    "disagree": "\U0001f44e",
    "tag": "\U0001f3f7\ufe0f",
    "drop a": "\U0001f4cc",
    "what": "\u2753",
    "share this": "\U0001f504",
    "repost": "\u267b\ufe0f",
    "follow": "\u2795",
}

TITLE_EMOJIS = [
    "\U0001f680", "\U0001f4a1", "\U0001f4c8", "\U0001f3af",
    "\U0001f3d7\ufe0f", "\U0001f525", "\U0001f9e0", "\U0001f48e",
    "\U0001f4ca", "\u2699\ufe0f",
]


def _accent_to_html(text: str) -> str:
    return (
        text.replace("[accent]", '<span class="accent">')
        .replace("[/accent]", "</span>")
        .replace("[primary]", '<span class="accent">')
        .replace("[/primary]", "</span>")
    )


def _body_to_html(text: str) -> str:
    paragraphs = [p.strip() for p in PARA_SPLIT.split(text) if p.strip()]
    parts = [_accent_to_html(p) for p in paragraphs]
    return "".join(f"<p>{p}</p>" for p in parts)


def _detect_cta_emoji(body: str) -> str:
    lowered = body.lower()
    for pattern, emoji in CTA_EMOJI_MAP.items():
        if pattern in lowered:
            return emoji
    return "\U0001f4ac"


def _pick_watermark(slide: dict, slide_num: int, total: int, decorate: bool) -> str:
    if not decorate:
        return ""
    if slide.get("is_cta"):
        return _detect_cta_emoji(slide.get("body", ""))
    if slide.get("title") and slide_num == 1:
        idx = len(slide["title"]) % len(TITLE_EMOJIS)
        return TITLE_EMOJIS[idx]
    return ""


def _image_to_uri(path: str) -> str:
    return Path(os.path.abspath(path)).as_uri()


def _render_carousel_sync(
    slides: list[dict],
    *,
    theme_name: str = "minimal",
    decorate: bool = False,
    diagram_images: Optional[dict[int, Image.Image]] = None,
    logo_file: Optional[str] = None,
    logo_position: str = "top-right",
    logo_size: str = "medium",
    output_path: str,
    logo_drawn: bool = False,
) -> str:
    theme = THEMES.get(theme_name, THEMES["minimal"])
    total = len(slides)

    diagram_paths: dict[int, str] = {}
    if diagram_images:
        for idx, img in diagram_images.items():
            fd, path = tempfile.mkstemp(suffix=".png")
            os.close(fd)
            try:
                img.save(path, "PNG")
            except Exception:
                os.remove(path)
                continue
            diagram_paths[idx] = path

    html_path: Optional[str] = None

    try:
        html_slides = []
        for i, s in enumerate(slides):
            slide_num = i + 1
            watermark = _pick_watermark(s, slide_num, total, decorate)
            diagram_src = diagram_paths.get(i)
            if diagram_src:
                diagram_src = _image_to_uri(diagram_src)

            has_body = bool(s.get("body"))
            has_title = bool(s.get("title"))

            html_slides.append({
                "title": s.get("title", ""),
                "title_html": _accent_to_html(s.get("title", "")) if has_title else "",
                "body": s.get("body", ""),
                "body_html": _body_to_html(s.get("body", "")) if has_body else "",
                "is_cta": s.get("is_cta", False),
                "watermark": watermark,
                "diagram_src": diagram_src,
                "slide_num": slide_num,
            })

        logo_uri = _image_to_uri(logo_file) if logo_file else None

        html = _TEMPLATE.render(
            slides=html_slides,
            theme=theme,
            canvas_w=CANVAS_W,
            canvas_h=CANVAS_H,
            total=total,
            logo_file=logo_uri,
            logo_position=logo_position,
            logo_size=logo_size,
            logo_drawn=logo_drawn,
        )

        fd, html_path = tempfile.mkstemp(suffix=".html")
        os.close(fd)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        asyncio.run(_generate_pdf(html_path, output_path))

        return output_path

    finally:
        for path in diagram_paths.values():
            try:
                os.remove(path)
            except OSError:
                pass
        if html_path:
            try:
                os.remove(html_path)
            except OSError:
                pass


async def _generate_pdf(html_path: str, output_path: str):
    from playwright.async_api import async_playwright

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": CANVAS_W, "height": CANVAS_H},
            device_scale_factor=2,
        )
        page = await context.new_page()
        await page.goto(Path(html_path).as_uri(), wait_until="networkidle")
        await page.emulate_media(media="print")
        await page.pdf(
            path=output_path,
            width=f"{CANVAS_W}px",
            height=f"{CANVAS_H}px",
            print_background=True,
            margin={"top": "0px", "bottom": "0px", "left": "0px", "right": "0px"},
        )
        await browser.close()


def render_carousel(
    slides: list[dict],
    *,
    theme_name: str = "minimal",
    decorate: bool = False,
    diagram_images: Optional[dict[int, Image.Image]] = None,
    logo_file: Optional[str] = None,
    logo_position: str = "top-right",
    logo_size: str = "medium",
    output_path: str,
    logo_drawn: bool = False,
) -> str:
    """Render slides into a PDF using Playwright (headless Chromium).

    Args:
        slides: List of slide dicts with keys title, body, is_cta.
        theme_name: One of ``THEMES`` keys.
        decorate: Whether to add emoji watermarks.
        diagram_images: Map of slide index -> Pillow Image.
        logo_file: Path to logo image file.
        logo_position: Logo placement key.
        logo_size: Logo size key (small/medium/large).
        output_path: Absolute path for the output PDF.
        logo_drawn: Whether logo was already applied.

    Returns:
        Absolute path to generated PDF.
    """
    return _render_carousel_sync(
        slides,
        theme_name=theme_name,
        decorate=decorate,
        diagram_images=diagram_images,
        logo_file=logo_file,
        logo_position=logo_position,
        logo_size=logo_size,
        output_path=output_path,
        logo_drawn=logo_drawn,
    )
