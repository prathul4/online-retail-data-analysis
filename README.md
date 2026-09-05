# RetailPulse — Customer Analytics & Revenue Intelligence Platform

An end-to-end retail analytics pipeline built on the Online Retail II dataset
(525K+ UK e-commerce transactions). Raw data is staged and modeled in SQL,
then profiled in Python: RFM customer segmentation via K-Means clustering
(elbow-validated) alongside a rule-based RFM baseline, monthly cohort
retention analysis, and time-series revenue forecasting — delivered as a
reproducible pipeline plus a business-facing insights report.

## What's inside

- **Cleaning**: deduplication, cancelled-invoice removal, negative/zero
  price and quantity handling on ~525K raw transactions.
- **SQL modeling layer**: a local SQLite database built from the cleaned
  data, queried with CTEs and window functions (`NTILE`, `LAG`, `RANK`) for
  RFM scoring, cohort activity, and monthly KPIs — see [`sql/`](sql/).
- **Sales/product/country analysis**: revenue, quantity, and transaction
  breakdowns with charts for every dimension.
- **Customer segmentation, two ways**: a rule-based RFM quintile score, and
  K-Means clustering on standardized RFM features (k chosen via the elbow
  method) — cross-validated against each other.
- **Cohort retention**: true month-over-month retention by first-purchase
  cohort, not just a repeat-vs-one-time split.
- **Revenue forecasting**: Holt-Winters exponential smoothing, backtested
  on a holdout window, with a documented limitation (no yearly seasonal
  term — only ~12 months of history) rather than an inflated accuracy claim.
- **[Business insights report](reports/business_insights_report.md)** and
  an **[exploratory notebook](notebooks/exploratory_analysis.ipynb)** that
  walks through the same pipeline interactively.

## Tech stack

- Python, pandas, NumPy
- scikit-learn (K-Means clustering)
- statsmodels (Holt-Winters forecasting)
- SQLite (SQL modeling layer — CTEs, window functions)
- Matplotlib
- Jupyter Notebook
- Git/GitHub

## Dataset

The dataset used is the Online Retail II dataset (December 2009 – December
2010 sheet). Place it at `data/raw/online_retail_II.xlsx` before running the
pipeline.

### Main Columns

- `Invoice` — Invoice/transaction number
- `StockCode` — Product code
- `Description` — Product description
- `Quantity` — Number of items
- `InvoiceDate` — Transaction date and time
- `Price` — Price per item
- `Customer ID` — Customer identifier
- `Country` — Customer's country

## Project Structure

```text
project2/
│
├── data/
│   ├── raw/
│   │   └── online_retail_II.xlsx
│   └── processed/
│       ├── retail.db                 SQLite database (SQL modeling layer)
│       ├── CSV outputs
│       ├── PNG visualizations
│       └── full_project_output.txt   full pipeline run log
│
├── sql/
│   ├── 01_schema.sql                 staging table + indexes
│   ├── 02_rfm.sql                    RFM scoring (NTILE window functions)
│   ├── 03_cohort_retention.sql       cohort activity counts
│   └── 04_kpis.sql                   monthly KPIs (LAG growth, RANK)
│
├── src/
│   ├── config.py                     paths & constants
│   ├── data_loader.py                raw Excel ingestion
│   ├── cleaning.py                   data quality cleaning
│   ├── database.py                   SQLite build + query runner
│   ├── sales_analysis.py             sales/product/country/order analysis
│   ├── rfm.py                        RFM metrics, rule-based + K-Means segmentation
│   ├── cohort.py                     repeat-customer & cohort retention analysis
│   ├── forecasting.py                revenue forecasting
│   ├── visualize.py                  shared chart helpers
│   └── main.py                       pipeline entry point
│
├── notebooks/
│   └── exploratory_analysis.ipynb    interactive walkthrough
│
├── reports/
│   └── business_insights_report.md   executive summary & recommendations
│
├── venv/
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## How to run

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

# Place the dataset at data/raw/online_retail_II.xlsx, then:
python src/main.py
```

This regenerates every CSV/PNG in `data/processed/`, the SQLite database
(`data/processed/retail.db`), and the run log
(`data/processed/full_project_output.txt`).

To explore interactively:

```bash
jupyter notebook notebooks/exploratory_analysis.ipynb
```

## Objectives

- Load and understand retail transaction data
- Clean missing and duplicate data
- Handle cancelled transactions and unusual prices
- Model cleaned data in a SQL layer (SQLite, window-function queries)
- Calculate sales/revenue and analyze by country, product, and customer
- Segment customers via RFM scoring and K-Means clustering
- Measure true cohort-based customer retention
- Forecast future revenue and report accuracy/limitations honestly
- Create visualizations and a business insights report
