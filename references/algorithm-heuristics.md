# 2026 LinkedIn Posting Heuristics

**Last verified:** 2026-06-02
**Changelog:** see `references/algorithm-changelog.md`
**Update workflow:** run `linkedin-humanizer --mode update-heuristics` to check for staleness

Sources: 360Brew paper (arXiv 2501.16450), AuthoredUp analysis of 3M+ posts Mar 2025-Feb 2026 (updated May 2026), AuthoredUp 360Brew explainer (updated Apr 2026), Buffer LinkedIn Algorithm guide quoting LinkedIn VP Dan Roth + Director of PM Alice Xiong (Dec 2025), LinkedIn Pressroom (vertical video feed launch 2026), LinkedIn Guide to Creating newsletter (Jun 2026 -- "Turn your Insight into Influence").

## Timing

| Audience | Best window (local) |
|---|---|
| US B2B / founders | Tue 8:00 AM ET, Wed 10:00 AM ET |
| EU decision-makers | Tue/Wed 7:00-8:30 AM CET |
| Global mixed | Tue/Wed/Thu 7:30-9:00 AM, audience timezone |

Avoid: Mon before 9 AM, Fri after 2 PM, Sat/Sun (30-50% reach cut for B2B).

## Format reach multipliers (relative to each profile's own median post)

Source: AuthoredUp analysis of 3M+ LinkedIn posts, personal profiles, Mar 2025-Feb 2026.
Multipliers are relative to the profile's own median -- not cross-profile comparisons.

| Format | Reach multiplier | Engagement multiplier | Notes |
|---|---|---|---|
| Document carousel (PDF) | **1.39x** | **1.30x** | Best combined performer; only 4.88% of creators use it. Note: LinkedIn updated the feed UI in Jun 2026 to display document posts in a compact carousel format (similar to multi-photo posts) -- distribution and ranking logic unchanged (confirmed by LinkedIn creator newsletter) |
| Single image | **1.20x** | **1.33x** | Highest engagement multiplier; reliable volume play |
| Poll | **1.78x reach** | **0.37x engagement** | Reach trap -- votes are not conversations |
| Text-only | **1.07x** | **0.78x** | Near-average reach, below-average engagement |
| Native video | **0.86x** | **0.93x** | -36% YoY; longer videos (3+ min) outperform short clips |
| LinkedIn Article | **0.69x** | **0.44x** | Poor feed reach; use for SEO/evergreen, not distribution |
| Reshare | **0.29x** | **0.22x** | Worst format; write your own post instead |

**Format by follower count** (best reach format shifts with audience size):

| Follower bracket | Top reach format | Notes |
|---|---|---|
| 0-5K | Image | Low-friction, algorithm pushes beyond network |
| 5K-20K | Image + Document mix | Documents start compounding |
| 20K-50K | Document | 1.30x reach |
| 50K+ | Document | 1.49x reach -- largest gap at this tier |

## Length

- Sweet spot: **900-1,300 chars** (~150-220 words)
- Hook cutoff: **first 210 chars** (mobile "… see more" line)
- Long-form (1,500-1,900) works only with line breaks every 1-2 sentences and narrative payoff
- Avoid <400 chars unless you're an established voice with punchy observations

## Hashtags

360Brew reads topic from the post's text content using semantic embeddings -- hashtags are no longer
a meaningful distribution lever. LinkedIn's own editorial director Laura Lorenzetti confirmed (via Buffer, Dec 2025):
"a nice to have, not a need to have. Don't use too many, and it's ok if you don't use them."

- **0 hashtags** is fine; performs equal to or better than 5+
- **1-3 niche hashtags** may still help human readers navigate topics; negligible algorithmic effect
- **5+ hashtags** correlate with spammy-account patterns (negative signal)
- Placement: end of post only, never mid-sentence
- Do not use hashtags as a substitute for clear topic writing -- 360Brew ignores them for ranking

## Link placement

Previous advice (links in first comment = 2.1x) is no longer accurate.
LinkedIn's own team (Dan Roth, VP of Content; Buffer Dec 2025) and AuthoredUp 360Brew research both
indicate first-comment links are also suppressed under 360Brew.

Current guidance:
- **If linking is necessary:** put the link in the post body; remove the auto-generated preview card to reduce the visual signal to the algorithm; accept ~15-20% lower reach vs a no-link post
- **First comment links:** also deboosted -- not a reliable workaround
- **Best approach:** write a post that delivers full value without the link; if readers want the source they'll ask; add the link only when the post itself clearly explains the value of clicking
- LinkedIn's team explicitly said: "if you're writing great knowledge in that post, people are also more likely to be interested in what more they can get if they go to that link" -- the post quality, not link placement, determines whether the link gets clicks
- **Workaround phrasing** ("Source below ↓") adds no reach benefit under 360Brew and may read as engagement bait

