"""Run the extraction, reconciliation, roll-up, and report steps in order."""

import argparse
import subprocess
import sys
from pathlib import Path


def run(args: list[str]) -> None:
    subprocess.run([sys.executable, *args], check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-dir", required=True, type=Path)
    parser.add_argument("--out-dir", default=Path("output"), type=Path)
    args = parser.parse_args()
    out = str(args.out_dir)
    docs = str(args.docs_dir)
    run(["read_receipts.py", "--docs-dir", docs, "--out-dir", out])
    run(["read_bank.py", "--docs-dir", docs, "--out-dir", out])
    run(["read_card.py", "--docs-dir", docs, "--out-dir", out])
    run(["reconcile.py", "--docs-dir", docs, "--json-dir", out, "--out-dir", out])
    run(["income_statement.py", "--json-dir", out, "--out-dir", out])
    run(["report.py", "--json-dir", out, "--out", str(args.out_dir / "income_statement.html")])


if __name__ == "__main__":
    main()
