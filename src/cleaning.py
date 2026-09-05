"""Data quality cleaning for the raw Online Retail II transactions.

Removes exact duplicates, cancelled invoices, and invalid negative-value
records, then derives the Revenue and YearMonth columns used throughout
the rest of the pipeline.
"""

from src import config


def clean_transactions(df):
    """Clean raw transactions and return (clean_df, cleaning_log)."""
    log = {"raw_shape": df.shape}

    df = df.drop_duplicates()
    log["duplicates_removed"] = log["raw_shape"][0] - df.shape[0]

    is_cancelled = df["Invoice"].astype(str).str.startswith("C")
    log["cancelled_transactions_removed"] = int(is_cancelled.sum())
    df = df[~is_cancelled].copy()

    negative_quantity = df["Quantity"] < 0
    log["negative_quantity_removed"] = int(negative_quantity.sum())
    df = df[~negative_quantity].copy()

    negative_price = df["Price"] < 0
    log["negative_price_removed"] = int(negative_price.sum())
    df = df[~negative_price].copy()

    log["zero_price_transactions"] = int((df["Price"] == 0).sum())
    log["missing_customer_id"] = int(df["Customer ID"].isna().sum())
    log["missing_description"] = int(df["Description"].isna().sum())
    log["clean_shape"] = df.shape

    df["Revenue"] = df["Quantity"] * df["Price"]
    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M")

    return df, log


def build_product_df(df):
    """Transactions with fee/postage stock codes (M, POST, DOT) excluded."""
    return df[~df["StockCode"].isin(config.EXCLUDED_PRODUCT_CODES)].copy()
