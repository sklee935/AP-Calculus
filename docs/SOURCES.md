# Sources and answer authority

Checked 2026-11-08 against the official course page and the Fall 2026 clarifications.

- [College Board AP Calculus AB course](https://apcentral.collegeboard.org/courses/ap-calculus-ab): eight units and course framework. The official page states that the 2026–27 clarifications do not change course content.
- [AP Calculus AB/BC clarifications, effective Fall 2026](https://apcentral.collegeboard.org/media/pdf/ap-calculus-ab-bc-course-and-exam-description-clarifications.pdf): EVT wording, differential-equation solution wording, and the May 2027 multiple-choice format (Part A: 29 questions/62 minutes; Part B: 13 questions/38 minutes). The supplied textbook already uses this format.
- Textbook Python sources under `ap-calculus-ab/scripts/`: authored question/answer authority. `content/question_bank.json` and `content/curriculum.json` are generated publications. Historical review dates are retained.
- Instagram `lessons/Lxx.json`: editable bilingual adaptations and new foundational examples. `source_question_ids` points to textbook question IDs, including `E##` exam question IDs. They can refer to the main example or the self-check. They do not mean an official College Board question or an unchanged quotation. An empty list identifies an independently authored example.

Do not silently alter a copied answer in the Instagram source. Correct the textbook Python first, export/validate the bank, then update its downstream lesson and verification. Independently authored examples have their own symbolic checks. Symbolic equality and arithmetic checks complement editorial review; they do not prove every verbal argument or guarantee instructional outcomes.

All diagrams are generated from stated mathematical expressions. The bundled Noto Sans CJK KR font is covered by its included SIL Open Font License. No other general license is granted to the authored instructional content.