## Signal weights (reported; not officially confirmed)

- Save = **5x a like**, 2x a comment
- In-depth comment (paragraph-length) > one-word reaction by 4x
- Comment-to-comment threading (user↔user replies) = strong quality signal
- Dwell time sweet spot: **31-60 seconds**
- "See More" expand + fast abandon (<3s) = clickbait penalty
- First 1-2 sentences scored for topic relevance before user scrolls

## First 60 minutes

- 60-90 min "Momentum Window" determines 80% of total reach
- Author reply to every comment within 90 min = required to hit the ceiling
- If 3+ substantive comments arrive in first 30 min, post gets second testing boost

## Delayed engagement (360Brew signal -- NEW)

Source: AuthoredUp 360Brew explainer (Apr 2026).

- Engagement arriving **24-72 hours after posting** triggers 4-6x better performance in "Suggested for you" feeds
- 360Brew does not treat a post as "done" after 24h -- it re-checks older posts when new engagement matches topic clusters
- Posts that keep collecting saves and in-depth comments get a second distribution wave
- Implication: reply to comments that arrive days later; don't abandon a post after day 1

## Profile-content alignment (360Brew signal -- NEW)

Source: arXiv 2501.16450 + AuthoredUp 360Brew explainer (Apr 2026).

360Brew reads both your profile and your posts as text, then checks whether they align.
A mismatch between stated expertise and post topics suppresses distribution.

- Your **headline and About section** should explicitly name your 2-3 core topics
- **80%+ of posts** should fall within those topic areas
- Allow ~**90 days** of consistent, aligned posting for 360Brew to fully categorize you
- "General Business" content (broad, unfocused) underperforms at **0.81x reach**
- Niche-specific content (e.g., "LinkedIn Content Creation") reaches **1.61x** median
- Scheduling posts does not penalize reach -- confirmed by LinkedIn's own team (Buffer Dec 2025)

## Posting frequency

Source: AuthoredUp analysis of 3M+ posts, personal profiles.

| Frequency | % of profiles | Median engagement rate | Median impressions/post |
|---|---|---|---|
| 1 post/week | 79.80% | 2.40% | 679 |
| 2-3 posts/week | 13.17% | 2.58% | 741 |
| 4-5 posts/week | 4.45% | **2.60%** | **870** |
| 6-7 posts/week | 1.61% | 2.54% | 959 |
| 8+ posts/week | 0.97% | 1.79% | 586 |

- **Sweet spot: 4-5 posts/week** -- highest engagement rate and 28% more impressions per post than once-weekly
- **8+ posts/week** causes sharp drop in both metrics -- audience fatigue + cannibalization
- 80% of profiles post only once a week; moving to 3-5 with quality content outperforms the vast majority
- Scheduling posts is **not penalized** -- confirmed by LinkedIn's own team (Buffer Dec 2025)

## Penalties

- Comment pods: **97% detection accuracy** (third-party claim). 360Brew measures lexical diversity and cluster overlap -- 5 unique varied comments outperform 50 identical "great post" reactions. Penalty: shadowban 3-14 days, reach cut 60-90%.
- TOS change: "We may limit how many comments a member can make in a time period."
- Recycled reply templates on own post: lexical-similarity detection downranks.
- Over-posting: 8+ posts/week triggers cannibalization and audience fatigue signal.

## Native articles

Source: AuthoredUp 3M post study (May 2026) contradicts earlier lift claims.

- Feed reach: **0.69x** reach multiplier, **0.44x** engagement -- underperforms all feed post formats
- LinkedIn Marketing Solutions Blog (Mar 2026): Articles are becoming stronger for **AI search discoverability** (cited and indexed by AI models) -- a different value proposition than feed reach
- Long-tail SEO via Google indexing remains a genuine bonus
- Use for **evergreen/reference content** where AI search and SEO value matter; not for feed distribution or timely takes
- Reshares perform even worse: **0.29x reach, 0.22x engagement** -- write your own post referencing the content and tag the author instead

## Engagement benchmarks by format (AuthoredUp 3M post study, Mar 2025-Feb 2026)

See "Format reach multipliers" section above for reach/engagement multipliers.
Additional context:

- Document posts account for **12.92% of all saves** -- roughly 2.6x their share of total content
- Polls generate votes, not conversations -- votes do not correlate with profile visits, follows, or pipeline
- Video reach dropped **36% YoY** for personal profiles; company pages (top 5%) see 1.72x reach from video
- Single image drives **highest engagement multiplier** (1.33x) -- best for comments and conversation
- Posting frequency of 4-5/week produces **28% more impressions per post** than once-weekly

