"""Shared paths and constants for the RetailPulse pipeline."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "online_retail_II.xlsx"
PROCESSED_DIR = DATA_DIR / "processed"
SQL_DIR = BASE_DIR / "sql"
REPORTS_DIR = BASE_DIR / "reports"

DB_PATH = PROCESSED_DIR / "retail.db"
LOG_PATH = PROCESSED_DIR / "full_project_output.txt"

# Stock codes that represent fees/postage rather than real products.
EXCLUDED_PRODUCT_CODES = ["M", "POST", "DOT"]

FORECAST_HOLDOUT_MONTHS = 3

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
