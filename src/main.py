from __future__ import annotations

import argparse
import csv
import logging
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

HERE = Path(__file__).resolve().parent
ROOT_DIR = HERE.parent
EXAMPLES_DIR = ROOT_DIR / "examples"
DEFAULT_INPUT = EXAMPLES_DIR / "sample_input.csv"
DEFAULT_OUTPUT = ROOT_DIR / "output" / "invoice.pdf"
BOTTOM_MARGIN = 20 * mm

logging.basicConfig(
    level=logging.INFO,
    format="[InvoiceGenerator] %(levelname)s - %(message)s",
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a PDF invoice from a CSV file.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT,
                        help="input CSV (default: examples/sample_input.csv)")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                        help="output PDF (default: output/invoice.pdf)")
    return parser.parse_args()


def _ensure_demo_input() -> None:
    if DEFAULT_INPUT.exists():
        return
    EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    with DEFAULT_INPUT.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["type", "col1", "col2", "col3"])  # simple tagged rows
        writer.writerow(["meta", "Invoice #", "INV-001", " "])
        writer.writerow(["meta", "Client", "Acme Corp", " "])
        writer.writerow(["item", "Consulting", "10", "150"])  # qty, unit price
        writer.writerow(["item", "Design", "5", "100"])


class InvalidInputError(Exception):
    pass


def _parse_number(value, field: str, line: int, desc: str) -> float:
    try:
        return float((value or "").strip())
    except ValueError:
        raise InvalidInputError(
            f"line {line}: {field} {value!r} for item {desc!r} is not a number"
        ) from None


def _load_data(input_path: Path):
    meta = {}
    items = []
    with input_path.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("type") == "meta":
                meta[row.get("col1", "")] = row.get("col2", "")
            elif row.get("type") == "item":
                desc = row.get("col1", "")
                qty = _parse_number(row.get("col2"), "quantity", reader.line_num, desc)
                price = _parse_number(row.get("col3"), "unit price", reader.line_num, desc)
                items.append((desc, qty, price))
    return meta, items


def _draw_table_header(c, y) -> None:
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20 * mm, y, "Description")
    c.drawRightString(100 * mm, y, "Qty")
    c.drawRightString(125 * mm, y, "Unit")
    c.drawRightString(190 * mm, y, "Total")
    c.setFont("Helvetica", 10)


def _render_pdf(meta, items, output_path: Path) -> None:
    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4

    y = height - 30 * mm
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20 * mm, y, "INVOICE")

    y -= 10 * mm
    c.setFont("Helvetica", 10)
    for k, v in meta.items():
        c.drawString(20 * mm, y, f"{k}: {v}")
        y -= 6 * mm

    y -= 6 * mm
    _draw_table_header(c, y)

    total = 0.0
    for desc, qty, price in items:
        y -= 6 * mm
        if y < BOTTOM_MARGIN:
            c.showPage()
            y = height - 20 * mm
            _draw_table_header(c, y)
            y -= 6 * mm
        line_total = qty * price
        total += line_total
        c.drawString(20 * mm, y, desc)
        c.drawRightString(100 * mm, y, f"{qty:g}")
        c.drawRightString(125 * mm, y, f"{price:.2f}")
        c.drawRightString(190 * mm, y, f"{line_total:.2f}")

    y -= 10 * mm
    if y < BOTTOM_MARGIN:
        c.showPage()
        y = height - 20 * mm
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(190 * mm, y, f"TOTAL: {total:.2f}")

    c.showPage()
    c.save()


def run() -> None:
    args = _parse_args()
    if args.input == DEFAULT_INPUT:
        _ensure_demo_input()
    if not args.input.exists():
        logging.error("Input file not found: %s", args.input)
        sys.exit(1)
    try:
        meta, items = _load_data(args.input)
    except InvalidInputError as e:
        logging.error("Invalid input in %s, %s. No invoice generated.", args.input, e)
        sys.exit(1)
    if not items:
        logging.warning("No invoice items found, aborting.")
        return
    args.output.parent.mkdir(parents=True, exist_ok=True)
    _render_pdf(meta, items, args.output)
    logging.info("Invoice PDF generated at %s", args.output)


if __name__ == "__main__":
    run()
