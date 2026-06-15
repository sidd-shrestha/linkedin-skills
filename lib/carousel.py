"""Carousel PDF generator for LinkedIn Document Carousel format.

Fully local, zero API calls. Uses Pillow for slide rendering and
img2pdf for PDF compilation.

Usage:
    from lib.carousel import generate_carousel
    pdf_path = generate_carousel(post_text, title="My Post", theme="ink-yellow")
"""

from __future__ import annotations
import os
import re
import tempfile
from dataclasses import dataclass, field
from typing import Optional

from PIL import Image, ImageDraw, ImageFont, ImageFilter


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CANVAS_W = 1080
CANVAS_H = 1080

TITLE_FONT_SIZE = 52
BODY_FONT_SIZE = 34
SMALL_FONT_SIZE = 26
EMOJI_FONT_SIZE = 160

SPLIT_MARKER = "|||"

CTA_PATTERNS = re.compile(
    r"(comment|agree\?|disagree\?|thoughts\?|tag |♻️|"
    r"drop a |what.*\?|share this|repost|follow)", re.IGNORECASE
)

EM_DASH = re.compile(r"—")

LOGO_DIR = os.path.join(
    "drafts", "draft-carousels", "Claude",
)

ACCENT_TAG = re.compile(r"\[/?(?:accent|primary)\]")
RE_DECORATE = re.compile(r"\[decorate\]", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Themes
# ---------------------------------------------------------------------------

THEMES = {
    "minimal": {
        "bg": "#ffffff",
        "text": "#1a1a1a",
        "accent": "#0A66C2",
        "accent2": "#dce6f0",
        "num": "#999999",
        "emoji": "💬",
    },
    "dark": {
        "bg": "#1a1a1a",
        "text": "#f0f0f0",
        "accent": "#0A66C2",
        "accent2": "#2a2a2a",
        "num": "#555555",
        "emoji": "🌙",
    },
    "ink-yellow": {
        "bg": "#faf8f5",
        "text": "#2c1810",
        "accent": "#F5D952",
        "accent2": "#f0e8d8",
        "num": "#aaa094",
        "emoji": "📝",
    },
    "neon": {
        "bg": "#0d0d0d",
        "text": "#e0e0e0",
        "accent": "#39ff14",
        "accent2": "#1a1a1a",
        "num": "#444444",
        "emoji": "⚡",
    },
    "bold": {
        "bg": "#0A66C2",
        "text": "#ffffff",
        "accent": "#ffffff",
        "accent2": "#0854a0",
        "num": "#b0cff0",
        "emoji": "💡",
    },
}

CTA_EMOJIS = {
    "comment": "💬",
    "thoughts": "🤔",
    "agree": "👍",
    "disagree": "👎",
    "tag": "🏷️",
    "drop a": "📌",
    "what": "❓",
    "share this": "🔄",
    "repost": "♻️",
    "follow": "➕",
}

TITLE_EMOJIS = ["🚀", "💡", "📈", "🎯", "🏗️", "🔥", "🧠", "💎", "📊", "⚙️"]


# ---------------------------------------------------------------------------
# Font helpers
# ---------------------------------------------------------------------------

def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\SegoeUI.ttf",
        "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidates:
        if os.path.isfile(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _load_emoji_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:\\Windows\\Fonts\\seguiemj.ttf",
        "C:\\Windows\\Fonts\\SegUIVar.ttf",
    ]
    for path in candidates:
        if os.path.isfile(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return _load_font(size)


# ---------------------------------------------------------------------------
# Draft parsing
# ---------------------------------------------------------------------------

RE_LOGO = re.compile(
    r"(?:\[claude\s+logo\s*(.*?)\]|\(!logo\(([^)]+)\)\))", re.IGNORECASE
)
RE_DIAGRAM_BLOCK = re.compile(
    r"\[\[(flowchart|comparison|framework)(?:\s*:\s*(.+?)|\s[^]]*?)?\]\]",
    re.IGNORECASE
)
RE_HEADING = re.compile(r"^##\s?(.+)$", re.MULTILINE)
RE_STRIP_HEADING = re.compile(r"^##\s*")


@dataclass
class DraftParseResult:
    cleaned: str = ""
    logo_position: Optional[str] = None
    logo_name: str = ""
    logo_size: str = "medium"
    diagram_slides: dict[int, dict] = field(default_factory=dict)
    slide_headings: dict[int, str] = field(default_factory=dict)
    has_accent: bool = False
    decorate: bool = False


def _pick_logo_path(name: str = "") -> Optional[str]:
    """Find a Claude logo in ``LOGO_DIR``.

    If *name* is given (e.g. ``"claude_logo_2"``), try to match it to a
    numbered file. Otherwise pick the best available.
    """
    if not os.path.isdir(LOGO_DIR):
        return None

    # name-based resolution: claude_logo_2 -> Claude_Logo_2.<ext>
    if name:
        name = name.lower().replace(" ", "_").replace("-", "_")
        parts = name.split("_")
        num_part = ""
        for p in parts:
            if p.isdigit():
                num_part = p
                break
        for f in sorted(os.listdir(LOGO_DIR)):
            if num_part and num_part in f:
                fp = os.path.join(LOGO_DIR, f)
                if os.path.isfile(fp):
                    return fp

    # default: icon PNG first, then any PNG, then any image
    for f in sorted(os.listdir(LOGO_DIR)):
        if "icon" in f.lower() and f.lower().endswith((".png", ".webp", ".jpg", ".jpeg")):
            return os.path.join(LOGO_DIR, f)
    for f in sorted(os.listdir(LOGO_DIR)):
        if f.lower().endswith((".png", ".webp", ".jpg", ".jpeg")):
            return os.path.join(LOGO_DIR, f)
    return None


def parse_draft(text: str) -> DraftParseResult:
    """Extract instructions from draft text.

    Strips ``[claude logo]``, ``[[flowchart: ...]]``, ``[accent]`` markers,
    resolves ``## Heading`` for diagram titles, and returns cleaned text
    plus structured metadata.
    """
    result = DraftParseResult()
    result.has_accent = bool(ACCENT_TAG.search(text))
    result.decorate = bool(RE_DECORATE.search(text))

    # ---- diagram blocks [[type: ...]] -----------------------------------
    diag_matches = list(RE_DIAGRAM_BLOCK.finditer(text))

    # ---- headings -------------------------------------------------------
    heading_matches = list(RE_HEADING.finditer(text))

    # ---- claude logo ----------------------------------------------------
    logo_match = RE_LOGO.search(text)
    if logo_match:
        pos_text = (logo_match.group(1) or logo_match.group(2) or "").strip().lower()
        result.logo_name = pos_text
        if "center" in pos_text or "bottom" in pos_text:
            result.logo_position = "center-bottom"
        elif "top" in pos_text:
            result.logo_position = "top-right"
        else:
            result.logo_position = "center-bottom"
        if "tiny" in pos_text or "small" in pos_text:
            result.logo_size = "small"
        elif "large" in pos_text or "big" in pos_text:
            result.logo_size = "large"
        else:
            result.logo_size = "medium"

    # ---- determine slide indices for diagram blocks ---------------------
    # We work on the cleaned text where ||| are preserved for splitting
    # We need to figure out which slide index each diagram falls on.
    # Approach: split text by |||, check which segment contains each diagram match.

    # First strip instructions that should be removed entirely from text
    cleaned = text

    # Remove [claude logo ...] lines entirely
    cleaned = RE_LOGO.sub("", cleaned)

    # Remove diagram blocks
    cleaned = RE_DIAGRAM_BLOCK.sub("", cleaned)

    # Remove [accent] tags (they stay as markers for rendering)
    # but also remove pure instruction lines like [[diagram generated...]]
    cleaned = re.sub(r"\[\[[^\]]*diagram[^\]]*\]\]", "", cleaned)

    # Remove [decorate] marker
    cleaned = RE_DECORATE.sub("", cleaned)

    # Clean up blank lines from removals
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()

    result.cleaned = cleaned

    # ---- map diagrams to slide indices ----------------------------------
    # split the original text to find which |||-segment each diagram is in
    segments = text.split(SPLIT_MARKER)
    slide_idx_by_diagram: list[int] = []
    for dm in diag_matches:
        pos = dm.start()
        # find which segment this falls into
        char_count = 0
        for si, seg in enumerate(segments):
            char_count += len(seg)
            if pos < char_count:
                slide_idx_by_diagram.append(si)
                break

    # ---- resolve headings and params for diagrams -----------------------
    for i, dm in enumerate(diag_matches):
        si = slide_idx_by_diagram[i] if i < len(slide_idx_by_diagram) else 0
        seg = segments[si] if si < len(segments) else ""
        heading = ""
        seg_headings = list(RE_HEADING.finditer(seg))
        if seg_headings:
            heading = seg_headings[-1].group(1).strip()
        if not heading:
            # fallback: standalone line before the diagram marker
            diag_pos = seg.find("[[")
            pre = seg[:diag_pos].strip() if diag_pos >= 0 else seg.strip()
            pre_lines = [l.strip() for l in pre.split("\n") if l.strip()]
            for line in reversed(pre_lines):
                if not line.startswith("[") and not line.startswith("!") and len(line) < 80:
                    heading = line
                    break
        si = slide_idx_by_diagram[i] if i < len(slide_idx_by_diagram) else 0
        raw = dm.group(2).strip() if dm.group(2) else None
        if raw is not None:
            parts = [p.strip() for p in raw.split(";")]
            if "=" in parts[0]:
                d_cfg: dict = {}
                for part in parts:
                    if "=" in part:
                        k, v = part.split("=", 1)
                        d_cfg[k.strip().lower()] = v.strip()
                cfg_type = dm.group(1).lower()
                if cfg_type == "flowchart":
                    steps = [s.strip() for s in d_cfg.get("steps", raw).split(",")]
                    result.diagram_slides[si] = {
                        "type": "flowchart",
                        "steps": steps,
                        "heading": d_cfg.get("heading", heading),
                    }
            else:
                cfg_type = dm.group(1).lower()
                if cfg_type == "flowchart":
                    steps = [s.strip() for s in raw.split(",")]
                    result.diagram_slides[si] = {
                        "type": "flowchart",
                        "steps": steps,
                        "heading": heading,
                    }
        else:
            cfg_type = dm.group(1).lower()
            if cfg_type == "flowchart":
                seg_text = segments[si] if si < len(segments) else ""
                inferred = _infer_flowchart_steps(seg_text)
                result.diagram_slides[si] = {
                    "type": "flowchart",
                    "steps": inferred,
                    "heading": heading,
                }

    return result


def _infer_flowchart_steps(text: str) -> list[str]:
    """Extract flowchart steps from contextual text (no explicit params)."""
    # Look for colon-introduced lists: "loop: explore, plan, code, commit"
    m = re.search(r'(?:loop|steps?|process|workflow|phases?)[:\s]+(.+)',
                  text, re.IGNORECASE)
    if m:
        raw = m.group(1)
        raw = re.split(r'(?<=[a-z)])[.!?]', raw)[0]  # stop at sentence boundary
        parts = [p.strip().rstrip(".") for p in raw.split(",")]
        parts = [p for p in parts if p and len(p) < 30]
        if len(parts) >= 2:
            return parts

    # Fallback: any comma-separated short phrases on a single line
    for line in text.split("\n"):
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 3:
            cleaned = [re.sub(r"^[-\d.\s]+", "", p).strip().rstrip(".") for p in parts]
            cleaned = [p for p in cleaned if p and len(p) < 30]
            if len(cleaned) >= 2:
                return cleaned

    # Look for "from X to Y" pattern
    m = re.search(r'from\s+"([^"]+)"\s+to\s+"([^"]+)"', text)
    if m:
        return [m.group(1), m.group(2)]

    return ["Define", "Explore", "Build", "Review"]


# ---------------------------------------------------------------------------
# Text cleaning
# ---------------------------------------------------------------------------

def _fix_mojibake(text: str) -> str:
    try:
        fixed = text.encode("cp1252").decode("utf-8")
        if fixed != text:
            return fixed
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    return text


def _clean_text(text: str) -> str:
    text = _fix_mojibake(text)
    text = EM_DASH.sub(" - ", text)
    return text


# ---------------------------------------------------------------------------
# Slide splitting
# ---------------------------------------------------------------------------

def _distribute_body(paragraphs: list[str]) -> list[str]:
    total_chars = sum(len(p) for p in paragraphs)
    if total_chars < 120 or len(paragraphs) <= 1:
        return ["\n\n".join(paragraphs)]

    n = max(1, min(3, round(total_chars / 250)))

    groups: list[list[str]] = [[] for _ in range(n)]
    for i, p in enumerate(paragraphs):
        groups[i % n].append(p)

    result = ["\n\n".join(g) for g in groups if g]
    return result if result else ["\n\n".join(paragraphs)]


def split_into_slides(text: str, mode: str = "detect") -> list[dict]:
    """Split post text into slides.

    *mode*:
      - ``"detect"`` (default): use ``|||`` markers if present, else auto
      - ``"auto"``: force content-aware distribution, ignore markers
      - ``"manual"``: require ``|||`` markers, error if missing
    """
    has_markers = SPLIT_MARKER in text

    if mode == "manual" or (mode == "detect" and has_markers):
        if mode == "manual" and not has_markers:
            raise ValueError(
                "Manual split mode requires `|||` markers in the text."
            )
        parts = [p.strip() for p in text.split(SPLIT_MARKER) if p.strip()]
        slides = []
        for i, part in enumerate(parts):
            lines = part.split("\n", 1)
            title = re.sub(RE_STRIP_HEADING, "", lines[0].strip()) if lines else ""
            slides.append({
                "title": title,
                "body": lines[1].strip() if len(lines) > 1 else "",
                "is_cta": i == len(parts) - 1 and len(parts) > 1,
            })
        return slides

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        return [{"title": "", "body": text.strip(), "is_cta": False}]

    title_para = paragraphs[0]
    remaining = paragraphs[1:]

    cta_para = None
    if remaining and CTA_PATTERNS.search(remaining[-1]):
        cta_para = remaining.pop()

    if not remaining:
        return [{"title": title_para, "body": "", "is_cta": False}]

    body_groups = _distribute_body(remaining)

    slides = [{"title": title_para, "body": "", "is_cta": False}]
    for group in body_groups:
        slides.append({"title": "", "body": group, "is_cta": False})
    if cta_para:
        slides.append({"title": "", "body": cta_para, "is_cta": True})

    return slides


# ---------------------------------------------------------------------------
# Preview
# ---------------------------------------------------------------------------

def preview_slides(text: str, mode: str = "detect") -> list[dict]:
    return split_into_slides(text, mode=mode)


# ---------------------------------------------------------------------------
# Background decoration
# ---------------------------------------------------------------------------

def _draw_background(
    draw: ImageDraw.ImageDraw,
    theme: dict,
    slide: dict,
    slide_num: int,
    total: int,
    decorate: bool = False,
):
    accent = theme["accent"]
    accent2 = theme["accent2"]

    stripe_w = 14
    draw.rectangle([0, 0, stripe_w, CANVAS_H], fill=accent)

    bar_y = CANVAS_H - 4
    draw.rectangle([stripe_w + 40, bar_y, CANVAS_W - 40, bar_y + 2], fill=accent2)

    sfont = _load_font(SMALL_FONT_SIZE)
    num_text = f"{slide_num} / {total}"
    draw.text((CANVAS_W - 120, CANVAS_H - 50), num_text, fill=theme["num"], font=sfont)

    if not decorate:
        return

    if slide["is_cta"]:
        emoji_char = "💬"
        for pattern, e in CTA_EMOJIS.items():
            if pattern in slide["body"].lower():
                emoji_char = e
                break
        _draw_emoji_watermark(draw, emoji_char, theme)
    elif slide["title"] and slide_num == 1:
        idx = len(slide["title"]) % len(TITLE_EMOJIS)
        _draw_emoji_watermark(draw, TITLE_EMOJIS[idx], theme)
    elif slide_num % 2 == 0 and total > 1:
        _draw_emoji_watermark(draw, "•", theme, dot_mode=True)


def _draw_emoji_watermark(
    draw: ImageDraw.ImageDraw,
    char: str,
    theme: dict,
    dot_mode: bool = False,
):
    if dot_mode:
        for x in range(3, 6):
            for y in range(2, 5):
                cx = x * 200 + 100
                cy = y * 200 + 50
                draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=theme["accent2"])
        return

    efont = _load_emoji_font(EMOJI_FONT_SIZE)
    bbox = draw.textbbox((0, 0), char, font=efont)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = CANVAS_W - w - 60
    y = CANVAS_H - h - 100

    overlay = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    odraw.text((x, y), char, font=efont, fill=(100, 100, 100, 30))
    draw._image.paste(overlay, (0, 0), overlay)


# ---------------------------------------------------------------------------
# Logo overlay
# ---------------------------------------------------------------------------

LOGO_SIZES = {
    "small": (120, 60),
    "medium": (180, 90),
    "large": (300, 150),
}


def _draw_claude_logo(
    img: Image.Image,
    theme: dict,
    image_path: Optional[str] = None,
    position: str = "top-right",
    logo_size: str = "medium",
):
    if image_path and os.path.isfile(image_path):
        try:
            logo = Image.open(image_path).convert("RGBA")
            max_w, max_h = LOGO_SIZES.get(logo_size, (180, 90))
            lw, lh = logo.size
            scale = min(max_w / lw, max_h / lh, 1)
            nw, nh = int(lw * scale), int(lh * scale)
            logo = logo.resize((nw, nh), Image.LANCZOS)

            if position == "center-bottom":
                x = (CANVAS_W - nw) // 2
                y = CANVAS_H - nh - 60
            else:
                x = CANVAS_W - nw - 40
                y = 40

            img.paste(logo, (x, y), logo)
            return
        except Exception:
            pass

    draw = ImageDraw.Draw(img)
    font = _load_font(26)
    text = "CLAUDE"

    tw = draw.textbbox((0, 0), text, font=font)
    badge_w = tw[2] + 36
    badge_h = 44

    x = CANVAS_W - badge_w - 40
    y = CANVAS_H - badge_h - 40

    draw.rounded_rectangle(
        [x, y, x + badge_w, y + badge_h],
        radius=22, fill=theme["accent"], outline=theme["accent"], width=0,
    )
    tx = x + (badge_w - tw[2]) / 2
    ty = y + (badge_h - tw[3]) / 2 - tw[1]
    draw.text((tx, ty), text, fill=theme["bg"], font=font)


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def _render_accent_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    x: int,
    y: int,
    text_color: str,
    accent_color: str,
    max_width: int,
) -> int:
    """Draw text with ``[accent]`` / ``[/accent]`` spans.

    Returns the y-position after the last drawn line.
    """
    # Split text into segments: (text, use_accent_color)
    segments: list[tuple[str, bool]] = []
    current: list[str] = []
    in_accent = False
    i = 0
    while i < len(text):
        if text[i : i + 8] == "[accent]":
            if current:
                segments.append(("".join(current), in_accent))
                current = []
            in_accent = True
            i += 8
        elif text[i : i + 9] == "[/accent]":
            if current:
                segments.append(("".join(current), in_accent))
                current = []
            in_accent = False
            i += 9
        else:
            current.append(text[i])
            i += 1
    if current:
        segments.append(("".join(current), in_accent))

    # Wrap each segment and draw
    line_y = y
    for seg_text, use_accent in segments:
        color = accent_color if use_accent else text_color
        words = seg_text.split()
        line: list[str] = []

        for word in words:
            test = " ".join(line + [word])
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] <= max_width:
                line.append(word)
            else:
                if line:
                    draw.text((x, line_y), " ".join(line), fill=color, font=font)
                    line_y += font.getbbox("Ag")[3] + 6
                line = [word]

        if line:
            draw.text((x, line_y), " ".join(line), fill=color, font=font)
            line_y += font.getbbox("Ag")[3] + 6

    return line_y


