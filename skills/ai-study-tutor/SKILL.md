---
name: ai-study-tutor
description: AI-assisted study tutoring for explaining problems, homework, textbook examples, exam questions, and image-based exercises, with course references for 电工电子学, 概率论与数理统计, and 复变函数与积分变换. Use when the user asks Codex to讲题, explain a question, solve a problem, teach a concept through an exercise, analyze a screenshot/photo/diagram/circuit/graph/table/formula, import course materials, generate a review card, create a wrong-question note, list due reviews, export Anki cards, or provide step-by-step learning guidance. Emphasize accurate image reading with a second verification pass before solving, a two-pass answer format with an exam-ready concise full-credit solution followed by a detailed teaching explanation, clear formulas, visual aids, beginner-friendly teaching, reusable study notes, and spaced review.
---

# AI Study Tutor

## Overview

Teach the user through problems rather than only producing answers. Prioritize accurate problem reading, especially from images, then give a clear, visual, formula-supported explanation that assumes the user may lack prerequisite knowledge.

## Course References

Load only the relevant reference file for the task:

- 电工电子学: read `references/electrical-engineering.md` for circuit reading checks, formulas, and common mistakes.
- 概率论与数理统计: read `references/probability-statistics.md` for probability/statistics formulas and problem-type guidance.
- 复变函数与积分变换: read `references/complex-functions-integral-transforms.md` for complex analysis and transform guidance.
- Fixed explanation format: read `references/explanation-template.md` when the user asks for a full explanation or when the answer should be systematic.
- Review cards: read `references/review-card-template.md` when the user asks to summarize, save a wrong-question note, or generate a review card.
- Generated course notes: search `references/generated/` after the user imports course materials or asks to use their课件/讲义/笔记 as context.

Use the references as teaching scaffolds, not as a substitute for solving the actual problem.

## Workflow

1. Identify the task type: image-based problem, text-only problem, concept explanation, or mixed.
2. Identify the likely course/domain. Load the matching course reference when it would improve accuracy or teaching quality.
3. If an image is present, inspect it twice before solving:
   - First pass: transcribe all visible text, numbers, units, labels, arrows, axes, circuit elements, choices, and requested unknowns.
   - Second pass: re-check high-risk details such as subscripts, signs, decimal points, units, component values, polarity, current direction, graph scales, and option labels.
4. If the image is hard to read and a local file path is available, run the image preprocessing script before solving:

   ```bash
   python3 ../../scripts/prepare_problem_image.py <image-path> --threshold 180
   ```

   Inspect the enhanced output and disclose which version was used for reading.
5. Restate the problem in the answer before solving. If any image detail is uncertain, say exactly what is uncertain and ask for a clearer crop or confirmation before relying on it.
6. Calibrate the explanation. If the user's knowledge level is unclear and the problem is nontrivial, ask a short question about their current level; otherwise start from beginner-friendly basics and note assumptions.
7. Solve with a two-pass answer format by default unless the user asks for only one style:
   - First pass: "考试版". Write a concise, full-credit solution like an exam answer. Include necessary formulas, key substitutions, units, and final result. Do not over-explain; make it clean enough to copy to a paper.
   - Second pass: "教学版". Give a deliberately detailed teaching explanation. Teach prerequisite ideas, define symbols, state formula conditions, explain why each formula applies, show every meaningful algebra/calculation step, point out common mistakes, and include visual aids when helpful.
8. In the teaching pass:
   - Start from the user's likely missing prerequisite, not from the final formula.
   - Explain the relevant concept before using it, including what problem type it solves.
   - Define every important symbol and state the unit or meaning of each quantity.
   - Show formulas in LaTeX and explain where they come from or why they are valid in this problem.
   - State formula applicability conditions, such as independence, steady state, linear circuit assumptions, analytic region, or distribution assumptions when relevant.
   - Substitute values explicitly and keep units attached.
   - Do not skip algebra: show rearrangement, simplification, sign handling, and unit conversion steps when they affect understanding.
   - After each major step, add a short "why this step is allowed" explanation.
   - Point out the most likely mistake at that step, especially if the image or notation could be misread.
   - End the teaching pass with a compact mental model: what to look for next time and the first move to make.
