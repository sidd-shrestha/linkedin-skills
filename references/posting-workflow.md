# Posting Workflow

## Project File Structure

```
drafts/
├── ideas/             ← raw captured ideas, one-liners, snippets from Obsidian
├── draft-post/        ← full post drafts ready for polishing
├── carousel_output/   ← generated carousel PDFs
├── carousel_preview/  ← slide preview PNGs
└── archive/           ← executed ideas (+ executed-ideas.md log)
```

The entire `drafts/` folder is gitignored — nothing inside gets committed.

## Ideation Sources
- **Multiple sources**: newsletters, social media (Twitter/LinkedIn/Reddit), personal experience (work stories, failures, lessons), conversations (client calls, DMs, comments)
- **Capture destination**: Obsidian vault (links, notes, snippets, voice memos) + bookmarks/saved messages to self
- **Project landing**: `drafts/ideas/` — when an Obsidian note is ready to become a post, drop the raw one-liner or snippet here

## Content Pillars (Mixed / Balanced)
Rotate across pillars — no fixed percentages, but covers:
- Authority / expertise
- Personal narrative / stories
- Community / engagement

## Weekly Rhythm (Aspirational)
- **Sunday distill** (30 min): review Obsidian vault, pick 3-4 captured items, turn each into a one-liner → save to `drafts/ideas/`
- Pick one → write full draft in `drafts/draft-post/`
- Ideally 2 good posts/week rather than 7 forced ones

## Post Creation Flow
1. **Capture** — idea lands in `drafts/ideas/` as a one-liner or snippet
2. **Write first** — expand into full draft in `drafts/draft-post/` without worrying about format
3. **Run through linkedin-format-optimizer** — pick the best format (text, carousel, poll, etc.)
4. **Polish** via linkedin-post-writer (hook, structure, CTA)
5. **Humanize** via linkedin-humanizer (scrub AI tells, enforce voice)
6. **Approve** — review card, reply "yes" to publish
7. **Publish** — manual copy-paste or auto-publish via Publora
8. **Archive** — move idea file from `drafts/ideas/` → `drafts/archive/` and log in `executed-ideas.md`

## Post-Publishing Engagement
- Reply to all comments (within 1-2 hours)
- Engage on peers' posts (10-20 comments/day)
- Track performance, note what worked

## Tools Used
| Step | Tool |
|---|---|
| Capture | Obsidian → `drafts/ideas/` |
| Format selection | `linkedin-format-optimizer` skill |
| Drafting | `linkedin-post-writer` skill |
| Comments | `linkedin-comment-drafter` / `linkedin-reply-handler` |
| Humanizer | `linkedin-humanizer` skill |
| Planning | `linkedin-content-planner` skill |
| Publishing | `lib.publish()` / Publora / manual |