def render_slide(
    slide: dict,
    slide_num: int,
    total: int,
    theme_name: str = "minimal",
    has_accent: bool = False,
    decorate: bool = False,
    diagram_image: Optional[Image.Image] = None,
) -> Image.Image:
    theme = THEMES.get(theme_name, THEMES["minimal"])
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), theme["bg"])
    draw = ImageDraw.Draw(img)

    title_font = _load_font(TITLE_FONT_SIZE)
    body_font = _load_font(BODY_FONT_SIZE)
    cta_font = _load_font(BODY_FONT_SIZE)

    _draw_background(draw, theme, slide, slide_num, total, decorate=decorate)

    text_w = CANVAS_W - 120
    margin_left = 60
    body_top = 100
    y = body_top

    if slide["title"]:
        text = _clean_text(slide["title"])
        if has_accent and ACCENT_TAG.search(text):
            y = _render_accent_text(
                draw, text, title_font, margin_left, y,
                theme["text"], theme["accent"], text_w,
            )
        else:
            lines = _wrap_text(draw, text, title_font, text_w)
            for line in lines:
                draw.text((margin_left, y), line, fill=theme["text"], font=title_font)
                y += title_font.getbbox("Ag")[3] + 6
        y += 20

        line_width = min(len(slide["title"]) * 14, 200)
        draw.rectangle([margin_left, y, margin_left + line_width, y + 4], fill=theme["accent"])
        y += 32

    if slide["body"]:
        text = _clean_text(slide["body"])
        font = cta_font if slide["is_cta"] else body_font
        color = theme["accent"] if slide["is_cta"] else theme["text"]

        if has_accent and not slide["is_cta"] and ACCENT_TAG.search(text):
            y = _render_accent_text(
                draw, text, font, margin_left, y,
                theme["text"], theme["accent"], text_w,
            )
        else:
            lines = _wrap_text(draw, text, font, text_w)
            for line in lines:
                draw.text((margin_left, y), line, fill=color, font=font)
                y += font.getbbox("Ag")[3] + 8

    if diagram_image:
        diagram_gap = 20
        available_h = CANVAS_H - y - diagram_gap - 80
        if available_h > 60:
            diag_w = CANVAS_W - 120
            diag = diagram_image.resize((diag_w, int(diag_w * diagram_image.height / diagram_image.width)), Image.LANCZOS)
            if diag.height > available_h:
                diag = diagram_image.resize((diag_w, available_h), Image.LANCZOS)
            diag_y = y + diagram_gap
            diag_x = 60
            img.paste(diag, (diag_x, diag_y), diag if diag.mode == "RGBA" else None)

    return img


