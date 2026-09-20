"""Build a human-readable HTML report from the generated JSON outputs."""

import argparse
import html
import json
from pathlib import Path


def load(directory: Path, name: str):
    return json.loads((directory / name).read_text(encoding="utf-8"))


def money(value) -> str:
    return f"${float(value or 0):,.2f}"


def row_cells(values) -> str:
    return "".join(f"<td>{html.escape(str(value if value is not None else '—'))}</td>" for value in values)


def build(directory: Path) -> str:
    statement = load(directory, "income_statement_jan2026.json")
    reconciliation = load(directory, "reconciliation_log.json")
    judgments = load(directory, "judgment_calls.json")
    excluded = [row for row in reconciliation if row.get("included_in_income_statement") == "no"]
    expense_rows = "".join(
        f"<tr>{row_cells((line['label'], money(line['amount_usd']), ', '.join(line.get('sources', []))))}</tr>"
        for line in statement.get("expense_lines", [])
    )
    excluded_rows = "".join(
        f"<tr>{row_cells((row.get('id'), money(row.get('amount_used_in_income_statement')), row.get('resolution')))}</tr>"
        for row in excluded
    ) or '<tr><td colspan="3">No excluded reconciliation rows.</td></tr>'
    reconciliation_rows = "".join(
        f"<article class='decision'><h3>{html.escape(str(row.get('id')))}</h3>"
        f"<p>{html.escape(str(row.get('resolution')))}</p></article>"
        for row in reconciliation
    )
    judgment_cards = "".join(
        f"<article class='judgment'><h3>{html.escape(str(row.get('transaction_id')))}</h3>"
        f"<p><b>Booked:</b> {html.escape(str(row.get('included_in_income_statement')))} · {money(row.get('amount_used_in_income_statement'))}</p>"
        f"<p><b>Confidence:</b> {html.escape(str(row.get('confidence')))}</p>"
        f"<ul>{''.join('<li>' + html.escape(str(source)) + '</li>' for source in row.get('evidence_for', []))}</ul></article>"
        for row in judgments
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Spoke &amp; Wrench · January 2026</title>
<style>
body{{margin:0;background:#0d0b10;color:#f8eff5;font:16px system-ui,sans-serif}}main{{max-width:1000px;margin:auto;padding:42px 22px}}h1{{color:#ff4fa3}}h2{{border-bottom:1px solid #47263b;padding-bottom:10px}}.hero,.card,.decision,.judgment{{background:#17121a;border:1px solid #3d2639;border-radius:14px;padding:20px;margin:14px 0}}.metrics{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}.metric strong{{display:block;font-size:1.7rem;color:#ff8bc5}}table{{border-collapse:collapse;width:100%}}th,td{{border-bottom:1px solid #352432;padding:12px;text-align:left;vertical-align:top}}th{{color:#ff8bc5}}.net{{font-size:1.5rem;color:#ff8bc5}}@media(max-width:650px){{.metrics{{grid-template-columns:1fr}}}}
</style></head><body><main>
<div class="hero"><h1>January Income Statement</h1><p>Spoke &amp; Wrench Bicycle Repair · period {html.escape(statement.get('period', '2026-01'))}</p>
<div class="metrics"><div class="metric">Revenue<strong>{money(statement.get('revenue_usd'))}</strong></div><div class="metric">Expenses<strong>{money(statement.get('total_expenses_usd'))}</strong></div><div class="metric">Net income<strong>{money(statement.get('net_income_usd'))}</strong></div></div></div>
<section class="card"><h2>Expense lines</h2><table><tr><th>Label</th><th>Amount</th><th>Sources</th></tr>{expense_rows}</table></section>
<section class="card"><h2>Excluded personal and business rows</h2><table><tr><th>Reconciliation ID</th><th>Booked amount</th><th>Reason</th></tr>{excluded_rows}</table></section>
<section><h2>Reconciliation decisions</h2>{reconciliation_rows}</section>
<section><h2>Three judgment calls</h2>{judgment_cards}</section>
</main></body></html>"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-dir", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(build(args.json_dir), encoding="utf-8")


if __name__ == "__main__":
    main()
