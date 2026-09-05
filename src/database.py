"""SQLite modeling layer: loads cleaned transactions into a local database
and runs the analytical SQL queries in sql/ against it.
"""

import sqlite3

import pandas as pd

from src import config

EXPORT_COLUMNS = [
    "Invoice", "StockCode", "Description", "Quantity", "InvoiceDate",
    "Price", "Customer ID", "Country", "Revenue", "YearMonth",
]


def build_database(df):
    """Create the SQLite schema (sql/01_schema.sql) and load clean transactions."""
    conn = sqlite3.connect(config.DB_PATH)
    try:
        schema_sql = (config.SQL_DIR / "01_schema.sql").read_text(encoding="utf-8")
        conn.executescript(schema_sql)

        export_df = df[EXPORT_COLUMNS].copy()
        export_df["InvoiceDate"] = export_df["InvoiceDate"].astype(str)
        export_df["YearMonth"] = export_df["YearMonth"].astype(str)
        export_df = export_df.rename(columns={"Customer ID": "CustomerID"})
        export_df["CustomerID"] = export_df["CustomerID"].astype("Int64").astype(str)
        export_df.loc[export_df["CustomerID"] == "<NA>", "CustomerID"] = None

        export_df.to_sql("transactions_clean", conn, if_exists="append", index=False)
        conn.commit()
    finally:
        conn.close()


def run_sql_file(filename):
    """Execute a .sql file (single query) and return the result as a DataFrame."""
    conn = sqlite3.connect(config.DB_PATH)
    try:
        sql = (config.SQL_DIR / filename).read_text(encoding="utf-8")
        return pd.read_sql_query(sql, conn)
    finally:
        conn.close()
