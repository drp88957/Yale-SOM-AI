# Spoke & Wrench Bicycle Repair — HW1

This project processes the January 2026 records for Spoke & Wrench Bicycle Repair into a reconciled income statement and HTML report.

## Setup

Create a local `.env` file in the project root (do not commit or zip it):

```text
PORTKEY_API_KEY=your_portkey_key_here
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

The scripts use the OpenAI Python SDK through Portkey and the model `gpt-5.6-luna`. The supplied document pack is intentionally not included in the submission ZIP; provide its unpacked path as `--docs-dir`.

## Run the pipeline

From this folder, with the document pack unpacked at `PATH`:

```bash
python read_receipts.py --docs-dir PATH/pdfs --out-dir output
python read_bank.py --docs-dir PATH/pdfs --out-dir output
python read_card.py --docs-dir PATH/pdfs --out-dir output
python reconcile.py --docs-dir PATH --json-dir output --out-dir output
python income_statement.py --json-dir output --out-dir output
python report.py --json-dir output --out output/income_statement.html
```

Problem 6 is the hand-authored `output/judgment_calls.json`. Problem 9 is the hand-authored `output/pipeline.html`. The optional `run_all.py` runs Problems 2–5, then the Python roll-up and report.

## Outputs

The `output/` folder contains the JSON artifacts from a successful run, the income statement webpage, and the pipeline diagram. `AI_prompts.md` records the problem-by-problem prompts used during development; runtime prompts are kept separately in `prompts/`.
