# Approved implementation plan

## Teaching outcome

Create 60 sequential introductory AP Calculus AB lessons, each containing eight 1080×1350 cards with English and Korean together. Use a bright digital whiteboard, large readable text, accurate typeset math, diagrams, teacher annotations, worked reasoning, error correction, and a self-check. Provide the self-check answer and reasoning in the bilingual caption.

Card order: learning question; prerequisite/definition; visual intuition; worked step 1; worked step 2; interpretation; common error and summary; independent check.

Main prose is at least 40px and safe margins at least 80px. A neutral course label and lesson number replace any unspecified academy or instructor identity. Do not invent qualifications or promises.

## Full series

The authoritative 60-item scope and 20-week Monday/Wednesday/Friday relative schedule are in instagram/course.json. The eight unit counts are 8, 8, 6, 6, 8, 10, 6, and 8. Actual posting dates and automatic social-media publishing are outside this task.

Lesson 01 starts with lim(x→3)(x²−9)/(x−3)=6, a nearby-values table, factoring, cancellation valid only for x≠3, and a graph with a hole at (3,6). The check is lim(x→4)(x²−16)/(x−4)=8.

## Implementation

First upload the supplied textbook sources, licensed fonts, PDF/Word editions, and this plan. Then create bilingual lesson JSON, editable HTML/CSS, SVG math/graphs, a Playwright PNG renderer, captions, alt text, previews, and non-mutating validation. Validate the first lesson before scaling by unit. Use verified textbook items where appropriate and independently verify newly authored examples.

Ship portable setup and commands for Python, Node/Chromium, and optional LibreOffice/Poppler textbook rendering. Maintain README.md, AGENTS.md, CLAUDE.md, and docs/HANDOFF.md so another machine or coding agent can clone and continue.

## Acceptance

- 60 unique sequential lesson IDs, eight bilingual slides each, 480 final PNGs.
- Linked source questions/prerequisites and correct math, domains, graph coordinates, units, and caption answers.
- No clipped text, missing glyphs/formulas, undersized main prose, or out-of-bounds content.
- Reproducible first-lesson generation from a fresh clone and read-only CI checks.
- Checked commits pushed to sklee935/AP-Calculus with an accurate handoff.