## Native video rules

Longer videos outperform shorter ones (AuthoredUp analysis of 36,946 video posts, Oct 2025-Mar 2026):

| Duration | Reach multiplier | Engagement multiplier |
|---|---|---|
| 3 min+ | **1.21x** | **1.17x** |
| 90s-3 min | 1.07x | 1.09x |
| 60-90s | 0.97x | 1.00x |
| 30-60s | 0.95x | 0.96x |
| 0-30s | 0.96x | 0.91x |

- Short clips (TikTok-style, under 60s) perform worst -- LinkedIn is not a short-form platform
- **Aim for 90s-3+ min** with dense substance; avoid padding
- Captions mandatory (majority of users watch without sound)
- **Native upload only** -- YouTube links get ~60% reach cut
- Hook in first 3 seconds visually
- **9:16 vertical** to surface in LinkedIn's dedicated swipeable video feed (launched 2026); square (1:1) is safe fallback
- LinkedIn's vertical video feed surfaces content to non-followers -- use it for discovery

## Hook cutoff (device-specific)

- Desktop: ~210 chars before "…see more"
- **Mobile: ~140 chars before "…see more"**
- Write for the 140-char mobile line; the desktop window is a bonus.

## Close mechanics

- Specific closing question (e.g., "What's your experience with X?") boosts engagement **20-40%** vs generic "Thoughts?"
- Name the topic inside the CTA — generic CTAs don't trigger replies.

## Save ratio absolute case

- 200 saves ≈ **4x the reach** of 1,000 likes
- Checklists, frameworks, and templates are save-bait — optimize for save, not like.

## Engagement benchmarks by follower count

| Follower count | Expected engagement rate |
|---|---|
| 1K-5K | 4-8% |
| 5K-10K | 3-5% |
| 10K-50K | 2-4% |
| 50K+ | 1-3% |

Use to calibrate whether a post underperformed or is within band before blaming the algorithm.

## Comment-weight math (reach multipliers)

- Comments weigh **~3x more than likes** for reach
- Posts with back-and-forth conversation: **3x reach** of posts with passive engagement
- Posts where the author replies to commenters: **2x+ distribution**
- Author-replied comments count as a **fresh ranker signal each time**

## Pod / pattern detection (avoid)

Triggers for suppression:
- 15+ comments landing within a 90-second window
- Same accounts engaging at the same clock minute daily (e.g., 9:01 AM)
- Identical like/comment pattern across every post

Observed real consequence: one creator dropped from 8,500 to 340 impressions overnight after pod detection.

**Recovery times:**
- From pod detection: **6-8 weeks**
- Already-credible account cold start: ~1 week
- New account cold start: 30-60 days

## External-link penalty (expanded)

- External links in post body: **~60% reach reduction** (move to first comment)
- Engagement-bait CTAs ("Agree? Comment below!") now **actively suppressed**, not just ignored
- **Viewer tolerance score:** if users scroll past your posts without dwelling, distribution progressively collapses even for followers

## Edit-safety window

- Edits within first **3 hours** trigger a re-evaluation
- Structural restructuring (>20% of text changed) **resets distribution entirely**
- Typo fixes safe after the 90-min momentum window

## Post-publish engagement windows

| Phase | Window | Action |
|---|---|---|
| Warm-up | 15 min **BEFORE** publishing | Leave 3-5 substantive comments on others' posts |
| Critical | First 30 min AFTER publishing | Reply to every comment within minutes |
| Seeding | 15-30 min after posting | Leave 3-5 bonus comments on your own post to create thread depth |
| Visibility bump | Reply within 1st hour | +35% visibility lift |

## Pre-publish checklist

- [ ] Hook fits in first 210 chars (desktop); write for 140-char mobile line as primary target
- [ ] No em dashes (`—`), en dashes (`–`), double dashes (`--`)
- [ ] No AI vocabulary blacklist (leverage, fundamentally, delve, etc.)
- [ ] At least 1 specific number per 100 words
- [ ] At least 1 named entity (person, company, product)
- [ ] At least 1 first-person concrete detail (what you saw, did, said)
- [ ] If linking: link is in-body with preview card removed, OR omitted entirely -- first-comment links are no longer a reliable workaround
- [ ] 0-3 hashtags at end (optional; 0 is fine)
- [ ] Length 900-1,300 for medium, 1,500-1,900 for long
- [ ] Line breaks between ideas, not every sentence
- [ ] One moment of real vulnerability or stakes
- [ ] Close is a specific answerable question OR a clean landing (not "what do you think?")
- [ ] Profile headline/About section topics match the post topic (360Brew alignment check)
