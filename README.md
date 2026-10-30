# Invoice Generator Bot

## Problem
Writing invoices by hand means retyping line items and recalculating totals every time.

## Example output
Generated from `examples/sample_input.csv` (full file: `examples/sample_output.pdf`):

![Sample invoice](docs/sample_output.png)

## What it does
- Reads a CSV with two kinds of rows: `meta` (header fields such as invoice number and client) and `item` (description, quantity, unit price).
- Calculates each line total (quantity x unit price) and the grand total.
- Renders an A4 invoice to `output/invoice.pdf`. Long item lists continue on new pages, with the table header repeated.
- Stops with an error and the CSV line number if a quantity or unit price is missing or not a number; no PDF is written in that case.

## Quick start
Tested with Python 3.11.

```bash
pip install -r requirements.txt
python src/main.py
```

The invoice is written to `output/invoice.pdf` (git-ignored). To use other files:

```bash
python src/main.py --input path/to/invoice.csv --output path/to/invoice.pdf
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

If the file is missing and no `--input` is given, the script recreates it before running.

## Adapting it to your data
Write your own CSV with `meta` and `item` rows, keeping the same four columns, and pass it with `--input`.
Numbers use a dot as decimal separator (`12.50`). The layout has no currency symbol or tax lines.
