"""Reconcile extracted transactions with the source document pack."""

import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

MODEL = "gpt-5.6-luna"
FIELDS = ("id", "sources", "amounts_seen", "included_in_income_statement",
          "amount_used_in_income_statement", "resolution")


def make_client() -> OpenAI:
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
    key = os.getenv("PORTKEY_API_KEY")
    if not key or key.startswith("paste_"):
        raise RuntimeError("Add PORTKEY_API_KEY to the root .env file.")
    return OpenAI(api_key=key, base_url="https://api.portkey.ai/v1",
                  default_headers={"x-portkey-api-key": key})


def read_document(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        return "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
    return path.read_text(encoding="utf-8")


def load_inputs(docs_dir: Path, json_dir: Path) -> dict:
    names = ("receipts.json", "bank_transactions.json", "credit_card_transactions.json")
    extracted = {}
    for name in names:
        path = json_dir / name
        if not path.is_file():
            raise FileNotFoundError(f"Missing extracted input: {path}")
        extracted[name] = json.loads(path.read_text(encoding="utf-8"))
    documents = {}
    for path in sorted(docs_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".pdf", ".txt"}:
            documents[path.name] = read_document(path)
    return {"extracted_transactions": extracted, "source_documents": documents}


def reconcile(client: OpenAI, prompt: str, payload: dict) -> list[dict]:
    response = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(payload, indent=2)},
        ],
    )
    rows = json.loads(response.output_text)
    if not isinstance(rows, list):
        raise ValueError("The model response must be a JSON array.")
    normalized = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("Every reconciliation item must be a JSON object.")
        item = {field: row.get(field) for field in FIELDS}
        if item["included_in_income_statement"] not in {"yes", "no"}:
            raise ValueError("included_in_income_statement must be yes or no")
        if item["included_in_income_statement"] == "no":
            item["amount_used_in_income_statement"] = 0
        normalized.append(item)
    return normalized


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-dir", required=True, type=Path)
    parser.add_argument("--json-dir", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()
    prompt = (Path(__file__).parent / "prompts" / "reconcile.md").read_text(encoding="utf-8")
    rows = reconcile(make_client(), prompt, load_inputs(args.docs_dir, args.json_dir))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "reconciliation_log.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
