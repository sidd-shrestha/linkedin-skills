# Newsletter Inbox

Drop pasted content from LinkedIn's login-walled sources here before running
`linkedin-humanizer --mode update-heuristics`.

The updater reads every `.md` file in this folder as Tier 1 input -- LinkedIn's
own voice -- and includes it in the diff against the current heuristics.

---

## How to use

### Step 1 -- Grab the content

Open any of these in your browser while logged into LinkedIn:

| Source | URL |
|---|---|
| LinkedIn Guide to Creating (showcase) | https://www.linkedin.com/showcase/linkedin-guide-to-creating/posts/?feedView=all |
| LinkedIn News newsletter | https://www.linkedin.com/newsletters/linkedin-news-6657388191436759040/ |
| Gyanda Sachdeva (VP Product) posts | https://www.linkedin.com/in/gyandasachdeva/recent-activity/all/ |
| LinkedIn for Creators newsletter | https://www.linkedin.com/newsletters/linkedin-for-creators/ |

Copy the text of any posts or articles published since the date of the last
changelog entry in `../references/algorithm-changelog.md`.

### Step 2 -- Paste into a file here

Create a new `.md` or drop a `.pdf` file in this folder named by date and source, for example:

```
newsletter-inbox/2026-06-linkedin-guide-to-creating.md
newsletter-inbox/2026-06-gyanda-sachdeva-posts.md
newsletter-inbox/2026-06-linkedin-carousel-guide.pdf
```

For `.md` files: paste the raw text. No special formatting needed -- just the post content,
one post per section or all together. Include the post date if visible.

For `.pdf` files: drop the PDF directly. The updater can read PDF content natively.
This is useful for LinkedIn's visual carousel guides published via the showcase.

### Step 3 -- Run the updater

```
linkedin-humanizer --mode update-heuristics
```

The updater will automatically read all `.md` files present in this folder,
treat them as Tier 1 sources, and include any new guidance in the diff report.

### Step 4 -- Archive processed files

After the updater has run and the changelog entry has been appended, the updater
automatically moves all processed files into `newsletter-inbox/archive/`.

If you ran the updater manually or need to archive files yourself:

```bash
# Windows PowerShell
New-Item -ItemType Directory -Force -Path "newsletter-inbox\archive"
Move-Item newsletter-inbox\*.md newsletter-inbox\archive\ -Exclude README.md
Move-Item newsletter-inbox\*.pdf newsletter-inbox\archive\
```

The `archive/` subfolder and its contents are also gitignored -- nothing in
`newsletter-inbox/` (except this README) is committed to the repo.

---

## What to look for when reading the showcase

LinkedIn's creator team posts about algorithm changes in plain language.
Watch specifically for:

- Changes to **which formats** get boosted or penalized
- New **engagement signals** being added or weighted differently
- **Posting frequency** guidance
- Changes to **link** or **hashtag** handling
- Announcements of **new features** (vertical video, newsletters, events, etc.)
- Any mention of **reach drops** or **algorithm updates** being rolled out

You don't need to copy everything -- just posts that mention reach, algorithm,
format performance, engagement signals, or creator best practices.

---

## File naming convention

```
YYYY-MM-source-description.md
```

Examples:
- `2026-06-linkedin-guide-to-creating.md`
- `2026-06-gyanda-algorithm-announcement.md`
- `2026-07-linkedin-news-creator-update.md`
