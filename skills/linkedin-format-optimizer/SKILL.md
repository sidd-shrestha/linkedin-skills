---
name: linkedin-format-optimizer
description: Suggest the best format for a LinkedIn post draft or topic (text, carousel, poll, video, image) using a data-driven decision matrix. Two modes: --advise recommends a format before writing based on content type, goal, and structural signals; --audit verifies whether a completed draft matches its chosen format and suggests conversions. Built on 2026 algorithm heuristics. Not for creating the post itself (use linkedin-post-writer).
---

# LinkedIn Format Optimizer

Analyze any LinkedIn post draft or topic and recommend the optimal format. Uses the content-type x goal decision matrix from `references/format-matrix.md`, backed by 2026 reach and engagement data from `../../references/algorithm-heuristics.md`.

## When to use

- User asks "what format should I use for this post?"
- User has a topic and wants format options before writing
- User shares a draft and asks "should this be a carousel?"
- User has a post that underperformed and wants a format post-mortem
- User is planning content and wants format variety guidance
- User has a draft with `|||` markers and wants to verify they should be a carousel

## Modes

The skill operates in two modes:

### `--advise` (default)
Pre-write format advisor. Given a topic, idea, or partial draft, recommends the best format before you write.

### `--audit`
Post-write format auditor. Given a completed draft + chosen format (or auto-detected from `|||` markers or diagram references), verifies the format fits and suggests conversions if it doesn't.

## Format decision matrix

Refer to `references/format-matrix.md` for the full lookup table. The core mapping:

| Content type | Best format | Reach multiplier | Save rate |
|---|---|---|---|
| Educational / framework | Carousel | 1.7-2.3x | Highest |
| How-to / tutorial | Carousel | 1.7-2.3x | High |
| Personal story / narrative | Text-only | 1.0-1.3x | Moderate |
| Opinion / hot take | Text-only | 1.0-1.3x | Low |
| Data breakdown / receipts | Carousel | 1.7-2.3x | Highest |
| Contrarian / sacred cow | Text-only | 1.0-1.3x | Low |
| Community question | Poll | 1.1x (+206% reach) | N/A |
| Quick tip | Text + image | 1.0-1.3x | Low |
| Lead magnet / offer | Carousel | 1.7-2.3x | Highest |
| Announcement / news | Text + image | 1.0-1.3x | Low |

Goal overrides the default: "max reach", "max comments", "authority/saves", "lead gen", "audience research" each shift the recommendation.

Structural signals also influence the recommendation: `|||` markers, `[[flowchart:...]]`, diagram references, list-heavy content, char count, and hook formula detection.

## Steps (`--advise` mode)

1. **Gather inputs.** Accept the post topic, partial draft, or idea. Ask for optional: primary goal (reach / comments / authority / leads / research), target audience, any preferred formats the user is considering.
2. **Classify the content type.** Analyze the topic or draft against the content type taxonomy in `references/format-matrix.md`. Look for structural signals (char count, lists, `|||` markers, diagram references, numbers, named entities, hook formula patterns).
3. **Apply the decision matrix.** Cross-reference content type x goal x structural signals to produce a ranked format list. Primary recommendation + 1-2 alternatives.
4. **Build the recommendation card.**
   - Primary format
   - Why (reach multiplier or engagement rate from algorithm-heuristics.md)
   - Alternative formats with trade-offs
   - If the user shared a draft: specific feedback on how it maps to each format
   - Tips for executing in the recommended format (slide count for carousel, hook structure for text, question framing for poll)
5. **Offer handoff.** "Want me to create this as a [recommended format]?" If yes, route to:
   - `linkedin-post-writer` for carousel or text
   - `linkedin-post-writer` with `|||` markers for carousel
   - Instruct user on native poll / video creation (no API support for these)
6. **On approval.** If the user accepts the format and continues writing, suggest they run `linkedin-humanizer --mode audit` on the final draft.

## Steps (`--audit` mode)

1. **Gather inputs.** Accept a completed post draft + optional chosen format. Auto-detect format intent from `|||` markers (carousel), `[[flowchart:...]]` / `[[framework:...]]` (carousel), poll-like phrasing (poll), or explicit user statement.
2. **Classify the content type.** Same analysis as `--advise`.
3. **Compare chosen format vs recommended format.**
   - **Optimal.** Chosen format matches the recommendation. Report: "Your post is in the right format. Here's why it works."
   - **Suboptimal but viable.** Chosen format differs but isn't harmful. Report: "This works as [chosen], but [recommended] would perform 2x better for reach because..."
   - **Mismatch.** Chosen format actively hurts performance. Report: "This post is in the wrong format. [Recommended] would reach 2-3x more people for this content type. Here's what to change."
4. **Include data.** Cite reach multipliers, engagement benchmarks, and signal weights from `../../references/algorithm-heuristics.md`.
5. **Offer conversion.** "Want me to convert this to [recommended format]?" If yes:
   - Text to carousel: Add `|||` markers and call `from lib.carousel import generate_carousel` to render the PDF. Tell the user: "Carousel saved to drafts/carousel_output/ -- upload it manually to LinkedIn as a Document Carousel."
   - Carousel to text: Merge slides into a single text draft with line breaks and a strong hook.
   - Any format to poll: Extract the question and offer 3-5 answer options.
6. **On approval.** After conversion, suggest running `linkedin-humanizer --mode audit` on the final output.

## Hard rules

Global voice rules: see root `SKILL.md` section Voice rules. Additional skill-specific rules:

- Always cite at least one data point from `../../references/algorithm-heuristics.md` in every format recommendation (reach multiplier, engagement rate, or signal weight).
- Never recommend a format solely because it has the highest reach multiplier. Consider user effort, the user's content creation track record, and whether they can sustain the format.
- When content type is ambiguous (e.g., a story that also contains data), present the top 2 formats with clear trade-offs and let the user decide.
- In `--audit` mode, always check whether the post already contains `|||` markers before recommending carousel conversion -- if it does, the user already made that choice; validate it rather than suggesting a change.
- Save recommendations are more valuable than reach recommendations. A format that generates saves compounds authority over time.

## Anti-patterns (skill will refuse)

- Recommending carousel for a pure narrative post (story immersion breaks across slides)
- Recommending poll for content that needs explanation (polls are shallow)
- Recommending video for data-heavy content (data needs scanning, not linear playback)
- Recommending carousel for a sub-300-char post (not enough material)
- Recommending text-only for a framework post with 5+ distinct concepts (cannibalizes saves)
- Recommending any format without citing a data point

## Resources

- `references/format-matrix.md` -- full content type taxonomy and decision matrix lookup
- `../../references/algorithm-heuristics.md` -- 2026 posting rules (format reach, timing, signal weights)
- `../../references/hook-formulas.md` -- 10 formula skeletons; hook type can influence format choice

## Related skills

- `linkedin-post-writer` -- creates posts and carousels from scratch using hook formulas
- `linkedin-humanizer` -- AI-tell scrubber and `--mode audit` pre-publish review
- `linkedin-content-planner` -- weekly format mix planning across pillars
- `linkedin-hook-extractor` -- reverse-engineer hooks from viral posts (useful before choosing a format)
