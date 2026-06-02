# LinkedIn Algorithm Changelog

Tracks known changes to LinkedIn's ranking algorithm and feed heuristics.
Each entry records what changed, the source, and which repo files were updated.

When a new change is detected, append an entry at the top of the "Entries" section
and update every file listed in the "Files to update" column.

To run a semi-automated update check, invoke:
`linkedin-humanizer --mode update-heuristics`
See `skills/linkedin-humanizer/sub-skills/algorithm-updater.md` for the full workflow.

---

## Source hierarchy

Not all sources carry the same weight. Use this tier system when sources conflict:

| Tier | Type | Use for |
|---|---|---|
| 1 -- Primary | LinkedIn's own publications + arXiv papers by LinkedIn researchers | Feature launches, official algorithm intent, model architecture |
| 2 -- Empirical | Large-scale behavioral data studies (AuthoredUp, van der Blom) | Measured multipliers, engagement rates, format performance numbers that LinkedIn doesn't publish |
| 3 -- Commentary | Newsletters, analyst reports, creator takes | Context, synthesis, practitioner patterns -- never cite a number from here without a tier 1 or 2 backing it |

When tier 1 and tier 2 conflict, flag it explicitly in the changelog entry rather than silently overwriting.

## Trusted sources to monitor

### Tier 1 -- LinkedIn official

| Source | URL | Update cadence |
|---|---|---|
| LinkedIn Official Blog | https://www.linkedin.com/blog/member | As published; check monthly |
| LinkedIn Engineering Blog | https://engineering.linkedin.com/blog | Irregular; check monthly |
| LinkedIn Pressroom | https://news.linkedin.com | As published |
| LinkedIn Marketing Solutions Blog | https://business.linkedin.com/marketing-solutions/blog | Weekly |
| arXiv (LinkedIn-authored papers) | https://arxiv.org/search/?searchtype=all&query=linkedin+ranking | Irregular |
| Gyanda Sachdeva (VP Product, LinkedIn) | https://www.linkedin.com/in/gyandasachdeva/ | Irregular; watch for algo announcements |

### Tier 2 -- Empirical data

| Source | URL | Update cadence |
|---|---|---|
| AuthoredUp reach data | https://authoredup.com/blog | Quarterly benchmarks |
| Richard van der Blom annual report | https://www.linkedin.com/in/richardvanderblom/ | Annual (Jan) |
| 360Brew newsletter + papers | https://360brew.com | Weekly digest |

### Tier 1.5 -- Freely fetchable, directly quotes LinkedIn's own team

These are third-party publications that conduct on-record interviews with LinkedIn product and editorial staff. Not official, but the closest publicly accessible proxy to LinkedIn's own newsletter (which requires login and cannot be fetched automatically).

| Source | URL | Update cadence | Notes |
|---|---|---|---|
| Buffer LinkedIn Algorithm guide | https://buffer.com/resources/linkedin-algorithm/ | Updated as LinkedIn changes; check quarterly | Quotes LinkedIn VP of Content Dan Roth + Director of PM Alice Xiong directly |
| Search Engine Journal (LinkedIn tag) | https://www.searchenginejournal.com/tag/linkedin/ | As published | Covers official LinkedIn product announcements and algorithm posts |
| Social Media Examiner (LinkedIn) | https://www.socialmediaexaminer.com/category/linkedin/ | Weekly | Summarizes LinkedIn creator guidance and product changes |

### LinkedIn creator newsletter (manual input only)

LinkedIn's own creator showcase and newsletters (`linkedin.com/showcase/linkedin-guide-to-creating/`) are login-walled and **cannot be fetched automatically** by any free tool. To include this source in an update run:

1. Open `https://www.linkedin.com/showcase/linkedin-guide-to-creating/posts/?feedView=all` while logged in
2. Copy the text of any posts published since the last changelog entry date
3. Paste into the `linkedin-humanizer --mode update-heuristics` session when prompted
4. The updater will analyze and propose changelog entries for any new guidance found

### Tier 3 -- Commentary and synthesis

| Source | URL | Update cadence |
|---|---|---|
| Trust Insights | https://www.trustinsights.ai/blog | Weekly |
| Social Media Today (LinkedIn tag) | https://www.socialmediatoday.com/tag/linkedin | As published |

---

## Files to update when heuristics change

