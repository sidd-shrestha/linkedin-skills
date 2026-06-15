# Idea Depth Model

Four-tier assessment for classifying raw notes and ideas into content strategies.

## Tier 1: Seed

A seed is a single observation or thought with no supporting structure. It needs
development before it can be published.

### Detection signals

| Signal | Threshold |
|---|---|
| Length | < 50 words |
| Paragraphs | 1 (single sentence) |
| Structure | None -- no bullet lists, no headings, no numbered steps |
| Data points | 0 |
| Examples | 0 |
| Narrative markers | None (no named people, dates, or timeline) |
| Thesis clarity | Vague or implied |

### Examples

> "LinkedIn reach is down a lot this year. How do you even get seen anymore?"

> "I need to write about the EPF transfer thing. That was a process."

> "AI tools are getting too expensive."

### Strategy

Expand. The seed has a kernel of an idea but no substance. Recommend a structure
outline (hook, context, stakes, data point, takeaway, CTA) and route to
`linkedin-post-writer` with an expansion prompt.

---

## Tier 2: Sprout

A sprout is a complete thought. It has a clear thesis, some supporting detail,
and reads as a finished idea -- but it's only enough for a single post.

### Detection signals

| Signal | Threshold |
|---|---|
| Length | 50-200 words |
| Paragraphs | 1-2 |
| Structure | Minimal -- may have one list or one data point |
| Data points | 0-1 |
| Examples | 0-1 |
| Narrative markers | Optional (may name a person or date) |
| Thesis clarity | Clear, one main point |

### Examples

> "Started using a new cold outreach template last month. Open rates went from
> 38% to 62%. The only change: personalized the first line based on their latest
> LinkedIn post. Works across industries."

> "The Labor Act of Nepal says social security starts from day one -- probation
> doesn't exempt employers. Most companies still delay EPF contributions until
> after confirmation. That's illegal."

### Strategy

Single post. The idea is ready. Route to `linkedin-format-optimizer` for format
recommendation, then `linkedin-post-writer` for execution.

---

## Tier 3: Tree

A tree is a rich, multi-angle idea. It has structure, data, examples, and enough
material to support a pillar piece plus derivative posts.

### Detection signals

| Signal | Threshold |
|---|---|
| Length | 200+ words |
| Paragraphs | 3+ |
| Structure | Lists, headings, or numbered steps present |
| Data points | 2+ specific numbers or statistics |
| Examples | 2+ concrete examples or cases |
| Narrative markers | Named people, timeline, or specific events |
| Distinct angles | 2-4 different angles on the same topic |
| Derivative potential | Can extract 3-5 standalone posts from the material |

### Examples

> A 400-word note covering: the user's EPF transfer experience, the two pathways
> (continue UCIN vs new account), what happens with gaps, the Labor Act section 52
> angle, the EPF vs SSF difference, what to ask your employer. Six distinct angles
> within one coherent topic.

### Strategy

Atomize. One pillar long-form piece plus 3-5 derivative posts across 1-2 weeks.
Derivatives can include carousel, poll, text post (counterintuitive finding),
text post (question), and a short video or image post.

Route to `linkedin-post-writer` for the pillar piece, then suggest `--plan` mode
for the full sequence.

---

## Tier 4: Forest

A forest contains multiple distinct topic areas that would each support their own
pillar piece. The material spans different subjects, not just different angles on
one subject.

### Detection signals

| Signal | Threshold |
|---|---|
| Length | 500+ words |
| Topic areas | 3+ distinct subjects |
| Per-topic depth | Each topic area has Tree-level richness |
| Structural divide | Clear topic breaks, headings, or subject transitions |
| Series potential | Could sustain 2-4+ weeks of content |

### Examples

> A 1,000-word document containing notes on: LinkedIn algorithm changes in 2026,
> cold outreach best practices, EPF transfer rights in Nepal, AI tool pricing
> trends, and thoughts on building a personal brand. Five distinct topics.

### Strategy

Serialize. Plan a multi-week pillar series. Each topic area gets its own week
with a pillar article + derivative posts. Priority by goal (reach: pick the
hottest topic; authority: pick the deepest).

Route to `linkedin-content-planner` for the full series calendar, then
`linkedin-post-writer` for each week's pillar.

---

## Goal modifiers

The user's stated goal can shift the recommendation within a tier:

| Goal | Seed | Sprout | Tree | Forest |
|---|---|---|---|---|
| **Reach** | Expand with broad hook | Format for max distribution | Aggressive atomization (5-7 posts) | Start with hottest topic first |
| **Authority** | Expand with data depth | Single polished pillar | One strong pillar, fewer derivatives | Deepest topic first, build slowly |
| **Leads** | Expand with CTA structure | Format as carousel + soft offer | Pillar + lead magnet CTA | Topic with highest conversion potential first |
| **Comments** | Expand with opinion hook | Format as text + question | Atomize with engagement hooks | Most controversial topic first |
| **Research** | N/A (too thin) | Format as poll | One poll + text post | Poll across multiple topics |

## Edge cases

| Situation | Handling |
|---|---|
| Note is 300 words but all one angle, no structure | Treat as Sprout (single post), not Tree |
| Note is 150 words but has 3 data points and a clear framework | Treat as Tree (rich density, not length) |
| User pastes a completed post draft | Return "This is already a Sprout. Want a format check?" → route to format-optimizer --audit |
| Mixed: one developed topic + two throwaway lines | Treat the developed topic at its tier, note the throwaway lines as separate seeds |
| All caps, no punctuation, stream of consciousness | Still assess on content. If the idea is there, classify it. |