def _wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    max_width: int,
) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""

    for word in words:
        test = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines if lines else [text]


# ---------------------------------------------------------------------------
# PDF compilation
# ---------------------------------------------------------------------------

def build_pdf(images: list[Image.Image], output_path: str) -> str:
    import img2pdf

    temp_paths: list[str] = []
    try:
        for img in images:
            fd, path = tempfile.mkstemp(suffix=".png")
            os.close(fd)
            img.save(path, "PNG")
            temp_paths.append(path)

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(img2pdf.convert(temp_paths))

        return output_path
    finally:
        for path in temp_paths:
            try:
                os.remove(path)
            except OSError:
                pass


# ---------------------------------------------------------------------------
# Preview
# ---------------------------------------------------------------------------

def preview_slide(
    slide: dict,
    slide_num: int,
    total: int,
    *,
    theme_name: str = "minimal",
    output_dir: str = "drafts/carousel_preview",
    has_accent: bool = False,
) -> str:
    """Render a single slide as a preview PNG.

    Returns the absolute path to the saved image.
    """
    img = render_slide(
        slide, slide_num, total, theme_name=theme_name, has_accent=has_accent
    )
    os.makedirs(output_dir, exist_ok=True)
    slug = (
        re.sub(
            r"[^a-zA-Z0-9]+",
            "-",
            (slide.get("title") or slide.get("body", ""))[:30],
        )
        .strip("-")
        .lower()
    )
    path = os.path.abspath(
        os.path.join(output_dir, f"slide-{slide_num}-{slug}.png")
    )
    img.save(path, "PNG")
    return path


