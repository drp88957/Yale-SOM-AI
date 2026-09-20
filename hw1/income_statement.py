"""Roll the reconciliation log into a January income statement."""

import argparse
import json
from collections import defaultdict
from pathlib import Path


def row_text(row: dict) -> str:
    return " ".join(str(row.get(key, "")) for key in ("id", "resolution", "sources")).lower()


def category_for(row: dict) -> tuple[str, str]:
    text = row_text(row)
    if any(word in text for word in ("revenue", "deposit", "payment", "sales", "service")):
        return "revenue", "revenue"
    if any(word in text for word in ("rent", "crown street")):
        return "expense", "rent"
    if any(word in text for word in ("electric", "eversource", "utilities", "comcast", "internet")):
        return "expense", "utilities"
    if any(word in text for word in ("insurance", "state farm", "liability")):
        return "expense", "insurance"
    if any(word in text for word in ("courier", "shipping", "delivery")):
        return "expense", "shipping"
    if any(word in text for word in ("parts", "bike parts", "cogs", "tubes", "chain", "restock")):
        return "expense", "cogs_parts"
    if any(word in text for word in ("tool", "equipment", "repair stand")):
        return "expense", "tools_equipment"
    if any(word in text for word in ("home depot", "bins", "broom", "supplies")):
        return "expense", "supplies"
    if any(word in text for word in ("jacket", "rei", "outerwear")):
        return "expense", "workwear"
    if any(word in text for word in ("fee", "service fee")):
        return "expense", "bank_fees"
    return "expense", "other"


def build_statement(rows: list[dict]) -> dict:
    revenue = 0.0
    expenses = defaultdict(float)
    expense_sources = defaultdict(set)
    for row in rows:
        if row.get("included_in_income_statement") != "yes":
            continue
        amount = float(row.get("amount_used_in_income_statement") or 0)
        kind, category = category_for(row)
        if kind == "revenue":
            revenue += amount
        else:
            expenses[category] += amount
            expense_sources[category].update(row.get("sources") or [])
    expense_lines = [
        {"label": category, "amount_usd": round(amount, 2), "category": category,
         "sources": sorted(expense_sources[category])}
        for category, amount in sorted(expenses.items())
    ]
    total = round(sum(line["amount_usd"] for line in expense_lines), 2)
    revenue = round(revenue, 2)
    return {"period": "2026-01", "revenue_usd": revenue, "expense_lines": expense_lines,
            "total_expenses_usd": total, "net_income_usd": round(revenue - total, 2)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-dir", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()
    rows = json.loads((args.json_dir / "reconciliation_log.json").read_text(encoding="utf-8"))
    statement = build_statement(rows)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "income_statement_jan2026.json").write_text(json.dumps(statement, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
