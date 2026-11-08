# Current handoff

Updated 2026-11-08. **AP Calculus AB: 60 lessons, 480 bilingual Instagram cards completed.** Repository: https://github.com/sklee935/AP-Calculus.

## Delivered

- Existing textbook Python, 124-question bank, graphs, PDF/Word editions, licensed full/subset Korean fonts and historical verification reports. Student books: 81 pages each; teacher guide: 56 pages.
- `instagram/lessons/L01.json`–`L60.json`: authoritative editable bilingual scripts, math, graphs/tables, source question links, prerequisites, self-check solutions, captions, alt text and 130 computation checks.
- Each `instagram/exports/Lxx/`: eight final PNGs, bilingual caption, eight alt texts, editable HTML, 8-card preview and source/CSS/PNG manifest.
- `instagram/CATALOG.md`, `instagram/schedule.csv`, browser gallery: 20 relative weeks, Monday/Wednesday/Friday. No dated schedule or Instagram posting.
- HTML/CSS + SVG + Playwright renderer; portable LibreOffice/Poppler textbook conversion; read-only validators, seven regression tests and GitHub Actions workflow.

## Setup and commands

Use Python 3.12, Node.js 24 and pnpm 11.25.0. Follow the root README for virtualenv, requirements, Node dependencies and `pnpm exec playwright install chromium`. No machine-specific paths are required.

```bash
python ap-calculus-ab/scripts/validate_content.py --check
python instagram/scripts/validate.py --complete --exports
python -m unittest discover -s tests -v
pnpm test:layout

# Edit the JSON first, then rebuild a lesson
python instagram/scripts/build.py --lessons L01
pnpm render --lessons L01
python instagram/scripts/catalog.py
python instagram/scripts/validate.py --complete --exports
```

Textbook rebuild: `python ap-calculus-ab/scripts/build_books.py`, `python scripts/render_documents.py --pages`, then `python ap-calculus-ab/scripts/validate_artifacts.py`. Install LibreOffice, Poppler and the bundled OTF font first; visually inspect regenerated pages.

## Validation and next work

The full course passes the 130 math checks, all 480 PNG/manifest checks, seven regression tests, and 480-card Chromium layout checks. Actual sampled visual review and the portable English-PDF smoke test are documented in [QA.md](QA.md). The first textbook checkpoint was pushed before the card course. GitHub Actions checks each subsequent push and performs a clean L01 rebuild.

No required AB implementation remains. Next optional work is instructor/academy branding once names are supplied, student feedback-based revisions, or the separate BC extension described in the textbook. Do not invent credentials, publish to Instagram, or assign real posting dates without a new user request.

## Source ownership and commit procedure

1. Read AGENTS.md and instagram/README.md. Textbook Python owns textbook answers; published JSON is downstream data. Lesson JSON owns card scripts.
2. Mark edited lessons in progress, preserve both languages/conditions/units, and update calculation checks. Regenerate outputs; update ready status before the final build.
3. Run read-only checks and inspect mobile/dense cards. CSS changes require regenerating all 60 lessons. Regenerate the catalog, update this handoff and actual QA scope.
4. Inspect `git diff`/`git status`, commit relevant sources plus verified exports, then push to main without force pushing. Confirm the GitHub Actions run succeeds.

Temporary QA pages, authoring scratch scripts, caches, node_modules and ZIP duplicates are ignored. Font OFL applies to the font; authored content has no general open-content license. See [SOURCES.md](SOURCES.md) for provenance and current official curriculum references.
