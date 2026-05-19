# Format Decision Matrix

The core logic for mapping content type + goal + structural signals to an optimal LinkedIn format.

## Content type classification

Classify the post draft or topic into one of these types based on its semantics, structure, and phrasing:

| Content type | Detection signals | Example opening |
|---|---|---|
| Educational / framework | "Here's a framework", "X steps to", step-by-step language, numbered lists, definitions, models | "The 4-step framework I use for customer discovery" |
| How-to / tutorial | Imperative verbs, instructional tone, walkthrough structure, "how to", tool mentions | "Here's how I structure my discovery calls" |
| Personal story / narrative | First-person past tense, timeline markers, specific date/anchor, emotional language | "A year ago I nearly quit my startup" |
| Opinion / hot take | Strong stance, contrarian framing, "here's why", debunking, declarative claims | "Most people are wrong about unit economics" |
| Data breakdown / receipts | Numbers, percentages, comparisons, "I analyzed", "the data shows", screenshots | "I analyzed 500 cold emails. Here's the one metric that matters" |
| Industry analysis / trend | Market shifts, comparisons, "is dead / dying", future predictions | "The era of generalist agencies is ending" |
| Announcement / news | Launch, update, milestone, "we just", "announcing", specific date reference | "We just crossed $100K ARR" |
| Community question | Direct question to audience, poll-like framing, opinion solicitation | "What's your biggest challenge with hiring?" |
| Quick tip / micro-content | Single insight, actionable in <1 minute, no narrative arc | "One trick for better cold outreach" |
| Lead magnet / offer | Free resource, giveaway, download, "I'm giving away" | "I'm giving away my content calendar template" |
| Case study / transformation | Before/after, specific results, named client/user, metric improvement | "How a SaaS founder grew from 0 to 1,000 leads" |
| Contrarian / sacred cow | Challenges consensus, "everyone says X but", historical receipts | "Remote work has been dying since 2023" |

## Format recommendation matrix

Primary mapping: content type x primary goal -> recommended format.

### Goal: Maximum reach

| Content type | Primary format | Reach multiplier | Why |
|---|---|---|---|
| Educational / framework | Carousel | 1.7-2.3x | Dwell time from multi-slide consumption |
| How-to / tutorial | Carousel | 1.7-2.3x | Sequential format matches instructional flow |
| Data breakdown / receipts | Carousel | 1.7-2.3x | Visual comparison, slide-by-slide reveal |
| Industry analysis / trend | Carousel | 1.7-2.3x | Framework-heavy, comparison-rich |
| Case study / transformation | Carousel | 1.7-2.3x | Before/after visual storytelling |
| Personal story / narrative | Text + image | 1.0-1.3x | Authenticity beats flash for story |
| Opinion / hot take | Text-only | 1.0-1.3x | Debate drives comments = algorithm boost |
| Contrarian / sacred cow | Text-only | 1.0-1.3x | Argument format; comments = reach |
| Community question | Poll | 1.1x | +206% reach vs average post |
| Quick tip / micro-content | Text + image | 1.0-1.3x | Low effort, fast consumption |
| Lead magnet / offer | Carousel | 1.7-2.3x | Save-bait, shareable asset |
| Announcement / news | Text + image | 1.0-1.3x | Timeliness > format optimization |

### Goal: Maximum engagement (comments + discussion)

| Content type | Primary format | Expected eng. rate | Why |
|---|---|---|---|
| Opinion / hot take | Text-only | Highest comment rate | Polarization drives replies |
| Contrarian / sacred cow | Text-only | Highest comment rate | Argument invites counter-argument |
| Personal story / narrative | Text-only | High comment rate | Relatability triggers sharing |
| Community question | Poll | +206% reach | Low-friction participation |
| Educational / framework | Carousel | 6.60% | Saves = 5x a like signal |
| Industry analysis / trend | Text-only | High comment rate | Expert opinions invite debate |
| Announcement / news | Text + image | Moderate | Congratulatory engagement |
| How-to / tutorial | Carousel | ~6x vs text | Framework saves |
| Case study / transformation | Carousel | High save rate | Aspirational saves |
| Lead magnet / offer | Carousel | High share rate | Asset-based engagement |
| Quick tip / micro-content | Single image | Moderate | Low-investment engagement |

### Goal: Authority building (saves + shares + credibility)

