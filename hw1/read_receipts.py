"""Extract one structured purchase row from each receipt PDF."""

import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

MODEL = "gpt-5.6-luna"
REQUIRED_FIELDS = ("vendor", "date", "description", "amount_usd", "category", "source_file")


def make_client() -> OpenAI:
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
    key = os.getenv("PORTKEY_API_KEY")
    if not key or key.startswith("paste_"):
        raise RuntimeError("Add PORTKEY_API_KEY to the root .env file.")
    return OpenAI(api_key=key, base_url="https://api.portkey.ai/v1",
                  default_headers={"x-portkey-api-key": key})


def extract_text(pdf_path: Path) -> str:
    return "\n".join(page.extract_text() or "" for page in PdfReader(str(pdf_path)).pages)


def extract_row(client: OpenAI, prompt: str, filename: str, receipt_text: str) -> dict:
    response = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"source filename: {filename}\n\nreceipt text:\n{receipt_text}"},
        ],
    )
    row = json.loads(response.output_text)
    row["source_file"] = filename
    missing = row.get("fields_not_found", [])
    row["fields_not_found"] = missing if isinstance(missing, list) else [str(missing)]
    for field in REQUIRED_FIELDS:
        row.setdefault(field, None)
        if row[field] is None and field not in row["fields_not_found"]:
            row["fields_not_found"].append(field)
    return {**{field: row[field] for field in REQUIRED_FIELDS}, "fields_not_found": row["fields_not_found"]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-dir", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()
    prompt_path = Path(__file__).parent / "prompts" / "receipts_extract.md"
    client = make_client()
    prompt = prompt_path.read_text(encoding="utf-8")
    # Problem 2 covers receipt PDFs only; statements, leases, quotes, and IOUs
    # are inputs for later problems.
    receipt_pdfs = sorted(args.docs_dir.glob("receipt_*.pdf"))
    rows = [extract_row(client, prompt, pdf.name, extract_text(pdf)) for pdf in receipt_pdfs]
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "receipts.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
