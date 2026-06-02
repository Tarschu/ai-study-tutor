# AI Study Tutor

[Chinese version](README.md)

AI Study Tutor is a local Codex plugin for course-aware problem solving, verified image reading, visual explanations, review cards, spaced review, and Anki-ready export.

Its goal is not just to produce answers. It works like a careful study tutor: read the problem first, verify image details, teach from the underlying concepts, and turn useful problems into reusable review cards.

![AI Study Tutor flow](assets/screenshot.png)

## Features

- **Verified image reading**: transcribe image-based questions, then re-check numbers, units, labels, directions, graph scales, circuit polarity, and option text before solving.
- **Course-aware tutoring**: built-in references for:
  - Electrical Engineering
  - Probability and Mathematical Statistics
  - Complex Functions and Integral Transforms
- **Fixed explanation template**: restate the problem, list knowns and unknowns, teach prerequisites, solve step by step, check the result, and summarize the method.
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
Explain this problem and first check whether any image details may have been read incorrectly.
```

```text
Explain this electrical engineering problem clearly and create a review card.
```

```text
Import this probability lecture note and use it as context for future explanations.
```

```text
What should I review today?
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

The script outputs grayscale, enhanced, and optional black/white copies.

### Import Course Material

Import PDF, DOCX, TXT, or Markdown files into generated course references:

```bash
python3 scripts/import_course_material.py ./lecture.pdf \
  --course "Electrical Engineering" \
  --topic "First-order circuits"
```

PDF import requires `pypdf`; DOCX import requires `python-docx`.

### Make Review Card

Create a Markdown review card:

```bash
python3 scripts/make_review_card.py \
  --title "Basic Ohm's Law Problem" \
  --course "Electrical Engineering" \
  --topic "Ohm's Law" \
  --question "Find the current from voltage and resistance" \
  --method "Identify U and R" \
  --method "Use I=U/R" \
  --formula '$I=U/R$' \
  --mistake "Do not read kilo-ohms as ohms" \
  --memory "Check units before applying Ohm's law" \
  --register
```

With `--register`, the generated card is also added to the spaced review queue.

### Study Progress

List due reviews:

```bash
python3 scripts/study_progress.py due
```

Record a review result:

```bash
python3 scripts/study_progress.py review \
  --id "electrical-engineering--basic-ohm-s-law-problem" \
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
