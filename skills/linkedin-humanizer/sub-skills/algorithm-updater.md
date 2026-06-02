# Algorithm Updater Sub-skill

Invoked via `linkedin-humanizer --mode update-heuristics`.

Fetches the freely accessible trusted sources listed below, optionally accepts
pasted content from LinkedIn's login-walled newsletter, compares all findings
against the repo's current heuristics, and produces:
1. A diff report of rules that appear stale or contradicted by newer data
2. Proposed edits to the affected files (shown for approval before writing)
3. A pre-filled changelog entry ready to append

---

## When to run

- Monthly, as part of routine maintenance
- After a major LinkedIn product announcement
- After the annual Richard van der Blom report (usually January)
- When a post underperforms unexpectedly and the format/timing rules may be out of date

Trigger phrases: "check if the algorithm is up to date", "update heuristics",
"is our algorithm data still current", "run the algorithm updater".

---

## Source tiers

See `../../references/algorithm-changelog.md` for the full source hierarchy.
Short version for this workflow:

- **Tier 1** -- LinkedIn official (blog, engineering blog, pressroom, arXiv papers)
- **Tier 1.5** -- Freely fetchable sources that directly quote LinkedIn's own team
- **Tier 2** -- Large-scale empirical data studies
- **Tier 3** -- Commentary; never cite a number without tier 1 or 2 backing

When sources conflict, flag it explicitly rather than silently overwriting.

---

## Step 1 -- Fetch freely accessible sources

Fetch the following URLs and extract content related to LinkedIn's ranking,
feed algorithm, format performance, engagement signals, or creator guidelines.
Focus on content published or updated after the most recent changelog entry date.

### Tier 1 -- LinkedIn official (always fetch)

| Source | URL |
|---|---|
| LinkedIn Official Blog | https://www.linkedin.com/blog/member |
| LinkedIn Engineering Blog | https://engineering.linkedin.com/blog |
| LinkedIn Pressroom | https://news.linkedin.com |
| LinkedIn Marketing Solutions Blog | https://business.linkedin.com/marketing-solutions/blog |
| arXiv (LinkedIn-authored papers) | https://arxiv.org/search/?searchtype=all&query=linkedin+ranking |

### Tier 1.5 -- Freely fetchable, directly quotes LinkedIn's team (always fetch)

| Source | URL |
|---|---|
| Buffer LinkedIn Algorithm guide | https://buffer.com/resources/linkedin-algorithm/ |
| Search Engine Journal (LinkedIn tag) | https://www.searchenginejournal.com/tag/linkedin/ |
| Social Media Examiner (LinkedIn) | https://www.socialmediaexaminer.com/category/linkedin/ |

### Tier 2 -- Empirical data (always fetch)

| Source | URL |
|---|---|
| AuthoredUp blog | https://authoredup.com/blog |
| 360Brew newsletter | https://360brew.com |

For each fetched source, note:
- Publication or update date of the most recent relevant article
- Any numeric claim (multipliers, percentages, char counts, time windows)
- Any rule that explicitly contradicts or updates a value in `../../references/algorithm-heuristics.md`
- Whether the claim is the publication's own data or a quote from LinkedIn staff

---

## Step 2 -- Check newsletter-inbox/ for LinkedIn-sourced pastes

LinkedIn's own creator newsletter and showcase posts require a login and cannot
be fetched automatically. The workflow for adding them is documented in
`../../../newsletter-inbox/README.md`.

Before proceeding, check whether any `.md` files (other than `README.md`) exist
in `newsletter-inbox/`:

```
newsletter-inbox/
  README.md          <- always present, skip
  2026-06-*.md       <- process these if present
```

**If files are present:** read each one (`.md` and `.pdf` both supported) and
treat their content as **Tier 1** -- LinkedIn's own voice. Extract any numeric
claims, rule changes, new features, or guidance changes, then add them to the
findings before proceeding to Step 3. After the full run completes, move all
processed files into `newsletter-inbox/archive/` (create the folder if absent).

**If no files are present:** say:
> "No LinkedIn newsletter pastes found in `newsletter-inbox/`. To include
> LinkedIn's own creator guidance, follow the instructions in
> `newsletter-inbox/README.md` and re-run the updater.
> Continuing with freely accessible sources only."

Then proceed to Step 3 with the fetched sources from Step 1.

---

## Step 3 -- Compare against current heuristics

Read `../../references/algorithm-heuristics.md` in full.

For each value or rule found in Steps 1-2, compare it to the current file.
Flag as:

- **CHANGED** -- the new source gives a different number or contradicts the rule
- **CONFIRMED** -- the new source repeats the same value (increases confidence)
- **NEW** -- the new source describes a rule or signal not currently in the file
- **DEPRECATED** -- the new source explicitly says a previous rule no longer applies
- **CONFLICT** -- tier 1 and tier 2 sources disagree; flag without resolving

Produce a comparison table:

| Area | Current value | New value | Status | Tier | Source |
|---|---|---|---|---|---|
| Example: carousel multiplier | 1.7-2.3x | 1.39x reach | CHANGED | 2 | AuthoredUp May 2026 |

---

## Step 4 -- Produce a diff report

For each CHANGED, NEW, DEPRECATED, or CONFLICT item, write the specific edit needed:

```
FILE: references/algorithm-heuristics.md
OLD: | Document carousel (PDF) | 1.7-2.3x |
NEW: | Document carousel (PDF) | 1.39x reach, 1.30x engagement |
REASON: AuthoredUp analysis of 3M+ posts Mar 2025-Feb 2026
        (https://authoredup.com/blog/best-performing-content-on-linkedin)
TIER: 2 -- empirical, no conflicting tier 1 source found
```

If a change also affects the audit checklist or post-audit blockers/warnings,
flag those files too with the specific section that needs updating.

For CONFLICT items, present both values and explain which tier wins and why,
then ask the user to decide before writing.

---

## Step 5 -- Ask for approval before writing anything

Present the full diff report to the user. Do NOT write any files yet.

Say:
> "I found N potential updates. Here is the full diff report above.
> Say 'apply all' to apply every item, list specific numbers to apply a subset,
> or 'skip' any items you want to leave unchanged."

---

## Step 6 -- Apply approved edits

For each approved edit:
1. Apply the change to the target file using exact line/section replacement
2. Preserve surrounding markdown structure (table alignment, heading levels)
3. Do not rewrite sections that were not flagged
4. After each file is written, confirm: "Updated `<filename>`."

---

## Step 7 -- Append changelog entry

After all edits are applied, append a new entry to
`../../references/algorithm-changelog.md` using the template at the bottom
of that file. Fill in:
- Today's date as "Date verified"
- Each source URL and tier used
- A one-line summary per changed rule (old -> new)
- Checked boxes for all files that were updated

---

## Hard rules for this sub-skill

- Never fabricate numeric claims. Every value must come from a fetched source
  with a URL, a pasted LinkedIn post, or a cited arXiv paper.
- If a source is paywalled or unavailable, note "could not verify" and skip it.
- Never delete existing changelog entries. Only prepend new ones above the baseline.
- Never update `references/algorithm-heuristics.md` without also checking whether
  `skills/linkedin-humanizer/references/audit-checklist.md` and
  `skills/linkedin-humanizer/sub-skills/post-audit.md` need corresponding edits.
- If no changes are found, report "All heuristics confirmed current as of <date>."
  and append a brief confirmation entry to the changelog with sources checked.
- Scheduling content is not penalized (confirmed by LinkedIn's own team) --
  never add a rule that implies otherwise.
