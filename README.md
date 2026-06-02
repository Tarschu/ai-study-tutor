# AI Study Tutor

AI Study Tutor is a local Codex plugin for course-aware problem solving, verified image reading, visual explanations, review cards, spaced review, and Anki-ready export.

它的目标不是只给答案，而是像一个谨慎的学习助教：先读题、复核图片信息，再从基础概念讲起，最后把有价值的题整理成可复习的错题卡。

![AI Study Tutor flow](assets/screenshot.png)

## Features

- **Verified image reading**: transcribe image-based questions, then re-check numbers, units, labels, directions, graph scales, circuit polarity, and option text before solving.
- **Course-aware tutoring**: built-in references for:
  - 电工电子学
  - 概率论与数理统计
  - 复变函数与积分变换
- **Fixed explanation template**: restate the problem, list knowns/unknowns, teach prerequisites, solve step by step, check the result, and summarize the method.
- **Image preprocessing**: enhance blurry or low-contrast screenshots/photos before reading.
- **Review cards**: generate Markdown wrong-question cards and register them in a spaced review queue.
- **Course material import**: import PDF, DOCX, TXT, and Markdown course materials into generated reference notes.
- **Anki export**: export review cards to CSV for Anki import.

## Installation

This repository is a Codex plugin. For local development, place it under your local plugins directory and install it from a configured marketplace.

If using the personal marketplace flow used by this project:

```bash
codex plugin add ai-study-tutor@migrated-claude-plugins
```

After installing or updating the plugin, start a new Codex thread so the latest skill instructions and scripts are loaded.

## Usage

Use the skill explicitly:

```text
Use $ai-study-tutor to explain this problem step by step.
```

Or ask naturally:

```text
讲一下这道题，先帮我确认图片里有没有读错。
```

```text
把这道电工电子学题讲清楚，并生成一张复习卡片。
```

```text
导入这份概率论课件，以后讲题时参考它。
```

```text
今天我应该复习哪些错题？
```

## Learning Loop

```mermaid
flowchart TD
  A["Import course materials"] --> B["Explain problem"]
  B --> C["Verify image details twice"]
  C --> D["Teach concepts and solve"]
  D --> E["Create review card"]
  E --> F["Schedule spaced review"]
  F --> G["Export to Anki CSV"]
```

## Included Skill

The main skill lives at:

```text
skills/ai-study-tutor/SKILL.md
```

It instructs Codex to:

- load the relevant course reference only when useful;
- inspect image questions twice before solving;
- disclose uncertain visual details instead of guessing;
- use LaTeX for formulas;
- include tables, Mermaid, ASCII diagrams, or generated images when helpful;
- create review cards and spaced review records when requested.

## Course References

Reference files are in:

```text
skills/ai-study-tutor/references/
```

Current references:

- `electrical-engineering.md`
- `probability-statistics.md`
- `complex-functions-integral-transforms.md`
- `explanation-template.md`
- `review-card-template.md`

Generated course notes from imported materials are written to:

```text
skills/ai-study-tutor/references/generated/
```

## Scripts

### Prepare Problem Image

Enhance a screenshot/photo for easier reading:

```bash
python3 scripts/prepare_problem_image.py ./problem.png --threshold 180
```

Outputs grayscale, enhanced, and optional black/white copies.

### Import Course Material

Import PDF, DOCX, TXT, or Markdown files into generated course references:

```bash
python3 scripts/import_course_material.py ./lecture.pdf \
  --course "电工电子学" \
  --topic "一阶电路"
```

PDF import requires `pypdf`; DOCX import requires `python-docx`.

### Make Review Card

Create a Markdown review card:

```bash
python3 scripts/make_review_card.py \
  --title "欧姆定律基础题" \
  --course "电工电子学" \
  --topic "欧姆定律" \
  --question "已知电压和电阻求电流" \
  --method "确认已知量 U 和 R" \
  --method "使用 I=U/R" \
  --formula '$I=U/R$' \
  --mistake "不要把千欧看成欧" \
  --memory "先看单位，再套欧姆定律" \
  --register
```

With `--register`, the card is also added to the spaced review queue.

### Study Progress

List due reviews:

```bash
python3 scripts/study_progress.py due
```

Record a review result:

```bash
python3 scripts/study_progress.py review \
  --id "电工电子学--欧姆定律基础题" \
  --result good
```

Review results:

- `again`
- `hard`
- `good`
- `easy`
- `mastered`

Progress is stored by default at:

```text
~/.ai-study-tutor/progress.json
```

### Export Anki CSV

Export review cards for Anki:

```bash
python3 scripts/export_anki_csv.py --output ./anki-cards.csv
```

The CSV fields are:

- `Front`
- `Back`
- `Tags`

Import the CSV in Anki using the standard file import flow.

## Repository Structure

```text
.
├── .codex-plugin/
│   └── plugin.json
├── assets/
│   ├── icon.png
│   ├── logo.png
│   └── screenshot.png
├── scripts/
│   ├── export_anki_csv.py
│   ├── import_course_material.py
│   ├── make_review_card.py
│   ├── prepare_problem_image.py
│   └── study_progress.py
└── skills/
    └── ai-study-tutor/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        └── references/
```

## Development

Validate the skill:

```bash
PYTHONPATH=/tmp/codex-skill-validate-pyyaml \
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/ai-study-tutor
```

Validate the plugin:

```bash
PYTHONPATH=/tmp/codex-skill-validate-pyyaml \
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

Update the local plugin cachebuster after changes:

```bash
python3 ~/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py .
codex plugin add ai-study-tutor@migrated-claude-plugins
```

## License

No license has been selected yet. Add one before publishing this repository publicly.