| File | What it contains |
|---|---|
| `references/algorithm-heuristics.md` | Canonical timing, format multipliers, signal weights, penalties |
| `skills/linkedin-humanizer/references/audit-checklist.md` | 20-point pre-publish checklist |
| `skills/linkedin-humanizer/sub-skills/post-audit.md` | Blockers and Warnings for audit mode |
| `skills/linkedin-humanizer/references/audit-ai-tells.md` | AI-tell blacklist and regex patterns |
| `references/industry-benchmarks.md` | Engagement rates by follower count and format |
| `SKILL.md` (root) | Voice rules and char ranges referenced in the bundle description |

---

## Entries

### 2026-06-02 -- LinkedIn newsletter batch: document UI change confirmed; qualitative creator guidance reviewed

**Date verified:** 2026-06-02
**Sources (Tier 1 -- LinkedIn's own creator newsletter and carousel guides):**
- "Turn your Insight into Influence" -- LinkedIn Guide to Creating newsletter
- "Create with Strategic Intent" -- LinkedIn Guide to Creating newsletter
- "Your Content Should Move Your Career Forward" -- LinkedIn carousel PDF
- "How to Build a Repeatable Format" -- LinkedIn carousel PDF

**What changed:**

| Area | Old value | New value | Status |
|---|---|---|---|
| Document post feed display | Standard carousel view | Compact carousel format (similar to multi-photo posts) -- UI change only | CHANGED (UI only) |
| Distribution / ranking for documents | unchanged | Confirmed unchanged by LinkedIn directly | CONFIRMED |

**Qualitative guidance confirmed (no new algorithmic rules found):**
- Post with strategic intent: choose 2-3 core topics that reflect where you want to go, and return to them consistently
- Repeatable format structure: Hook -> Takeaway -> CTA is LinkedIn's own recommended baseline
- Topic consistency compounds over time -- reinforces the 360Brew profile-alignment finding already in heuristics
- "Your strategic content lane" = intersection of skills you want and areas you know well (Venn diagram from LinkedIn PDF)
- Set a sustainable rhythm (weekly / biweekly / monthly) -- consistent cadence beats sporadic bursts

**Impact:** Low -- one UI change (no ranking effect). Qualitative guidance confirms existing rules; no numeric updates needed.

**Files updated:**
- [x] references/algorithm-heuristics.md -- document carousel UI note added; sources line updated

---

### 2026-06-02 -- 360Brew impact update: format multipliers, link placement, hashtags, delayed engagement, profile alignment

**Date verified:** 2026-06-02
**Sources:**
- AuthoredUp analysis of 3M+ LinkedIn posts, personal profiles, Mar 2025-Feb 2026 (Tier 2) -- https://authoredup.com/blog/best-performing-content-on-linkedin
- AuthoredUp "LinkedIn 360Brew: What Actually Changed" updated Apr 2026 (Tier 2) -- https://authoredup.com/blog/linkedin-360brew
- AuthoredUp LinkedIn Video Posts guide, Apr 2026 (Tier 2) -- https://authoredup.com/blog/linkedin-video-posts
- Buffer "How LinkedIn's Algorithm Works in 2026, According to the LinkedIn Team" Dec 2025 (Tier 1.5) -- https://buffer.com/resources/linkedin-algorithm/ -- quotes VP of Content Dan Roth and Director of PM Alice Xiong directly
- LinkedIn Pressroom (Tier 1) -- confirmed vertical video feed launch 2026
- arXiv 2501.16450 (Tier 1) -- 360Brew model architecture confirming semantic topic reading

**Note on LinkedIn newsletter:** `linkedin.com/showcase/linkedin-guide-to-creating/` is login-walled and was not checked in this run. Paste content from that page into the next update run to include it.

**What changed:**

| Area | Old value | New value | Status |
|---|---|---|---|
| Carousel multiplier | 1.7-2.3x | 1.39x reach, 1.30x engagement | CHANGED |
| Native video multiplier | 1.4-1.8x | 0.86x reach, 0.93x engagement; -36% YoY | CHANGED |
| Text-only multiplier | 1.0-1.3x | 1.07x reach, 0.78x engagement | CHANGED |
| Single image multiplier | 1.0x baseline | 1.20x reach, 1.33x engagement (above baseline) | CHANGED |
| Poll multiplier | 1.1x | 1.78x reach / 0.37x engagement (reach trap) | CHANGED |
| Video length advice | 30-90s recommended | 3+ min = 1.21x reach; under 60s performs worst | CHANGED |
| Link in first comment | ~2.1x impressions | Also suppressed under 360Brew; no longer a reliable workaround | CHANGED |
| Hashtags | 1-3 niche = ~5% lift | Negligible; 360Brew reads topic from text; confirmed by LinkedIn's own team | CHANGED |
| Article multiplier | ~1.2-1.4x lift | 0.69x reach, 0.44x engagement in feed; SEO/AI-search value remains | CHANGED |
| Reshare performance | not listed | 0.29x reach, 0.22x engagement -- worst format | NEW |
| Vertical video feed | not mentioned | LinkedIn launched dedicated swipeable vertical video feed in 2026 | NEW |
| Delayed engagement | not mentioned | Engagement 24-72h after posting triggers 4-6x better performance in Suggested feeds | NEW |
| Profile-content alignment | not mentioned | 360Brew checks profile-post topic match; mismatch suppresses reach; ~90 days to establish cluster | NEW |
| Format by follower count | not mentioned | Under 5K: images lead; 5K-20K: mix; 20K+: documents lead (1.30x-1.49x) | NEW |
| Posting frequency sweet spot | 2+ posts/day = penalty | 4-5 posts/week = peak; 8+/week drops sharply | UPDATED |
| Mobile hook cutoff | stated as 265 chars in audit-checklist | Corrected to 140 chars mobile / 210 chars desktop | FIXED |

**Impact:** High -- format multipliers, link placement advice, and hashtag guidance were all materially stale. Any audit or post-write recommendation using the old numbers would have given incorrect guidance.

**Files updated:**
- [x] references/algorithm-heuristics.md
- [x] skills/linkedin-humanizer/references/audit-checklist.md
- [ ] skills/linkedin-humanizer/sub-skills/post-audit.md -- review Blockers/Warnings for link placement rule
- [ ] references/industry-benchmarks.md -- engagement rate benchmarks by follower count may need updating

---

### 2026-Q1 -- Baseline established

**Date verified:** 2026-01-01 (Q1 baseline)
**Sources:**
- 360Brew / arXiv 2501.16450 (LinkedIn ranking foundation model)
- AuthoredUp 2026 reach data (format multipliers, engagement rates)
- Trust Insights Q1 2026 guide (timing windows, momentum mechanics)
- Social Media Today reporting on Gyanda Sachdeva anti-pod measures

**What was current at this baseline:**

| Area | Rule |
|---|---|
| Format multipliers | Carousel 1.7-2.3x, native video 1.4-1.8x, text 1.0-1.3x, external link 0.4-0.6x |
| Length sweet spot | 900-1,300 chars; hook in first 210 chars (desktop), 140 chars (mobile) |
| Hashtags | 0-2 niche hashtags; 5+ is a negative signal |
| Link placement | In-body links suppressed 40-60%; first-comment links get ~2.1x impressions |
| Signal weights | Save = 5x like; in-depth comment > one-word by 4x; dwell 31-60s is sweet spot |
| Momentum window | First 60-90 min determines ~80% of total reach |
| Pod detection | 97% accuracy; shadowban 3-14 days, reach cut 60-90% |
| Over-posting | 2+ posts/day triggers cannibalization signal |
| Edit-safety | Edits within first 3h trigger re-evaluation; >20% text change resets distribution |
| Native video | 30-90s, captioned, vertical 9:16, native upload only |
| Close mechanics | Specific closing question boosts engagement 20-40% vs generic "Thoughts?" |

**Files updated:** All files listed above set to reflect this baseline.

---

### How to add a new entry

```
### YYYY-MM-DD -- <short description of change>

**Date verified:** YYYY-MM-DD
**Source:** <publication name + URL>
**Reported by:** <author or handle if relevant>

**What changed:**
- <old rule> -> <new rule>
- Example: "Carousel multiplier was 1.7-2.3x -> now 2.0-2.8x per AuthoredUp Q2 2026 data"

**Impact:** <High / Medium / Low> -- <one sentence on who is affected>

**Files updated:**
- [ ] references/algorithm-heuristics.md
- [ ] skills/linkedin-humanizer/references/audit-checklist.md
- [ ] skills/linkedin-humanizer/sub-skills/post-audit.md
- [ ] (others as applicable)
```
