"""Extract January credit-card charges into JSON."""

import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

MODEL = "gpt-5.6-luna"
FIELDS = ("date", "merchant", "issuer_category", "amount_usd", "classification", "expense_category")


def make_client() -> OpenAI:
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
    key = os.getenv("PORTKEY_API_KEY")
    if not key or key.startswith("paste_"):
        raise RuntimeError("Add PORTKEY_API_KEY to the root .env file.")
    return OpenAI(api_key=key, base_url="https://api.portkey.ai/v1",
                  default_headers={"x-portkey-api-key": key})


def pdf_text(path: Path) -> str:
    return "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)


def extract_rows(client: OpenAI, prompt: str, statement_text: str) -> list[dict]:
    response = client.responses.create(
        model=MODEL,
        input=[{"role": "system", "content": prompt}, {"role": "user", "content": statement_text}],
    )
    rows = json.loads(response.output_text)
    if not isinstance(rows, list):
        raise ValueError("The model response must be a JSON array.")
    return [{field: row.get(field) for field in FIELDS} for row in rows]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-dir", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()
    statement = args.docs_dir / "credit_card_jan2026.pdf"
    if not statement.is_file():
        raise FileNotFoundError(f"Missing credit-card statement: {statement}")
    prompt = (Path(__file__).parent / "prompts" / "card_extract.md").read_text(encoding="utf-8")
    rows = extract_rows(make_client(), prompt, pdf_text(statement))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "credit_card_transactions.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
