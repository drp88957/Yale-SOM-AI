# AI Prompt Log

This file records the instructions typed to the vibe coder during the assignment. It is separate from runtime files in `prompts/`.

## Assignment-wide context

The work is for Spoke & Wrench Bicycle Repair, using the supplied document pack to build a January income statement. Every AI call must use the OpenAI API through Portkey, with the root `.env` credential loaded as `PORTKEY_API_KEY`. I will work one problem at a time, use a separate script per problem, keep runtime prompts in `prompts/`, keep generated results in `output/`, and preserve the required `hw1` ZIP layout for the final submission.

## Prompt 1

Create `AI_prompts.md` at the start of the assignment and keep it updated as you work. This file is the log of what you typed to your vibe coder, not the runtime files in `prompts/` that your scripts read.

## Assignment logging requirements

I will maintain one separate section for each of Problems 2–9. Each section will identify the problem number and title, record at least one prompt in my own words, explain in one sentence what was missing after the first prompt when a second prompt was needed, and show evidence that the work was done problem by problem rather than through one assignment-wide prompt.

## Problem 2 — Read receipts

- Prompt typed: Build Problem 2 as a standalone receipt-ingestion workflow for Spoke & Wrench: read only the receipt PDFs from the supplied pack, send each receipt's extracted text to the LLM through `prompts/receipts_extract.md`, preserve unknown values instead of guessing, and write one JSON row per receipt to `output/receipts.json` with the required fields and CLI arguments. Leave statements, leases, quotes, and IOUs for later problems.
- What was lacking after the first prompt: The initial version considered every PDF, so I clarified that Problem 2 must filter to `receipt_*.pdf` and reserve the other document types for later problems.
- Evidence of problem-by-problem work: The supplied pack is unpacked under `pdfs/`, and the Problem 2 implementation is limited to `read_receipts.py`, `prompts/receipts_extract.md`, and the `output/receipts.json` destination; it now selects only the five receipt PDFs.

## Problem 3 — Read bank statement

- Prompt typed: Build Problem 3 as a separate bank-statement workflow: read only `bank_statement_jan2026.pdf`, ask the LLM to identify every statement line and classify it as business or personal with direction, accounting label, and expense subtype, then save the JSON array to `output/bank_transactions.json`.
- What was lacking after the first prompt: No second prompt was needed; the implementation included the required fields, positive amounts, credit/debit direction, and null handling for non-expense rows.
- Evidence of problem-by-problem work: Added only `read_bank.py` and `prompts/bank_extract.md` for this problem, with a separate output file and an explicit check for the bank statement filename.

## Problem 4 — Read credit card statement

- Prompt typed: Build Problem 4 as a separate credit-card workflow: read only `credit_card_jan2026.pdf`, extract every charge, preserve the issuer category, classify each charge as business or personal, assign a shop expense category only to business charges, and save the JSON array to `output/credit_card_transactions.json`.
- What was lacking after the first prompt: No second prompt was needed; the statement text confirmed that the redacted field is the issuer category, so the implementation names it `issuer_category` and preserves it verbatim.
- Evidence of problem-by-problem work: Added only `read_card.py` and `prompts/card_extract.md` for this problem, with a distinct output filename and an explicit check for the credit-card statement.

## Problem 5 — Reconciliation log

- Prompt typed: Build Problem 5 as a separate reconciliation workflow: consume the three JSON outputs from Problems 2–4, read the relevant PDFs and emails from the Spoke & Wrench pack, identify duplicates, mismatches, mixed deposits, personal activity, and unsupported standalone decisions, and produce one auditable row per reconciled amount in `output/reconciliation_log.json`.
- What was lacking after the first prompt: No second prompt was needed; the implementation explicitly validates yes/no inclusion decisions and forces excluded rows to use amount zero.
- Evidence of problem-by-problem work: Added only `reconcile.py` and `prompts/reconcile.md` for this problem; its CLI takes the prior JSON directory separately from the source-document directory and writes a separate reconciliation log.

## Problem 6 — Judgment calls

- Prompt typed: Create `output/judgment_calls.json` by selecting three of the hardest reconciliation decisions from the actual reconciliation log: the mixed $560 Square deposit, the excluded REI charge, and the Park Tool receipt/card mismatch. Use the exact reconciliation IDs and final amounts, include document-name evidence, and provide a confidence level with at least one low-confidence call.
- What was lacking after the first prompt: No second prompt was needed; the three rows cover a mixed business/personal amount, an ambiguous business-versus-personal expense, and a receipt/card amount mismatch.
- Evidence of problem-by-problem work: Created the required hand-authored `output/judgment_calls.json` only after Problems 2–5, with exactly three objects whose IDs match the generated reconciliation log and confidence values high, medium, and low.

## Problem 7 — January income statement

- Prompt typed: Build Problem 7 as a pure-Python roll-up: read `output/reconciliation_log.json`, include only rows marked yes, classify their reconciled amounts into revenue or expense categories from the reconciliation evidence, preserve expense sources, calculate totals and net income for period `2026-01`, and write `output/income_statement_jan2026.json`.
- What was lacking after the first prompt: No second prompt was needed; the script uses reconciliation amounts as its only numeric inputs and excludes every row not marked yes.
- Evidence of problem-by-problem work: Added only `income_statement.py`; it reads the Problem 5 log at runtime and does not hardcode transaction amounts.

## Problem 8 — Income statement webpage

- Prompt typed: Build Problem 8 as a generated one-page HTML report: read the income statement, reconciliation log, and judgment-call JSON files from `output/`, display the January revenue/expense/net-income statement, reconciliation decisions, excluded personal and business rows, and all three judgment calls, then write to the exact `--out` path without hardcoding totals.
- What was lacking after the first prompt: No second prompt was needed; the report reads every displayed number from the JSON files at runtime and escapes text before inserting it into HTML.
- Evidence of problem-by-problem work: Added only `report.py`; its output is generated at `output/income_statement.html` by the required command and uses the Problem 5–7 and Problem 6 artifacts as inputs.

## Problem 9 — Process flow diagram

- Prompt typed: Create a standalone one-page HTML block diagram for the Spoke & Wrench pipeline. Show the document pack, PDFs, emails, every script from Problems 2–8 with what each reads and writes, all JSON/HTML outputs, arrows between stages, and clear LLM markers, especially the path ending at `output/income_statement.html`.
- What was lacking after the first prompt: No second prompt was needed; the diagram includes a legend and a dedicated end-to-end path summary so the document-pack-to-report flow remains clear on small screens.
- Evidence of problem-by-problem work: Created only `output/pipeline.html` for Problem 9; it is a hand-coded HTML artifact and does not add another Python script.

## Problem 10 — Submission format

- Prompt typed: Package the completed Problems 2–9 work as a grader-ready `hw1` folder and `hw1.zip`: include all scripts, runtime prompts, requirements, README, AI prompt log, and sample outputs, while excluding the document pack and API credentials. Add an optional ordered runner and document installation, `.env`, model, and command-line usage.
- What was lacking after the first prompt: No second prompt was needed; the package now has the required README, dependency file, optional runner, and explicit exclusion rules for secrets and source documents.
- Evidence of problem-by-problem work: Problem 10 adds only packaging artifacts (`README.md`, `requirements.txt`, `run_all.py`, and the final ZIP); earlier problem scripts, prompts, and outputs remain separate and traceable.
