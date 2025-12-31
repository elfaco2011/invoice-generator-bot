# Automated Invoice Generation Bot

## 🔍 Problem
Creating invoices manually is time-consuming and prone to errors, especially when handling multiple clients or recurring billing.

## ✅ Solution
This Python automation bot generates structured invoices automatically from input data, reducing manual work and improving billing accuracy.

## 🚀 Features
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

## 🎯 Use Cases
- Freelancer invoicing
- Small business billing
- Automated recurring invoices

## 📦 Ready-made Automation Pack
Looking for a plug-and-play invoicing solution?
👉 https://khalidelfakir.gumroad.com

