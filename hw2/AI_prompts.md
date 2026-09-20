# AI Prompts

## Problem 1: Vibe coder prompts

### Prompt I typed

Create the `AI_prompts.md` file for this assignment. Start a section for Problem 1, include the problem title, and record the prompt I used to ask you to create and maintain this log. Keep the wording focused on this problem instead of asking you to complete the whole homework at once.

### Follow-up prompt

No follow-up was needed. The first prompt created the required file and the Problem 1 section with the requested information.

## Problem 2: Seller brief

### Prompt I typed

Choose a smaller B2B company with its own public website that could realistically use an agent to find business customers. Create `assets/seller_brief.md` for Vancord, a cybersecurity and IT services firm at `https://vancord.com/`. Explain why I chose it and list the seller information an agent should collect, including services, ideal customer profile, problems solved, proof points, prospect industry and size, public technology or security signals, likely decision-maker role, personalized reason to reach out, sources, research date, fit score, and disqualification notes. Make the fields useful for finding appropriate business targets and clearly distinguish evidence from assumptions.

### Follow-up prompt

No follow-up was needed. The first prompt produced the seller brief with the company, website, choice rationale, and the requested research fields.

## Problem 3: Agent system prompt

### Prompt I typed

Create `prompts/sales_agent.md` as the system prompt for one PydanticAI sales agent. Add instructions for the profile-building phase: use the seller fields from my Vancord brief, crawl the supplied website and useful same-domain pages, record source URLs and the research date, use only verified website evidence, mark unsupported fields as missing instead of inventing facts, and save valid JSON to `assets/company_profile.json`. Give the agent a careful, practical, evidence-driven personality. The prompt should leave room to add customer-finding and email-drafting instructions later, and it must explicitly prohibit sending emails or taking external actions.

### Follow-up prompt

No follow-up was needed. The first prompt created the reusable system-prompt file with the required profile fields, crawl rules, evidence safeguards, personality, and JSON output path.

## Problem 4: Build agent and run the company profile

### Prompt I typed

Build one PydanticAI agent in `sales_agent.py` that loads `prompts/sales_agent.md`, accepts a query plus a required `--url`, and uses bounded website-crawling and profile-saving tools. Load the Portkey key from the root `.env` without printing it, use `gpt-5.6-luna`, and keep the agent safe and cost-efficient with a small request limit and same-domain page cap. Log every run to `output/audit_log.json` with timestamps, iteration/tool summaries, arguments, results, and the stop event. Then run it on Vancord at `https://vancord.com/` to create `assets/company_profile.json`.

### Follow-up prompt

The first implementation needed a small follow-up: make the system prompt explicitly tell the agent to call `crawl_company_website` for research and `save_company_profile` only after validating the evidence, so the runtime behavior matches the new tools and the saved-file claim is verifiable.

## Problem 5: Expand the prompt and find customers

### Prompt I typed

Extend the existing `prompts/sales_agent.md` without replacing the profile instructions. Add one bounded tool loop for customer research: read `assets/company_profile.json`, search for potential customers using that profile, inspect each candidate's public website, reject competitors and weak or random matches, collect only public contact emails, and draft one personalized outreach email per accepted target. Require evidence and source URLs for every target, make the drafts clearly unsent, save targets to `output/targets.json` and emails to `output/emails.json`, and keep using `output/audit_log.json` with cost and fabrication safeguards.

### Follow-up prompt

The first run needed a follow-up because one candidate site had a certificate error and the initial request cap was too small for three verified targets. Make website inspection record an evidence gap and continue when one site fails, and raise the bounded customer-research cap to 16 model requests while keeping the profile run at 8. Then rerun the exact `--profile` command and validate both output JSON files.

## Problem 6: Agent harness summary

### Prompt I typed

Create the root `HARNESS.md` as a readable manager-level summary of the harness around the sales agent. Compare it to the implementation and document every available tool with its purpose, inputs, and outputs; the profile and customer stopping limits, page cap, target-count completion rule, failure handling, and audit events; and guardrails against invented facts, guessed contacts, competitor or random targets, email sending, unsafe actions, exposed credentials, malformed JSON, and runaway cost.

### Follow-up prompt

No follow-up was needed. The first prompt produced a concise harness summary aligned with the six tools and the current limits in `sales_agent.py`.

## Problem 7: Rank targets and emails

### Prompt I typed

Read `output/targets.json` and `output/emails.json`, then write `output/reflection.md` in my own words. Rank Willington Nameplate, Boston Medical Center Health System, and Mott Corporation from best to worst Vancord target, explaining the fit evidence, contact quality, and any weaknesses. Evaluate each email's tone, personalization, ask, evidence, and readiness for real use. Do not paste agent reasoning; make it a short manager judgment.

### Follow-up prompt

No follow-up was needed. The first prompt created the requested ranking and practical email-quality reflection.
