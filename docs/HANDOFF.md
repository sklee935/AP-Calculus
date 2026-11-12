# Current handoff

Updated 2026-11-12. **AP Calculus AB: 60 lessons, 480 bilingual Instagram cards completed.** Repository: https://github.com/sklee935/AP-Calculus.

## Active publication request

The user requested **one additional Instagram post**, explicitly including actual publication. L05 is prepared under that existing authorization; publication is **pending**. Chrome's account/tabs could be read, but account-switch clicks and keyboard actions did not take effect, direct tab control failed, and native coordinate input reported no available window. No upload or Share action was performed in this attempt. The user has been asked to restore the browser connection and select @logoscrest.math. Do not ask for publishing permission again after recovery; the request already authorizes one post.

Prepared files: `instagram/publishing/L05-caption.txt` (1,151 characters) and `L05-post.json`. The eight existing `instagram/exports/L05/01.png`–`08.png` are the upload assets. The branded caption preserves both canonical language bodies and adds explicit radians/x≠0/squeeze-inequality conditions. Lesson source/CSS/exports remain unchanged. `python instagram/scripts/validate.py --lessons L05 --exports` passed (8 cards, 2 math checks, 8 PNGs); the eight-card contact sheet was visually reviewed. The graph shows the oscillating curve between ±x²; check answer is 3/2. There is no live-post review or confirmed post URL for L05.

After browser control is restored, verify the target account and inspect its current posts to avoid duplicates, upload L05 once in 01–08 order at 4:5, add the prepared caption, eight bilingual alt texts joined by ` | `, and the Suwanee, Georgia city tag. Keep Facebook cross-post off. Verify sharing, location/caption and all eight indices, save a UI proof, then update the manifest/publication log, commit/push and confirm CI. Further posts after this one require a new user request.

## Delivered

- Existing textbook Python, 124-question bank, graphs, PDF/Word editions, licensed full/subset Korean fonts and historical verification reports. Student books: 81 pages each; teacher guide: 56 pages.
- `instagram/lessons/L01.json`–`L60.json`: authoritative editable bilingual scripts, math, graphs/tables, source question links, prerequisites, self-check solutions, captions, alt text and 130 computation checks.
- Each `instagram/exports/Lxx/`: eight final PNGs, bilingual caption, eight alt texts, editable HTML, 8-card preview and source/CSS/PNG manifest.
- `instagram/CATALOG.md`, `instagram/schedule.csv`, browser gallery: 20 relative weeks, Monday/Wednesday/Friday. No dated or automated course schedule.
- Separate user-requested launch: [@logoscrest.math](https://www.instagram.com/logoscrest.math/) now uses **Logos Crest Math Academy | Suwanee**, the book/cross/geometry crest avatar, and a Suwanee, GA bilingual-study bio. Public brand assets and the exact built-in image-generation prompt are under `branding/logos-crest/`.
- **L01–L04 manually published on 2026-11-08** under separate user requests, each as an 8-card 4:5 carousel with bilingual caption/alt text and the Suwanee, Georgia city tag. [L01](https://www.instagram.com/p/DfftFgOGyO5/) · [L02](https://www.instagram.com/p/DffuwIvm9b1/) · [L03: tables and graphs](https://www.instagram.com/p/DffwVVDmwZf/) · [L04: factoring and conjugates](https://www.instagram.com/p/DffwrPmGwgb/) · [publication log](../instagram/publishing/README.md). L05–L60 have not been published by this task. No Facebook cross-post.
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

Launch checkpoint validation: `python instagram/scripts/validate.py --lessons L01 --exports` passed (8 cards, 2 math checks, 8 PNGs); `git diff --check` passed. A read-only metadata inspection verified the avatar SHA-256/1254×1254 RGB format, 105-character bio, eight 1080×1350 card paths, 953-character actual caption, eight bilingual alt texts and publication-log link in both catalog output and generator. Lesson source/CSS/exports were not changed for this launch.

Second-post checkpoint: `python instagram/scripts/validate.py --lessons L02 --exports` passed (8 cards, 3 math checks, 8 PNGs). The 888-character branded caption preserves the lesson's two language versions and check answer. The eight-card contact sheet was reviewed before posting. Instagram confirmed sharing, the profile showed two posts, and all eight carousel indices were traversed. Live cards 1, 3 (graph with open point (0,2) and filled point (0,5)), and 8 were visually inspected. L02 math/scripts/exports remain unchanged.

Two-additional-post checkpoint: the user's request for two more posts was fulfilled with L03 and L04. `python instagram/scripts/validate.py --lessons L03,L04 --exports` passed (16 cards, 4 math checks, 16 PNGs). Both contact sheets were reviewed; metadata inspection checked all image paths/dimensions, eight bilingual alt texts per post, and preservation of both canonical caption bodies. Actual branded caption lengths are 1,031 and 929 characters. Instagram confirmed sharing each post and the profile count rose to three, then four. Both live carousels were traversed through index 8. Live cards reviewed: L03 1/3/8 (including open (1,2), filled (1,4)); L04 1/5/8 (including the x≠4 cancellation condition). Actual URLs, selected city and review scope are recorded in `instagram/publishing/L03-post.json` and `L04-post.json`. Teaching source/CSS/exports are unchanged. L05 is the next unposted prepared lesson; wait for a new user request before publishing it.

No required AB implementation remains; the current L05 publication request is pending as described above. The logo and four earlier posts were completed under the user's separate requests. Actual UI verification for L01: profile photo/bio saved, profile showed one post, published caption and Suwanee location were visible, carousel advanced through all eight indices; live cards 1 and 8 were visually reviewed. The later verification records above supplement this scope. No additional visual certification of every middle card is implied. No street address or trademark clearance is available. Optional work is student feedback-based revisions, new branded lesson variants, or the separate BC extension described in the textbook. Do not invent credentials or assign real posting dates without a new user request.

## Source ownership and commit procedure

1. Read AGENTS.md and instagram/README.md. Textbook Python owns textbook answers; published JSON is downstream data. Lesson JSON owns card scripts.
2. Mark edited lessons in progress, preserve both languages/conditions/units, and update calculation checks. Regenerate outputs; update ready status before the final build.
3. Run read-only checks and inspect mobile/dense cards. CSS changes require regenerating all 60 lessons. Regenerate the catalog, update this handoff and actual QA scope.
4. Inspect `git diff`/`git status`, commit relevant sources plus verified exports, then push to main without force pushing. Confirm the GitHub Actions run succeeds.

Temporary QA pages, authoring scratch scripts, caches, node_modules and ZIP duplicates are ignored. Font OFL applies to the font; authored content has no general open-content license. See [SOURCES.md](SOURCES.md) for provenance and current official curriculum references.
