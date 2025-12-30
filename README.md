# Invoice Generator Bot (PDF)

Simple invoice generator that reads structured CSV data and renders a clean invoice PDF using `reportlab`.

## What it does
- Reads `examples/sample_input.csv` describing invoice metadata and line items.
- Parses items with quantity and unit price.
- Calculates line totals and overall total.
- Renders a one-page invoice to `examples/sample_output.pdf`.

## How to run (DEMO)
```bash
cd invoice-generator-bot
python src/main.py
```

A demo `sample_input.csv` will be created on first run.

## Inputs & outputs
- **Input:** `examples/sample_input.csv` (tagged `meta` and `item` rows).
- **Output:** `examples/sample_output.pdf` (generated invoice).

## Dependencies
- Python 3.x
- `reportlab` (install with `pip install reportlab`).
