# Online Retail Data Analysis

## Project Overview

This project analyzes the Online Retail II dataset using Python and pandas.

The main goal is to clean retail transaction data, analyze sales and customer behavior, perform RFM customer analysis, segment customers, and generate useful visualizations and business insights.

## Objectives

- Load and understand retail transaction data
- Clean missing and duplicate data
- Handle cancelled transactions and unusual prices
- Calculate sales/revenue
- Analyze sales by country
- Analyze products and customers
- Perform RFM analysis
- Segment customers based on their behavior
- Create visualizations
- Save analysis results as CSV and PNG files

## Dataset

The dataset used is the Online Retail II dataset.

### Main Columns

- `Invoice` — Invoice/transaction number
- `StockCode` — Product code
- `Description` — Product description
- `Quantity` — Number of items
- `InvoiceDate` — Transaction date and time
- `Price` — Price per item
- `Customer ID` — Customer identifier
- `Country` — Customer's country

## Technologies Used

- Python
- pandas
- NumPy
- Matplotlib
- Jupyter Notebook
- VS Code
- Git/GitHub

## Project Structure

```text
project2/
│
├── data/
│   ├── raw/
│   │   └── online_retail_II.xlsx
│   └── processed/
│       ├── CSV outputs
│       ├── PNG visualizations
│       └── full_project_output.txt
│
├── notebooks/
├── reports/
├── sql/
├── src/
│   └── main.py
│
├── venv/
├── .gitignore
├── README.md
└── requirements.txt