# Verification record / 검증 기록

2026-11-08. This record distinguishes automated full-course checks from sampled visual inspection.

## Full-course automated checks

- 60 sequential lessons, eight bilingual cards each: **480 PNGs**, all 1080×1350.
- Correct eight-unit counts and 20 relative Monday/Wednesday/Friday weeks.
- Source question IDs, prerequisite links, bilingual titles/notes/alt text, exact self-check placement and caption answers.
- **130 symbolic/arithmetic checks** covering the worked examples and self-check calculations; table dimensions and open graph points checked.
- Source and CSS hashes match the PNG manifests; all PNG dimensions and checksums verified. Combined captions fit Instagram’s 2,200-character limit.
- Chromium loads the bundled CJK font. All 480 cards pass content-boundary checks with 80px horizontal margins. Prose is 44px and table text 40px; effective base math and graph-label sizes are checked at ≥40px. Small course metadata is 25–27px. Mathematical subscripts/superscripts retain normal typographic sizing.
- Seven regression tests pass, including rejection of incorrect answers, missing translations/cards, unknown question IDs/lesson IDs, and nested formula arrays. The complete validator is tested not to modify source or export files.
- Textbook `validate_content.py --check` recomputes the existing 88 MCQ oracle checks, 37 FRQ scalar/identity checks and 16 worked-example checks without updating publication files or their historical review dates.

Commands are in the root README. CI runs the same read-only checks and regenerates L01 in a separate clean source copy with SVG/HTML/PNG outputs removed first.

## Actual visual review

Eight-card contact previews reviewed for **23 lessons**: L01, L02, L03, L04, L05, L07, L08, L12, L16, L18, L27, L29, L35, L38, L43, L48, L50, L52, L53, L54, L57, L58, L60. These span all eight units and include tables, open/closed points, derivative graphs, a slope field, shaded areas and dense formulas.

Full-size cards reviewed include L01/01, L01/05, L01/06, L43/07 and L48/03. A 360px-wide mobile-size sheet was inspected for L01/06, L16/05, L26/02, L38/07, L43/07 and L48/03. Long formulas were split into lines and the slope-field axis label was spaced away from its tick labels. Reviewed samples have no visible clipping or missing formulas/glyphs. The other cards receive automated layout checks; this record does not claim individual full-size visual review of all 480 cards.

## Portable textbook conversion smoke check

`scripts/render_documents.py --book english --output-dir ...` converted the existing English DOCX using LibreOffice in an isolated profile. The resulting test PDF has 81 pages; page 20 was rasterized with Poppler and visually checked. This test output is temporary and does not replace the supplied textbook PDFs. The historical textbook layout reports remain unchanged; there was no new full-book page-by-page review in this implementation.

## Practical limits

Calculations have independent checks and authored explanations have editorial review, but not every prose statement is formally machine-proved. This is a foundational lesson series and does not claim to cover every possible AP problem variant. Review actual student response and adapt pacing as needed. BC lessons, actual posting dates and social publishing are not included.
