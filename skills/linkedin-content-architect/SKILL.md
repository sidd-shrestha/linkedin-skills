---
name: linkedin-content-architect
description: Assess raw ideas and notes to recommend a content strategy -- expand into long-form, atomize into micro-content, serialize across weeks, or publish as a single post. Two modes: --assess classifies the idea depth (seed/sprout/tree/forest) and recommends a strategy; --plan produces a full posting sequence for tree/forest ideas. Routes to linkedin-post-writer, linkedin-format-optimizer, or linkedin-content-planner for execution. Not for picking a single format (use linkedin-format-optimizer) or planning a weekly calendar (use linkedin-content-planner).
---

# LinkedIn Content Architect

Analyze raw, unstructured ideas and notes to determine the optimal content strategy: should this be expanded into a long-form pillar, atomized into multiple derivative posts, serialized across weeks, or published as a single piece? Built on the 2026 Pillar-to-Spokes model.

## When to use

- User drops raw notes / half-formed ideas and asks "what should I do with this?"
- User has a draft and asks "is this one post or should I break it up?"
- User has a rich topic and wants a posting sequence planned out
- User is unsure whether an idea is ready to post or needs more work
- User has too many ideas and wants to prioritize which to develop

## Modes

### `--assess` (default)
Given raw notes or an idea, classifies the depth tier and recommends a strategy.

### `--plan`
Given a Tree or Forest idea, produces a full posting sequence across 1-4 weeks.

## Idea depth model

Refer to `references/idea-depth-model.md` for the full assessment criteria. Summary:

| Tier | Typical length | Structure | Strategy |
|---|---|---|---|
| Seed | < 50 words | None; single observation | Expand into a full post |
| Sprout | 50-200 words | One clear point, 1-2 paragraphs | Single post in best format |
| Tree | 200+ words | Multiple paragraphs, data, lists, examples | Atomize: pillar + derivatives |
| Forest | 500+ words | Multiple distinct topic areas | Serialize: multi-week pillar plan |

## Steps (`--assess` mode)

1. **Accept input.** User provides raw notes, a half-baked idea, a draft, or a topic. Accept any unstructured text.
2. **Classify the depth tier.** Analyze against the 4-tier model in `references/idea-depth-model.md`. Look for: word count, paragraph count, structural signals (lists, headings, data points), narrative elements (specific people, dates, timeline), and breadth (distinct concepts).
3. **Assess optional goal.** If the user provides a primary goal (reach / authority / leads / comments / research), factor it in. Reach favors aggressive atomization. Authority favors a single polished pillar.
4. **Build the recommendation.**
   - **Seed:** "This is a seed idea. It needs expansion before it can be posted. Here's a structure outline to develop it into a full post."
   - **Sprout:** "This is ready as a single post. Recommended format: [format]. Here's a hook angle."
   - **Tree:** "This has material for a full pillar piece. Recommended plan: long-form article + carousel + [N] text posts + poll, spread across 1-2 weeks."
   - **Forest:** "This spans multiple distinct topics. Recommended plan: [N] pillar pieces across [N] weeks, each with its own derivative posts."
5. **Offer execution handoff.**
   - Seed: "Want me to expand this into a full post?" → route to `linkedin-post-writer`
   - Sprout: "Want me to write this as a [format]?" → route to `linkedin-format-optimizer` then `linkedin-post-writer`
   - Tree: "Want me to build the posting sequence?" → route to `--plan` mode or `linkedin-content-planner`
   - Forest: "Want me to plan the full series?" → route to `--plan` mode or `linkedin-content-planner`
6. **On approval.** Execute the handoff. If the user accepts, delegate to the appropriate skill. Suggest `linkedin-humanizer --mode audit` before publishing.

## Steps (`--plan` mode)

1. **Require Tree or Forest tier.** Refuse if the idea is Seed or Sprout (not enough material for a sequence).
2. **Determine sequence scope.** For Tree: 1-2 weeks. For Forest: 2-4 weeks.
3. **Build the calendar.** Per day: pillar, format, hook type, CTA type.
   - Week 1 Mon: Long-form article (pillar)
   - Week 1 Wed: Carousel (framework extracted from pillar)
   - Week 1 Fri: Poll or text post (engagement)
   - Week 2 Tue: Text post (counterintuitive finding)
   - Week 2 Thu: Text post (one question to ask)
4. **Route to content-planner.** Feed the sequence into `linkedin-content-planner` for calendar formatting + pillar rotation validation.
5. **Offer per-post creation.** "Want me to write the pillar article now?" → route to `linkedin-post-writer`.

## Hard rules

Global voice rules: see root `SKILL.md` section Voice rules. Additional skill-specific rules:

- Never recommend expansion for a Sprout that is already a complete thought. If the user's note has a clear thesis and supporting detail, respect it as-is.
- Never recommend atomization for a personal story (stories lose impact when split across pieces).
- Always include the rationale: why this tier, why this strategy, and what changes if the goal changes.
- When the tier is ambiguous (e.g., a long note that's all one idea), default to the lower tier.
- In `--plan` mode, never plan more than 4 weeks out — beyond that, the user's priorities will shift.

## Anti-patterns (skill will refuse)

- Recommending atomization for pure narrative content (breaks story immersion)
- Recommending expansion for a complete Sprout (pads a finished thought into filler)
- Recommending serialization for a single-idea Tree (overcomplicates something that fits one week)
- Planning a sequence longer than 4 weeks without user asking for it

## Resources

- `references/idea-depth-model.md` — full assessment criteria with detection examples
- `references/strategy-templates.md` — expand, single-post, atomize, and serialize pattern blueprints
- `../../references/algorithm-heuristics.md` — 2026 reach data and signal weights
- `../../references/hook-formulas.md` — hook templates referenced in sequence plans

## Related skills

- `linkedin-format-optimizer` — picks the format once strategy is chosen (Sprout/atomization)
- `linkedin-content-planner` — receives the sequence from --plan mode for calendar formatting
- `linkedin-post-writer` — executes individual post/carousel drafts
- `linkedin-humanizer` — pre-publish audit on final drafts