def preview_themes(
    text: str,
    *,
    slide_index: int = 0,
    output_dir: str = "drafts/carousel_preview",
) -> dict[str, str]:
    """Render slide *slide_index* (0-based) in every available theme.

    Returns a dict mapping theme_name -> absolute file path.
    """
    slides = split_into_slides(text)
    if not slides or slide_index >= len(slides):
        raise ValueError(
            f"Slide index {slide_index} out of range (total {len(slides)} slides)"
        )

    parsed = parse_draft(text)
    slide = slides[slide_index]
    total = len(slides)

    os.makedirs(output_dir, exist_ok=True)
    slug = (
        re.sub(
            r"[^a-zA-Z0-9]+",
            "-",
            (slide.get("title") or slide.get("body", ""))[:30],
        )
        .strip("-")
        .lower()
    )

    results: dict[str, str] = {}
    for theme_name in THEMES:
        img = render_slide(
            slide,
            slide_index + 1,
            total,
            theme_name=theme_name,
            has_accent=parsed.has_accent,
        )
        path = os.path.abspath(
            os.path.join(output_dir, f"{theme_name}-slide-{slide_index + 1}-{slug}.png")
        )
        img.save(path, "PNG")
        results[theme_name] = path

    return results


def _check_overflow(text: str, font_size: int, max_width: int, max_height: int) -> Optional[str]:
    """Return a warning string if *text* likely overflows the canvas, or None."""
    font = _load_font(font_size)
    draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    lines = _wrap_text(draw, text, font, max_width)
    line_h = font.getbbox("Ag")[3] + 8
    total_h = len(lines) * line_h
    if total_h > max_height:
        excess = total_h - max_height
        pct = int(excess / max_height * 100)
        return f"~{pct}% overflow ({len(lines)} lines, {len(text)} chars)"
    return None