| Content type | Primary format | Save rate | Why |
|---|---|---|---|
| Educational / framework | Carousel | Highest | Frameworks are save-bait |
| Data breakdown / receipts | Carousel | Highest | Reference-quality data |
| How-to / tutorial | Carousel | High | Step-by-step = future reference |
| Case study / transformation | Carousel | High | Aspirational saves |
| Industry analysis / trend | Carousel | High | Reference material |
| Lead magnet / offer | Carousel | Highest | Asset = shareable |
| Personal story / narrative | Text-only | Moderate | Story = less saveable |
| Opinion / hot take | Text-only | Low | Takes = ephemeral |
| Contrarian / sacred cow | Text-only | Low | Takes = ephemeral |

### Goal: Lead generation

| Content type | Primary format | Conversion potential | Why |
|---|---|---|---|
| Lead magnet / offer | Carousel | Highest | CTA on last slide, gated asset |
| Case study / transformation | Carousel | High | Proof + CTA across slides |
| Educational / framework | Carousel | Medium | Top-of-funnel awareness |
| How-to / tutorial | Carousel | Medium | Value-first, soft CTA |
| Data breakdown / receipts | Carousel | Medium | Authority builds trust |
| Announcement / news | Text + image | Low | Awareness only |

### Goal: Audience research

| Content type | Primary format | Data quality | Why |
|---|---|---|---|
| Community question | Poll | Highest | Structured vote data |
| Community question | Text-only | High | Unstructured comment insights |
| Opinion / hot take | Text-only | Medium | Self-selecting respondents |

## Structural signal detection

Signals in the draft that influence format suitability:

| Signal | Indicates | Format implication |
|---|---|---|
| `|||` markers | User already split content into slides | Carousel-ready. Honor the structure. |
| `[[flowchart:...]]` | Diagram inclusion | Carousel-ready. Diagram content benefits from visual. |
| `[[framework:...]]` | Framework diagram | Carousel-ready. Framework = visual. |
| `[claude_logo]` or logo markers | Visual asset mentioned | Carousel-ready. Image assets exist. |
| Bulleted / numbered lists (3+ items) | Structured, scannable content | Carousel or text with strong formatting. Avoid video/poll. |
| 3+ specific numbers or statistics | Data-heavy | Carousel for visual comparison; text if narrative. |
| Personal name + specific date/timeline | Narrative / story | Text-only or text + personal photo. |
| Length <300 chars | Too short for carousel | Text, text + image, or poll. |
| Length 900-1,300 chars | Sweet spot for text | Flexible — can be text or carousel. |
| Length >1,500 chars | Long-form | Carousel (breaks up text) or long-form text with breaks. |
| Contrarian framing ("X is wrong", "everyone says") | Opinion / debate | Text-only (comments = reach). |
| Poll-like phrasing ("how many of you", "what's your") | Community question | Poll format. |
| External link in body | Link-sharing | Move to first comment. Format stays flexible. |

## Conversion feasibility checks

When deciding whether a draft *can* be converted to another format:

### Text -> Carousel

| Check | Pass condition |
|---|---|
| Has 4+ distinct ideas/paragraphs | Each paragraph maps to a slide |
| Has ||| markers | Already structured |
| Has data, lists, or comparisons | Visual presentation adds value |
| Total length >500 chars | Enough material to fill 4+ slides |
| Not primarily narrative/story | Stories lose impact when chopped into slides |

### Text -> Poll

| Check | Pass condition |
|---|---|
| Contains a question | Can be reformulated as poll |
| Question has 2-5 clear answer options | Poll needs predefined choices |
| Topic invites opinion (not fact) | Polls need subjective answers |

### Text -> Video

| Check | Pass condition |
|---|---|
| Personal story or opinion | Best video content types |
| Has emotional arc | Video amplifies emotional resonance |
| Can be delivered in 30-90s | LinkedIn video length sweet spot |

### Carousel -> Text

| Check | Pass condition |
|---|---|
| Has 6+ slides | Text can condense |
| Each slide is text-heavy | No visual dependency |
| Slides are sequential (not visual comparison) | No layout loss |

## Format anti-patterns by content type

| Content type | Avoid | Why |
|---|---|---|
| Educational / framework | Poll | Framework needs explanation; poll is too shallow |
| Personal story / narrative | Carousel | Story needs narrative flow; slides break immersion |
| Opinion / hot take | Carousel | Argument needs full text; slides fragment the take |
| Data breakdown / receipts | Video | Data needs scanning, not linear playback |
| Community question | Carousel | Question + swiping = friction |
| Quick tip | Carousel | Too much effort for too little content |
| Lead magnet | Text-only | Asset needs visual wrapper to feel valuable |
