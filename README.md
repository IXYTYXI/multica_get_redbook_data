# multi_get_redbook_skill (xhs-scraper)

Self-built Multica skill to scrape Xiaohongshu (小红书 / RED) — note search, author
profile, note details, comments — and write to Feishu bitable. Mirrors the existing
`douyin-scraper` architecture, adapted for Xiaohongshu. **Independent implementation;
it does not reuse the third-party MediaCrawler fork's code** (that project is a
validated reference for the signing *approach* only).

See `SKILL.md` for the full status table, prerequisites, and architecture.

## Quick check (offline, no login)

```bash
pip install -r requirements.txt
python main.py check        # -> "xhs-scraper scaffold OK"
```

## Status

- ✅ Stage 0 — scaffold, reused storage/downloader/date-filter, data models
- ⏳ Stage 1 — browser-injection signing (`core/sign.py`), login-gated (`XHS_COOKIE`)
- ⏳ Stage 2 — scrapers (search / note / comment / user) with `xsec_token` passthrough
- ⏳ Stage 3 — Feishu wiring, media, orchestration
- ⏳ Stage 4 — docs / known limits

## Login session

Signing needs a logged-in session. Provide the full cookie string via `XHS_COOKIE`,
injected through the Multica agent's custom_env (`multica agent env set`), never via a
workdir file or issue comment.