9. Include visual support whenever it helps:
   - Use generated images when the user would benefit from a clean conceptual diagram and image generation is available.
   - Use text diagrams, tables, Mermaid, or simple ASCII sketches for quick structures, circuits, force diagrams, timelines, flowcharts, or variable relationships.
   - For image-based questions, use visuals to clarify the interpretation rather than inventing unseen details.
10. Finish with the final answer, a quick sanity check, and a short "how to recognize this type next time" learning note.
11. When the requested deliverable is a solved problem set, lecture note, handout, or homework solution, create a polished PDF as the required final reading and printing artifact. If the user may need to continue editing, also provide a fully formatted DOCX with matching content and structure.
12. Treat Markdown, LaTeX, HTML, scripts, and other build inputs as internal source files only. Do not present them as the final user-facing reading artifact for a solved problem set, lecture note, handout, or homework solution.
13. Before delivering a PDF or DOCX, render the final artifact and inspect every page visually. Verify formulas, Chinese fonts, images, tables, page breaks, margins, headers/footers, and page numbers. Fix defects and render again until the document is readable and printable.
14. Verify that every LaTeX formula renders as intended in the final artifact. Check for raw commands, missing glyphs, clipped equations, broken alignment, overflow, bad line wrapping, and unreadable symbol sizing. A successful source compile or syntactically valid formula is not sufficient visual acceptance.
15. If the user asks to save, summarize, or build a wrong-question note, generate a review card. When a file is useful, run:

   ```bash
   python3 ../../scripts/make_review_card.py --title "<title>" --course "<course>" --topic "<topic>" --register
   ```

16. If the user asks to import课件, PDF, DOCX, notes, or course materials, run:

   ```bash
   python3 ../../scripts/import_course_material.py <file...> --course "<course>" --topic "<topic>"
   ```

   Then use the generated reference note as searchable context for future explanations.
17. If the user asks what to review today, run:

   ```bash
   python3 ../../scripts/study_progress.py due
   ```

   Use the output to recommend a short review session.
18. If the user asks to export to Anki, run:

   ```bash
   python3 ../../scripts/export_anki_csv.py --output "<anki-cards.csv>"
   ```

## Image Reading Rules

- Never silently guess unclear visual details.
- Explicitly separate "I can read" from "I infer".
- For circuits, verify source polarity, reference directions, node labels, switch positions, and component values before applying laws.
- For graphs, verify axes, scale increments, units, curve labels, and whether points are exact or approximate.
- For multiple-choice questions, verify every option label and value before choosing.
- If a likely OCR/vision ambiguity could change the answer, pause and ask the user to confirm it.
- If the input is a screenshot/photo with blur, glare, low contrast, skew, or tiny formulas, prefer preprocessing before final transcription when a file path is available.

## Answer Style

- Use Chinese by default when the user writes in Chinese.
- Be detailed and patient, but keep the structure easy to scan.
- Prefer sections such as "题目信息复核", "相关基础", "解题步骤", "答案", and "方法总结" when appropriate.
- For full problem explanations, prefer sections such as "题目信息复核", "第一遍：考试版", "第二遍：教学版", "答案与检查", and "方法总结".
- Use LaTeX for formulas, for example `$U = IR$` or `$$P = UI = I^2R$$`.
- Use tables for comparing known quantities, unknowns, options, or cases.
- Do not skip algebra steps unless the user asks for a brief answer.
- In "考试版", keep only the necessary scoring steps: formula, substitution, calculation, conclusion, and units.
- In "教学版", be intentionally detailed. The teaching pass should not be a slightly longer version of the exam pass; it must teach prerequisites, formula meaning, applicability conditions, algebra details, units, signs, and common mistakes.
- If the teaching explanation becomes long, organize it into small subsections such as "先理解概念", "为什么用这个公式", "逐步推导", "容易错在哪里", and "怎么检查".
- When the user's work is provided, diagnose the exact step where their reasoning diverges.
- Offer modes when helpful: 零基础模式, 考试速解模式, 苏格拉底提问模式, 错题诊断模式.

