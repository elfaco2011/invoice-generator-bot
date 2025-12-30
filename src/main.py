from __future__ import annotations

import csv
import logging
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

HERE = Path(__file__).resolve().parent
EXAMPLES_DIR = HERE.parent / "examples"
INPUT_PATH = EXAMPLES_DIR / "sample_input.csv"
OUTPUT_PATH = EXAMPLES_DIR / "sample_output.pdf"

logging.basicConfig(
    level=logging.INFO,
    format="[InvoiceGenerator] %(levelname)s - %(message)s",
)


def _ensure_demo_input() -> None:
    if INPUT_PATH.exists():
        return
    EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    with INPUT_PATH.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["type", "col1", "col2", "col3"])  # simple tagged rows
        writer.writerow(["meta", "Invoice #", "INV-001", " "])
        writer.writerow(["meta", "Client", "Acme Corp", " "])
        writer.writerow(["item", "Consulting", "10", "150"])  # qty, unit price
        writer.writerow(["item", "Design", "5", "100"])


def _load_data():
    meta = {}
    items = []
    with INPUT_PATH.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("type") == "meta":
                meta[row.get("col1", "")] = row.get("col2", "")
            elif row.get("type") == "item":
                try:
                    qty = float(row.get("col2", "0") or 0)
                    price = float(row.get("col3", "0") or 0)
                except ValueError:
                    qty, price = 0.0, 0.0
                items.append((row.get("col1", ""), qty, price))
    return meta, items


def _render_pdf(meta, items) -> None:
    c = canvas.Canvas(str(OUTPUT_PATH), pagesize=A4)
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
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20 * mm, y, "Description")
    c.drawString(90 * mm, y, "Qty")
    c.drawString(110 * mm, y, "Unit")
    c.drawString(140 * mm, y, "Total")

    c.setFont("Helvetica", 10)
    total = 0.0
    for desc, qty, price in items:
        y -= 6 * mm
        line_total = qty * price
        total += line_total
        c.drawString(20 * mm, y, desc)
        c.drawRightString(100 * mm, y, f"{qty:g}")
        c.drawRightString(125 * mm, y, f"{price:.2f}")
        c.drawRightString(190 * mm, y, f"{line_total:.2f}")

    y -= 10 * mm
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(190 * mm, y, f"TOTAL: {total:.2f}")

    c.showPage()
    c.save()


def run() -> None:
    _ensure_demo_input()
    meta, items = _load_data()
    if not items:
        logging.warning("No invoice items found, aborting.")
        return
    _render_pdf(meta, items)
    logging.info("Invoice PDF generated at %s", OUTPUT_PATH)


if __name__ == "__main__":
    run()
