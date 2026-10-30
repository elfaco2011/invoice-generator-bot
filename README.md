# Invoice Generator Bot

## Problem
Writing invoices by hand means retyping line items and recalculating totals every time.

## Example output
Generated from `examples/sample_input.csv` (full file: `examples/sample_output.pdf`):

![Sample invoice](docs/sample_output.png)

## What it does
- Reads a CSV with two kinds of rows: `meta` (header fields such as invoice number and client) and `item` (description, quantity, unit price).
- Calculates each line total (quantity x unit price) and the grand total.
- Renders a one-page A4 invoice to `examples/sample_output.pdf`.

## Quick start
Tested with Python 3.11.

```bash
pip install -r requirements.txt
python src/main.py
```

## Sample data
`examples/sample_input.csv`:

```text
type,col1,col2,col3
meta,Invoice #,INV-001,
meta,Client,Acme Corp,
item,Consulting,10,150
item,Design,5,100
```

- `meta` rows: `col1` is the label, `col2` the value. Each one is printed as `label: value` under the title.
- `item` rows: `col1` description, `col2` quantity, `col3` unit price.

If the file is missing, the script recreates it before running.

## Adapting it to your data
Replace `examples/sample_input.csv` with your own `meta` and `item` rows, keeping the same four columns.
The layout is a single page with no currency symbol or tax lines; long item lists do not continue on a second page.