def _versioned_path(output_dir: str, base_name: str, ext: str) -> str:
    """Return a path that won't overwrite an existing file.

    Appends ``-v1``, ``-v2`` … to *base_name* until the path is free.
    """
    os.makedirs(output_dir, exist_ok=True)
    candidate = os.path.join(output_dir, f"{base_name}{ext}")
    if not os.path.isfile(candidate):
        return os.path.abspath(candidate)

    v = 1
    while True:
        candidate = os.path.join(output_dir, f"{base_name}-v{v}{ext}")
        if not os.path.isfile(candidate):
            return os.path.abspath(candidate)
        v += 1


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_carousel(
    post_text: str,
    *,
    renderer: str = "pillow",
    output_dir: str = "drafts/carousel_output",
    title: Optional[str] = None,
    theme: str = "ink-yellow",
    draft: bool = False,
    split_mode: str = "detect",
    logo: bool | str = False,
    logo_position: str = "top-right",
    diagram_slides: Optional[dict[int, dict]] = None,
    preview_only: bool = False,
    slide_filter: Optional[list[int]] = None,
) -> str:
    """Full pipeline: parse -> split -> render -> PDF (or preview).

    Args:
        post_text: The LinkedIn post text (may contain ``[claude logo]``,
            ``[[flowchart: ...]]``, ``[accent]`` instructions).
        renderer: ``"pillow"`` (default, existing Pillow+img2pdf pipeline) or
            ``"playwright"`` (HTML+Chromium, vector text, CSS themes).
        output_dir: Directory to save the PDF (or preview PNGs).
        title: Optional filename stem; auto-derived if omitted.
        theme: One of ``THEMES`` keys (default: ink-yellow).
        draft: Save to ``drafts/draft-carousels/`` instead of *output_dir*.
        split_mode: ``"detect"`` (auto/manual based on content),
            ``"auto`` (ignore markers), ``"manual"`` (require markers).
        logo: ``True`` for drawn badge, or a path to a logo image.
        logo_position: Where to place logo (``"top-right"``, ``"center-bottom"``).
        diagram_slides: Map of slide index -> diagram config (merged with
            any parsed from draft text).
        preview_only: When ``True``, save each slide as a PNG instead of
            compiling a PDF. Returns the preview directory path.
        slide_filter: 0-based indices of slides to include; ``None`` means all.

    Returns:
        Absolute path to the generated PDF file (or preview directory when
        *preview_only* is ``True``).
    """
    if theme not in THEMES:
        available = ", ".join(THEMES)
        raise ValueError(f"Unknown theme '{theme}'. Available: {available}")

    if draft:
        output_dir = "drafts/draft-carousels"

    # parse draft instructions
    parsed = parse_draft(post_text)
    post_text = parsed.cleaned

    # merge diagram_slides from draft parsing with explicit param
    merged_diagrams: dict[int, dict] = {}
    if parsed.diagram_slides:
        merged_diagrams.update(parsed.diagram_slides)
    if diagram_slides:
        merged_diagrams.update(diagram_slides)

    # auto-resolve logo path if not provided explicitly
    logo_file: Optional[str] = None
    if logo is True:
        logo_file = _pick_logo_path()
    elif isinstance(logo, str):
        logo_file = logo
    elif parsed.logo_position:
        logo_file = _pick_logo_path(name=parsed.logo_name)
        logo_position = parsed.logo_position

    slides = split_into_slides(post_text, mode=split_mode)
    if not slides:
        msg = "Cannot generate carousel: no content to split."
        raise ValueError(msg)

    # apply slide_filter
    if slide_filter is not None:
        slides = [s for i, s in enumerate(slides) if i in slide_filter]
        if not slides:
            raise ValueError("slide_filter produced an empty slide list.")

    if not title:
        first_line = slides[0]["title"] or slides[0]["body"]
        title = re.sub(r"[^a-zA-Z0-9]+", "-", first_line.strip())[:50].strip("-")

    if draft:
        prefix = "draft-"
    else:
        prefix = ""
    base_name = f"{prefix}{title.lower()}"

    # ---- Playwright renderer path ----------------------------------------
    if renderer == "playwright":
        diagram_images: dict[int, Image.Image] = {}
        for i, s in enumerate(slides):
            if merged_diagrams and i in merged_diagrams:
                cfg = merged_diagrams[i]
                dt = cfg.get("type", "")
                if dt == "flowchart":
                    from lib.excalidraw import render_flowchart
                    diagram_images[i] = render_flowchart(
                        cfg["steps"], THEMES[theme],
                        heading=cfg.get("heading", ""),
                    )
                elif dt == "comparison":
                    from lib.excalidraw import render_comparison
                    diagram_images[i] = render_comparison(
                        cfg["left_title"], cfg.get("left_items", []),
                        cfg["right_title"], cfg.get("right_items", []),
                        THEMES[theme],
                    )
                elif dt == "framework":
                    from lib.excalidraw import render_framework
                    diagram_images[i] = render_framework(cfg.get("items", []), THEMES[theme])

        output_path = _versioned_path(output_dir, base_name, ".pdf")

        from lib.html_renderer import render_carousel as playwright_render
        return playwright_render(
            slides,
            theme_name=theme,
            decorate=parsed.decorate,
            diagram_images=diagram_images or None,
            logo_file=logo_file,
            logo_position=logo_position,
            logo_size=parsed.logo_size,
            output_path=output_path,
        )

    # ---- Pillow renderer path --------------------------------------------
    images: list[Image.Image] = []
    overflow_warnings: list[str] = []
    for i, s in enumerate(slides):
        diagram_img = None
        if merged_diagrams and i in merged_diagrams:
            cfg = merged_diagrams[i]
            dt = cfg.get("type", "")
            if dt == "flowchart":
                from lib.excalidraw import render_flowchart
                diagram_img = render_flowchart(
                    cfg["steps"], THEMES[theme],
                    heading=cfg.get("heading", ""),
                )
            elif dt == "comparison":
                from lib.excalidraw import render_comparison
                diagram_img = render_comparison(
                    cfg["left_title"], cfg.get("left_items", []),
                    cfg["right_title"], cfg.get("right_items", []),
                    THEMES[theme],
                )
            elif dt == "framework":
                from lib.excalidraw import render_framework
                diagram_img = render_framework(cfg.get("items", []), THEMES[theme])
        images.append(
            render_slide(s, i + 1, len(slides),
                         theme_name=theme, has_accent=parsed.has_accent,
                         decorate=parsed.decorate,
                         diagram_image=diagram_img)
        )
        body = s.get("body", "")
        if body:
            text_w = CANVAS_W - 120 if not diagram_img else int(CANVAS_W * 0.55) - 60
            warn = _check_overflow(body, BODY_FONT_SIZE, text_w, CANVAS_H - 180)
            if warn:
                slug = (s.get("title") or body[:30]).strip()[:40]
                overflow_warnings.append(f"  Slide {i + 1} ({slug}): {warn}")

    if logo_file and images and not preview_only:
        _draw_claude_logo(images[0], THEMES[theme], image_path=logo_file, position=logo_position, logo_size=parsed.logo_size)

    # ---- preview mode: save PNGs, return dir ----------------------------
    if preview_only:
        os.makedirs(output_dir, exist_ok=True)
        saved: list[str] = []
        for i, img in enumerate(images):
            slug = (
                re.sub(
                    r"[^a-zA-Z0-9]+",
                    "-",
                    (slides[i].get("title") or slides[i].get("body", ""))[:30],
                )
                .strip("-")
                .lower()
            )
            path = os.path.join(output_dir, f"{i + 1:02d}-{slug}.png")
            img.save(path, "PNG")
            saved.append(os.path.abspath(path))

        summary = (
            f"Preview: {len(saved)} slides -> {output_dir}/\n"
            + "\n".join(f"  {p}" for p in saved)
        )
        if overflow_warnings:
            summary += "\nOverflow warnings:\n" + "\n".join(overflow_warnings)
        print(summary)
        return os.path.abspath(output_dir)

    # ---- PDF mode -------------------------------------------------------
    output_path = _versioned_path(output_dir, base_name, ".pdf")

    build_pdf(images, output_path)

    if overflow_warnings:
        print(f"PDF generated: {output_path}")
        print("Overflow warnings:\n" + "\n".join(overflow_warnings))

    return output_path
