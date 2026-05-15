# Carousel Generator — Learning Journey

## Why I built it

LinkedIn Document Carousels (multi-page PDFs) get **1.7-2.3x more reach** than text-only posts. But creating them meant switching to Canva, Figma, or Google Slides — breaking the draft→approve→publish flow that the `linkedin-skills` bundle is built around.

I wanted a **zero-API, fully local** carousel generator that takes the same draft text the post-writer skill produces and turns it into a print-ready PDF in one command.

## Architecture decisions

| Decision | Choice | Why |
|---|---|---|
| Rendering engine | **Pillow** | Zero browser dependency. No Playwright, no headless Chrome. Ships with `pip install Pillow img2pdf`. |
| PDF assembly | **img2pdf** | Lossless PNG→PDF. No re-encoding artifacts. Handles multi-page. |
| Canvas size | **1080×1080** | LinkedIn renders Document Carousels at 1:1. 1080px is the recommended resolution. |
| Fonts | **System fonts** (Segoe UI, Arial, DejaVu Sans) | No bundling. Falls back gracefully across Win/Mac/Linux. |
| Emoji rendering | **Segoe UI Emoji** on Windows | Native Windows emoji. Other platforms fall back to text. |
| Themes | **5 built-in** (minimal, dark, ink-yellow, neon, bold) | Covers light/dark/colorful. Users can add more via `THEMES` dict. |
| Draft markers | `[accent]`, `[claude logo]`, `[[flowchart: ...]]`, `|||` | Zero-config. The same draft works as a post or a carousel. |

## How the pipeline works

```
draft text
  → parse_draft()       — strip markers, extract metadata
  → split_into_slides() — split by ||| or auto-distribute
  → render_slide()      — Pillow draw per slide
  → build_pdf()         — img2pdf assemble
  → PDF file
```

### Slide splitting

Two modes:

- **Manual** (`|||` markers) — full control. Each `|||`-separated block is one slide. The first line becomes the title.
- **Auto** — distributes paragraphs across slides, capping at ~250 chars per slide. Detects CTA paragraphs and puts them on the last slide.

### Draft markers

- `[accent]text[/accent]` — highlight spans in theme accent color
- `[claude logo]` / `[claude logo bottom]` — overlay Claude badge
- `[[flowchart: step1, step2, ...]]` — render a Pillow flowchart diagram
- `|||` — slide separator

## Enhancement: Interactive Preview

The original generator was a one-shot pipeline — text in, PDF out. If the layout was wrong, you had to regenerate blind.

### What I added

1. **`preview_only=True`** — renders each slide as a PNG into a directory. You see every slide before committing to a PDF.
2. **`preview_themes()`** — renders slide 1 in all 5 themes side-by-side so you can pick the best look.
3. **`slide_filter=[0, 2, 4]`** — select only specific slides for the final output.
4. **Overflow warnings** — alerts when body text is too long for the 1080×1080 canvas, with estimated overflow %.
5. **`--preview` and `--preview-themes` CLI flags** — direct access from `testing/gen_carousel.py`.

### Usage

```bash
# Preview slides as PNGs
python testing/gen_carousel.py --preview --draft my-draft.txt

# Compare themes
python testing/gen_carousel.py --preview-themes --draft my-draft.txt

# Generate final PDF
python testing/gen_carousel.py --theme bold --draft my-draft.txt
```

## Key lessons learned

### Font rendering is the hardest part

- Pillow's `textbbox()` and `getbbox()` return different values. `textbbox` is correct for wrapping; `getbbox` is correct for line height.
- Emoji fonts (Segoe UI Emoji) have different metrics than text fonts. You need separate font objects and a fallback chain.
- No cross-platform emoji solution exists for Pillow. On macOS you get tofu boxes; on Linux you need `noto-fonts-emoji`. We document the constraint rather than fighting it.

### Slide splitting heuristics are brittle

Auto-split by character count works for 80% of cases. The other 20% — short dense text, very long paragraphs, mixed lists — needs manual `|||` markers. Making the heuristic smarter (semantic chunking, bullet detection) is the next frontier.

### img2pdf is fast but limited

It converts images to PDF without re-encoding. Great for quality, but you can't embed hyperlinks, vector text, or metadata. For a LinkedIn carousel (which is just a displayed PDF) this is fine. For a downloadable resource, you'd want a proper PDF library.

### The diagram integration pattern works well

`[[flowchart: ...]]` markers in draft text → parsed by `parse_draft()` → rendered by `lib/excalidraw.py` → inserted at the right slide position. No config files, no external tools.

## What's next

- **Image embedding** — `[[image: path_or_url]]` to embed screenshots, photos, or diagrams into slides
- **Custom themes** — user-defined color schemes via a JSON file
- **More layout templates** — split-screen, quote cards, stat blocks, numbered lists
- **HTML/PPTX export** — for users who need editable formats
- **Slide notes** — a speaker notes field per slide, stripped from the PDF
- **Web UI** — drag-and-drop preview in the browser (biggest lift, but would eliminate the CLI barrier)
