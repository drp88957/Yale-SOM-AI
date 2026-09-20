# Sales Agent Harness

This document summarizes the controls around the `gpt-5.6-luna` PydanticAI agent. The agent receives the human's plain-language query, while the harness supplies narrowly scoped tools and validates saved outputs.

## Tools

| Tool | What it does | Inputs | Output |
|---|---|---|---|
| `crawl_company_website` | Fetches a small set of public pages from the supplied seller domain and extracts visible text. | Up to six relative or same-domain paths. | JSON list containing each URL, extracted page text, or a fetch error. |
| `save_company_profile` | Validates that a profile is a JSON object with a company name and writes it to the approved profile location. | Profile JSON string. | Confirmation of the saved file, or a validation error. |
| `read_company_profile` | Reads the previously generated seller profile. It only permits the approved profile path. | `assets/company_profile.json`. | The profile as JSON text. |
| `search_customer_candidates` | Uses Portkey's web search capability to find possible customer organizations. It does not contact them. | A focused search query. | Public search-result text. |
| `inspect_customer_website` | Fetches one public candidate website, extracts visible text, and finds email-shaped addresses exposed on that page. | An HTTP or HTTPS URL. | JSON containing URL, page text, public emails, or an error summary. |
| `save_targets_and_emails` | Writes the selected companies and outreach drafts to separate output files. | Two JSON arrays: targets and emails. | Confirmation with counts. Every email must have `send_status: "draft_only"`. |

## Stopping rules

- The profile mode is limited to 8 model requests; customer mode is limited to 16 model requests.
- Seller crawling is capped at six pages per tool call and stays on the supplied domain.
- The agent stops after it has saved the requested number of qualified targets and matching drafts. For Problem 5, that means 3 targets and 3 drafts.
- A candidate is not accepted without website inspection and evidence of a credible fit with the seller profile. A missing public email is recorded as `null`, not fabricated.
- A failed candidate-site fetch is recorded as an error/evidence gap so the loop can continue; other tool or model failures end the run and are written to `output/audit_log.json`.
- Every run writes a start event, numbered tool-call iterations with concise action summaries (not private chain-of-thought), tool-call/result summaries, and a final completed or failed event to `output/audit_log.json`.

## Guardrails

- The agent must use verified public website/search evidence and source URLs. It must not invent company facts, capabilities, contacts, emails, certifications, or outcomes.
- The seller profile is read through the approved path, and profile output is saved only to `assets/company_profile.json`.
- Target and email outputs are saved only to `output/targets.json` and `output/emails.json`.
- Emails are drafts only. The harness never provides a send, submit, login, purchase, or messaging tool, and saved drafts must be marked `draft_only`.
- Candidate research is limited to public websites and public business email addresses. The agent must not guess private contact details or use a random competitor, directory listing, or famous company merely because it has a website.
- The Portkey credential is loaded from the root `.env` as `PORTKEY_API_KEY`; it is never included in prompts, output, audit data, or printed logs.
- Usage limits, page caps, request timeouts, same-domain checks for seller crawling, and structured JSON validation prevent runaway calls and malformed evidence files.
- The agent must not take unsafe, illegal, deceptive, destructive, or irreversible actions.
