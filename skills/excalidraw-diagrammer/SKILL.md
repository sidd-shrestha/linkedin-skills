---
name: excalidraw-diagrammer
description: |
  Generate Excalidraw diagram scenes (flowcharts, comparisons, frameworks)
  for LinkedIn carousel slides. Creates editable `.excalidraw` JSON files
  that open in excalidraw.com or the desktop app, plus renders diagram
  slides directly into carousel PDFs. Triggers on "diagram this",
  "flowchart", "make a comparison slide", "visualize the framework".
  Not for plain text posts (use linkedin-post-writer).
---

# Excalidraw Diagrammer

Turn text-heavy carousel slides into visual diagrams. Each diagram is
generated as both an editable `.excalidraw` JSON file and a Pillow-rendered
image for PDF inclusion.

## When to use

- User says "diagram the agentic loop", "make a flowchart", "turn slide 3 into a diagram"
- A post has a sequential process, before/after comparison, or multi-pillar framework
- User wants visual variety in their carousel (mix of text and diagram slides)

## Diagram types

| Type | Layout | Best for |
|---|---|---|
| `flowchart` | Horizontal boxes + arrows | Processes, steps, loops |
| `comparison` | Two columns side-by-side | Before/after, pro/con, then/now |
| `framework` | Multiple labelled nodes | Pillars, principles, categories |

## Flow

1. **Identify the content.** Extract the relevant text from the post or from
   the user's description. Ask clarifying questions if the diagram type is
   ambiguous.

2. **Generate the Excalidraw scene.** Call the relevant builder:
   - `lib.excalidraw.build_flowchart(steps, title)`
   - `lib.excalidraw.build_comparison(left_title, left_items, right_title, right_items, heading)`
   - `lib.excalidraw.build_framework(items, title)`

   Save to `draft-carousels/diagrams/<slug>.excalidraw`.

3. **Add to carousel (optional).** If a carousel is being built, pass the
   diagram as a `diagram_slides` entry to `generate_carousel()`:
   ```python
   generate_carousel(text, diagram_slides={
       1: {"type": "flowchart", "steps": ["Explore", "Plan", "Code", "Commit"]},
   })
   ```

4. **Tell the user.** Mention both files:
   - "Diagram saved to `draft-carousels/diagrams/<slug>.excalidraw` — open in excalidraw.com to tweak"
   - "Added to carousel as slide N"

## Examples

### Flowchart
> User: diagram the agentic loop
>
> Flowchart: Explore → Plan → Code → Commit, 4 boxes with arrows

### Comparison
> User: make a comparison slide for my transition
>
| Before | After |
|---|---|
| QA Automation | AI Architecture |
| Tell it HOW | Tell it WHAT |
| Manual scripts | Agentic loops |

### Framework
> User: visualize the 3 pillars of AI readiness
>
| People | Process | Platform |
|---|---|---|
| Training | Workflow | Tools |
| Culture | Governance | Infrastructure |

## Files

- `lib/excalidraw.py` — scene builders, Pillow renderers, save helpers
- `draft-carousels/diagrams/` — saved `.excalidraw` JSON files

## Related skills

- `linkedin-post-writer` — generates the post that the diagram illustrates
- `linkedin-humanizer` — scrub AI tells from the final post
