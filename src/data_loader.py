"""Raw data ingestion for the RetailPulse pipeline."""

import pandas as pd

from src import config

REQUIRED_COLUMNS = [
    "Invoice",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "Price",
    "Customer ID",
    "Country",
]


def load_raw_data(path=None):
    """Load the raw Online Retail II transactions from Excel."""
    path = path or config.RAW_DATA_PATH
    df = pd.read_excel(path)

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Raw dataset is missing expected columns: {missing}")

    return df
