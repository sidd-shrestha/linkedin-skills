# Content Architect — Design Plan

## Why this skill exists

`linkedin-format-optimizer` recommends a format (text, carousel, poll, video, image) for a
topic or draft — but it can't assess whether the raw idea should be **expanded into long-form**
or **deconstructed into micro-content**. The 2026 LinkedIn strategy consensus is **Pillar-to-Spokes**:
one long-form piece → 5-10+ derivative posts. This skill bridges the gap between raw notes and
execution by deciding the *strategy* first, then routing to format/planner/writer.

## How it differs from siblings

| Skill | Input | Question answered |
|---|---|---|
| `linkedin-format-optimizer` | Topic or completed draft | "What format?" |
| `linkedin-content-planner` | Theme + audience + pillars | "What's my week look like?" |
| `linkedin-content-architect` | Raw unstructured notes | "What *strategy* — expand, atomize, serialize, or single-post?" |

## Core logic: 4-tier depth assessment

| Tier | Signal | Strategy |
|---|---|---|
| **Seed** | <50 words, single observation, no structure, no data | → Expand. Route to post-writer with structure prompt |
| **Sprout** | 50-200 words, one thesis, 1-2 paragraphs, complete thought | → Single post. Route to format-optimizer + post-writer |
| **Tree** | 200+ words, structured (lists/data/examples), multiple angles | → Atomize. Pillar article + 3-5 derivatives |
| **Forest** | 500+ words, multiple distinct concepts, series potential | → Serialize. Multi-week pillar plan |

Goal (reach/authority/leads/comments/research) modifies the strategy: go aggressive on atomization
for reach, consolidate for authority.

## Files

| File | Purpose |
|---|---|
| `skills/linkedin-content-architect/SKILL.md` | Skill definition, --assess and --plan modes |
| `skills/linkedin-content-architect/references/idea-depth-model.md` | 4-tier assessment criteria with detection signals |
| `skills/linkedin-content-architect/references/strategy-templates.md` | Blueprints for expand, single-post, atomize, serialize |

## Registration changes

- `.claude-plugin/plugin.json` → v1.0.5, "13 skills"
- `.claude-plugin/marketplace.json` → v1.0.5
- `SKILL.md` (root) → add bundle entry
- `README.md` → add skill table row
- `skills/linkedin-format-optimizer/SKILL.md` → related skills ref
- `skills/linkedin-content-planner/SKILL.md` → related skills ref
- `skills/linkedin-post-writer/SKILL.md` → related skills ref
