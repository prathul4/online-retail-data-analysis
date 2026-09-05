-- RetailPulse: staging schema for cleaned transactions.
-- Populated from the Python cleaning stage (src/cleaning.py) via
-- src/database.py, which loads a pandas DataFrame into this table.

DROP TABLE IF EXISTS transactions_clean;

CREATE TABLE transactions_clean (
    Invoice     TEXT,
    StockCode   TEXT,
    Description TEXT,
    Quantity    INTEGER,
    InvoiceDate TEXT,
    Price       REAL,
    CustomerID  TEXT,
    Country     TEXT,
    Revenue     REAL,
    YearMonth   TEXT
);

CREATE INDEX idx_transactions_customer ON transactions_clean (CustomerID);
CREATE INDEX idx_transactions_month ON transactions_clean (YearMonth);
CREATE INDEX idx_transactions_country ON transactions_clean (Country);