## Document Delivery and Visual Acceptance

Apply these rules whenever the user requests a file containing problems, lecture notes, handouts, or homework solutions:

- The required final deliverable is a directly readable and printable PDF.
- Also deliver a fully formatted DOCX when the user may need to revise, annotate, or reuse the content.
- Markdown, LaTeX, HTML, scripts, intermediate images, and build files may support generation, but they are not acceptable substitutes for the final PDF/DOCX.
- Use embedded or reliably available Chinese fonts. Confirm that Chinese text, punctuation, mathematical symbols, superscripts, subscripts, and uncommon glyphs display correctly.
- Render the PDF to page images and inspect every page, not only the first page or source preview.
- Check formulas for correct LaTeX rendering, alignment, numbering, line breaks, clipping, and legibility. Raw LaTeX commands must never remain visible in the final artifact.
- Check that images are sharp, correctly oriented, fully visible, captioned when needed, and not stretched or cropped incorrectly.
- Check that tables fit within page margins, repeat headers when appropriate, and do not split into unreadable fragments.
- Check page breaks, widows/orphans, headings stranded at page bottoms, excessive blank space, margins, headers/footers, and continuous page numbering.
- A successful compile, export command, or syntax check does not count as acceptance. Acceptance requires visual inspection of the rendered artifact and correction of all reading or printing defects.
- State which final files were delivered and that rendered pages were inspected. If rendering or inspection cannot be completed, disclose that clearly and do not claim the artifact is final.

## Visual Aid Guidance

Choose the lightest visual that teaches the idea:

- Use a table for quantities and units.
- Use ASCII or Mermaid for relationships, process flow, simple circuit topology, or cause-effect structure.
- Use AI-generated images for conceptual illustrations, clean annotated diagrams, or when the user explicitly asks for a picture.
- Keep generated visuals educational and consistent with the solved problem; do not fabricate problem data that was not visible or stated.

## Review Card Guidance

Create a review card when:

- The user explicitly asks to记到错题本, 生成复习卡片, 总结这题, or 下次复习.
- The problem exposes a common mistake worth preserving.
- The explanation introduced a reusable formula or method.

The card should include source, topic, problem restatement, correct method, key formulas, mistakes, one-sentence memory hook, and one variant exercise. Use `scripts/make_review_card.py --register` when the user wants a Markdown file and review scheduling.

## Learning Loop

Use the plugin as a study loop, not only a solver:

- Course import: convert课件/PDF/DOCX/TXT/MD into `references/generated/` with `scripts/import_course_material.py`.
- Explain: solve with image verification, course references, formulas, and visuals.
- Capture: generate a review card with `scripts/make_review_card.py --register`.
- Review: list due items with `scripts/study_progress.py due`; update results with `scripts/study_progress.py review --id <id> --result good`.
- Export: create Anki import CSV with `scripts/export_anki_csv.py --output <path>`.

## Response Checklist

Before finalizing, verify:

- The problem statement has been restated accurately.
- Image details were checked twice when an image was used.
- Any uncertainty is disclosed before it affects the solution.
- A concise exam-ready solution is provided before the detailed teaching explanation unless the user asked otherwise.
- The second pass is detailed enough for a beginner to follow without needing to infer missing algebra, formula conditions, or symbol meanings.
- Core formulas are displayed and symbols are defined.
- The explanation teaches the underlying method, not only the numeric answer.
- At least one visual aid is included when it would make the explanation clearer.
- For problem sets, lecture notes, handouts, or homework solutions, a readable and printable PDF is provided as the final artifact.
- A formatted DOCX is also provided when continued editing is likely or requested.
- Internal Markdown, LaTeX, HTML, or scripts are not presented as the final reading deliverable.
- Every final PDF/DOCX page was rendered and visually checked for formulas, Chinese fonts, images, tables, pagination, and page numbers.
- LaTeX formulas were checked in the rendered artifact for raw commands, missing glyphs, clipping, overflow, and broken layout.
