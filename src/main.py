import sys
import pandas as pd

# Save all output to a text file
# Save all output to a text file
sys.stdout = open(
    "data/processed/full_project_output.txt",
    "w",
    encoding="utf-8"
)

print("=" * 70)
print("PROJECT 2 - ONLINE RETAIL DATA ANALYSIS")
print("=" * 70)


# ============================================================
# STEP 1 - LOAD DATASET
# ============================================================

print("\n" + "=" * 60)
print("STEP 1 - LOAD DATASET")
print("=" * 60)

df = pd.read_excel(
    "data/raw/online_retail_II.xlsx"
)

print("\nDataset loaded successfully.")


# ============================================================
# STEP 2 - DISPLAY FIRST 5 ROWS
# ============================================================

print("\n" + "=" * 60)
print("STEP 2 - FIRST 5 ROWS")
print("=" * 60)

print(df.head())


# ============================================================
# STEP 3 - DATASET SHAPE
# ============================================================

print("\n" + "=" * 60)
print("STEP 3 - DATASET SHAPE")
print("=" * 60)

print(df.shape)


# ============================================================
# STEP 4 - COLUMN NAMES
# ============================================================

print("\n" + "=" * 60)
print("STEP 4 - COLUMN NAMES")
print("=" * 60)

print(df.columns.tolist())


# ============================================================
# STEP 5 - DATA TYPES
# ============================================================

print("\n" + "=" * 60)
print("STEP 5 - DATA TYPES")
print("=" * 60)

print(df.dtypes)


# ============================================================
# STEP 6 - MISSING VALUES
# ============================================================

print("\n" + "=" * 60)
print("STEP 6 - MISSING VALUES")
print("=" * 60)

print(df.isnull().sum())


# ============================================================
# STEP 7 - DUPLICATE ROWS
# ============================================================

print("\n" + "=" * 60)
print("STEP 7 - DUPLICATE ROWS")
print("=" * 60)

print("Duplicate rows:")
print(df.duplicated().sum())


# ============================================================
# STEP 8 - BASIC STATISTICS
# ============================================================

print("\n" + "=" * 60)
print("STEP 8 - BASIC STATISTICS")
print("=" * 60)

print(df.describe())


# ============================================================
# STEP 9 - REMOVE DUPLICATE ROWS
# ============================================================

print("\n" + "=" * 60)
print("STEP 9 - REMOVE DUPLICATE ROWS")
print("=" * 60)

df = df.drop_duplicates()

print("\nShape after removing duplicates:")
print(df.shape)

print("\nRemaining duplicate rows:")
print(df.duplicated().sum())


# ============================================================
# STEP 10 - NEGATIVE QUANTITY ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 10 - NEGATIVE QUANTITY ANALYSIS")
print("=" * 60)

negative_quantity = df[
    df["Quantity"] < 0
]

print("\nNegative quantity rows:")
print(negative_quantity.shape)

print("\nFirst 5 negative quantity rows:")
print(negative_quantity.head())


# ============================================================
# STEP 11 - ZERO QUANTITY ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 11 - ZERO QUANTITY ANALYSIS")
print("=" * 60)

zero_quantity = df[
    df["Quantity"] == 0
]

print("\nZero quantity rows:")
print(zero_quantity.shape)

print("\nSample zero quantity rows:")
print(zero_quantity.head())


# ============================================================
# STEP 12 - NEGATIVE PRICE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 12 - NEGATIVE PRICE ANALYSIS")
print("=" * 60)

negative_price = df[
    df["Price"] < 0
]

print("\nNegative price rows:")
print(negative_price.shape)

print("\nNegative price records:")
print(negative_price)


# ============================================================
# STEP 13 - ZERO PRICE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 13 - ZERO PRICE ANALYSIS")
print("=" * 60)

zero_price = df[
    df["Price"] == 0
]

print("\nZero price rows:")
print(zero_price.shape)

print("\nSample zero price rows:")
print(zero_price.head())


# ============================================================
# STEP 14 - CANCELLED INVOICE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 14 - CANCELLED INVOICE ANALYSIS")
print("=" * 60)

cancelled = df[
    df["Invoice"].astype(str).str.startswith("C")
]

print("\nCancelled transactions:")
print(cancelled.shape)

print("\nSample cancelled transactions:")
print(cancelled.head())


# ============================================================
# STEP 15 - CANCELLED VS NEGATIVE QUANTITY
# ============================================================

print("\n" + "=" * 60)
print("STEP 15 - CANCELLED VS NEGATIVE QUANTITY")
print("=" * 60)

cancelled_negative = cancelled[
    cancelled["Quantity"] < 0
]

cancelled_positive = cancelled[
    cancelled["Quantity"] > 0
]

print("\nCancelled transactions with negative quantity:")
print(cancelled_negative.shape)

print("\nCancelled transactions with positive quantity:")
print(cancelled_positive.shape)


# ============================================================
# STEP 16 - REMOVE CANCELLED TRANSACTIONS
# ============================================================

print("\n" + "=" * 60)
print("STEP 16 - REMOVE CANCELLED TRANSACTIONS")
print("=" * 60)

df = df[
    ~df["Invoice"].astype(str).str.startswith("C")
]

print("\nShape after removing cancelled transactions:")
print(df.shape)

print("\nRemaining cancelled transactions:")
print(
    df["Invoice"]
    .astype(str)
    .str.startswith("C")
    .sum()
)


# ============================================================
# STEP 17 - CHECK CUSTOMER ID
# ============================================================

print("\n" + "=" * 60)
print("STEP 17 - CUSTOMER ID ANALYSIS")
print("=" * 60)

print("\nMissing Customer IDs:")
print(df["Customer ID"].isna().sum())

print("\nAvailable Customer IDs:")
print(df["Customer ID"].notna().sum())

print("\nUnique Customer IDs:")
print(df["Customer ID"].nunique())


# ============================================================
# STEP 18 - CHECK PRODUCT DESCRIPTIONS
# ============================================================

print("\n" + "=" * 60)
print("STEP 18 - PRODUCT DESCRIPTION ANALYSIS")
print("=" * 60)

print("\nMissing descriptions:")
print(df["Description"].isna().sum())

print("\nAvailable descriptions:")
print(df["Description"].notna().sum())

print("\nUnique descriptions:")
print(df["Description"].nunique())


# ============================================================
# STEP 19 - CHECK STOCK CODES
# ============================================================

print("\n" + "=" * 60)
print("STEP 19 - STOCK CODE ANALYSIS")
print("=" * 60)

print("\nUnique Stock Codes:")
print(df["StockCode"].nunique())

print("\nSample Stock Codes:")
print(df["StockCode"].unique()[:20])


# ============================================================
# STEP 20 - CHECK COUNTRIES
# ============================================================

print("\n" + "=" * 60)
print("STEP 20 - COUNTRY ANALYSIS")
print("=" * 60)

print("\nNumber of countries:")
print(df["Country"].nunique())

print("\nCountries:")
print(df["Country"].unique())


# ============================================================
# STEP 21 - CHECK DATE RANGE
# ============================================================

print("\n" + "=" * 60)
print("STEP 21 - DATE RANGE ANALYSIS")
print("=" * 60)

print("\nEarliest Invoice Date:")
print(df["InvoiceDate"].min())

print("\nLatest Invoice Date:")
print(df["InvoiceDate"].max())


# ============================================================
# STEP 22 - CHECK INVALID DATES
# ============================================================

print("\n" + "=" * 60)
print("STEP 22 - INVALID DATE CHECK")
print("=" * 60)

print("\nMissing Invoice Dates:")
print(df["InvoiceDate"].isna().sum())

print("\nInvoiceDate data type:")
print(df["InvoiceDate"].dtype)


# ============================================================
# STEP 23 - QUANTITY DISTRIBUTION
# ============================================================

print("\n" + "=" * 60)
print("STEP 23 - QUANTITY DISTRIBUTION")
print("=" * 60)

print("\nQuantity statistics:")
print(df["Quantity"].describe())

print("\nMinimum Quantity:")
print(df["Quantity"].min())

print("\nMaximum Quantity:")
print(df["Quantity"].max())


# ============================================================
# STEP 24 - PRICE DISTRIBUTION
# ============================================================

print("\n" + "=" * 60)
print("STEP 24 - PRICE DISTRIBUTION")
print("=" * 60)

print("\nPrice statistics:")
print(df["Price"].describe())

print("\nMinimum Price:")
print(df["Price"].min())

print("\nMaximum Price:")
print(df["Price"].max())


# ============================================================
# STEP 25 - UNUSUAL QUANTITY ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 25 - UNUSUAL QUANTITY ANALYSIS")
print("=" * 60)

high_quantity = df[
    df["Quantity"] > df["Quantity"].quantile(0.99)
]

print("\nTransactions above 99th percentile quantity:")
print(high_quantity.shape)

print("\nSample high quantity transactions:")
print(high_quantity.head())


# ============================================================
# STEP 26 - UNUSUAL PRICE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 26 - UNUSUAL PRICE ANALYSIS")
print("=" * 60)

high_price = df[
    df["Price"] > df["Price"].quantile(0.99)
]

print("\nTransactions above 99th percentile price:")
print(high_price.shape)

print("\nSample high price transactions:")
print(high_price.head())


# ============================================================
# STEP 27 - MISSING CUSTOMER ID ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 27 - MISSING CUSTOMER ID ANALYSIS")
print("=" * 60)

missing_customer_df = df[
    df["Customer ID"].isna()
]

print("\nTransactions without Customer ID:")
print(missing_customer_df.shape)

print("\nMissing Customer ID by country:")
print(
    missing_customer_df["Country"]
    .value_counts()
    .head(10)
)


# ============================================================
# STEP 28 - MISSING DESCRIPTION ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 28 - MISSING DESCRIPTION ANALYSIS")
print("=" * 60)

missing_description_df = df[
    df["Description"].isna()
]

print("\nTransactions without Description:")
print(missing_description_df.shape)

print("\nMissing descriptions by country:")
print(
    missing_description_df["Country"]
    .value_counts()
    .head(10)
)


# ============================================================
# STEP 29 - UNIQUE INVOICE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 29 - INVOICE ANALYSIS")
print("=" * 60)

print("\nUnique invoices:")
print(df["Invoice"].nunique())

print("\nTotal transaction rows:")
print(len(df))


# ============================================================
# STEP 30 - PRODUCT TRANSACTION ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 30 - PRODUCT TRANSACTION ANALYSIS")
print("=" * 60)

product_transaction_counts = (
    df.groupby("StockCode")
    .size()
    .sort_values(ascending=False)
)

print("\nTop 10 Stock Codes by transaction count:")
print(
    product_transaction_counts.head(10)
)


# ============================================================
# STEP 31 - COUNTRY TRANSACTION ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 31 - COUNTRY TRANSACTION ANALYSIS")
print("=" * 60)

country_transaction_counts = (
    df.groupby("Country")
    .size()
    .sort_values(ascending=False)
)

print("\nTop 10 countries by transaction count:")
print(
    country_transaction_counts.head(10)
)


# ============================================================
# STEP 32 - FINAL PRE-CLEANING VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 32 - FINAL PRE-CLEANING VALIDATION")
print("=" * 60)

print("\nCurrent dataset shape:")
print(df.shape)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nNegative quantities:")
print(
    (df["Quantity"] < 0).sum()
)

print("\nZero quantities:")
print(
    (df["Quantity"] == 0).sum()
)

print("\nNegative prices:")
print(
    (df["Price"] < 0).sum()
)

print("\nZero prices:")
print(
    (df["Price"] == 0).sum()
)

print("\nCancelled invoices:")
print(
    df["Invoice"]
    .astype(str)
    .str.startswith("C")
    .sum()
)

print("\n" + "=" * 70)
print("STEPS 1-32 COMPLETED")
print("=" * 70)
# ============================================================
# STEP 33 - REMOVE CANCELLED TRANSACTIONS
# ============================================================

print("\n" + "=" * 60)
print("STEP 33 - REMOVE CANCELLED TRANSACTIONS")
print("=" * 60)

df = df[
    ~df["Invoice"].astype(str).str.startswith("C")
].copy()

print("\nShape after removing cancelled transactions:")
print(df.shape)

print("\nRemaining cancelled transactions:")
print(
    df["Invoice"]
    .astype(str)
    .str.startswith("C")
    .sum()
)


# ============================================================
# STEP 34 - CHECK REMAINING NEGATIVE QUANTITIES
# ============================================================

print("\n" + "=" * 60)
print("STEP 34 - REMAINING NEGATIVE QUANTITIES")
print("=" * 60)

negative_quantity = df[df["Quantity"] < 0]

print("\nRemaining negative quantity rows:")
print(negative_quantity.shape)

print("\nSample remaining negative quantity rows:")
print(negative_quantity.head())


# ============================================================
# STEP 35 - ANALYZE REMAINING NEGATIVE QUANTITIES
# ============================================================

print("\n" + "=" * 60)
print("STEP 35 - NEGATIVE QUANTITY ANALYSIS")
print("=" * 60)

print("\nNegative quantity transactions by price:")
print(negative_quantity["Price"].describe())

print("\nNegative quantity transactions with zero price:")
print(
    (negative_quantity["Price"] == 0).sum()
)

print("\nNegative quantity transactions with missing Customer ID:")
print(
    negative_quantity["Customer ID"].isna().sum()
)

print("\nNegative quantity transactions with missing Description:")
print(
    negative_quantity["Description"].isna().sum()
)


# ============================================================
# STEP 36 - REMOVE INVALID NEGATIVE QUANTITIES
# ============================================================

print("\n" + "=" * 60)
print("STEP 36 - REMOVE INVALID NEGATIVE QUANTITIES")
print("=" * 60)

df = df[df["Quantity"] >= 0].copy()

print("\nShape after removing negative quantities:")
print(df.shape)

print("\nRemaining negative quantity rows:")
print(
    (df["Quantity"] < 0).sum()
)


# ============================================================
# STEP 37 - CHECK REMAINING NEGATIVE PRICES
# ============================================================

print("\n" + "=" * 60)
print("STEP 37 - REMAINING NEGATIVE PRICES")
print("=" * 60)

negative_price = df[df["Price"] < 0]

print("\nRemaining negative price rows:")
print(negative_price.shape)

print("\nRemaining negative price records:")
print(negative_price)


# ============================================================
# STEP 38 - REMOVE NEGATIVE PRICE RECORDS
# ============================================================

print("\n" + "=" * 60)
print("STEP 38 - REMOVE NEGATIVE PRICE RECORDS")
print("=" * 60)

df = df[df["Price"] >= 0].copy()

print("\nShape after removing negative-price records:")
print(df.shape)

print("\nRemaining negative price rows:")
print(
    (df["Price"] < 0).sum()
)


# ============================================================
# STEP 39 - ANALYZE ZERO-PRICE TRANSACTIONS
# ============================================================

print("\n" + "=" * 60)
print("STEP 39 - ZERO-PRICE TRANSACTION ANALYSIS")
print("=" * 60)

zero_price = df[df["Price"] == 0]

print("\nZero-price rows:")
print(zero_price.shape)

print("\nZero-price transactions with missing Customer ID:")
print(
    zero_price["Customer ID"].isna().sum()
)

print("\nZero-price transactions with missing Description:")
print(
    zero_price["Description"].isna().sum()
)

print("\nSample zero-price transactions:")
print(zero_price.head())


# ============================================================
# STEP 40 - NEGATIVE QUANTITY & CANCELLATION CHECK
# ============================================================

print("\n" + "=" * 60)
print("STEP 40 - NEGATIVE QUANTITY & CANCELLATION ANALYSIS")
print("=" * 60)

negative_quantity = df[df["Quantity"] < 0]

print("\nNegative quantity rows:")
print(negative_quantity.shape)

print("\nNumber of negative quantity transactions:")
print(len(negative_quantity))

print("\nCancellation invoices:")
cancellations = df[
    df["Invoice"].astype(str).str.startswith("C")
]

print(len(cancellations))

print("\nPercentage of negative quantity transactions:")

if len(df) > 0:
    negative_percentage = (
        len(negative_quantity) / len(df) * 100
    )
else:
    negative_percentage = 0

print(round(negative_percentage, 2), "%")


# ============================================================
# STEP 41 - FINAL DATA QUALITY CHECK & SALES AMOUNT
# ============================================================

print("\n" + "=" * 60)
print("STEP 41 - FINAL DATA QUALITY CHECK")
print("=" * 60)

print("\nFinal dataset shape:")
print(df.shape)

print("\nRemaining missing values:")
print(df.isnull().sum())

print("\nRemaining duplicate rows:")
print(df.duplicated().sum())

print("\nRemaining negative quantities:")
print((df["Quantity"] < 0).sum())

print("\nRemaining negative prices:")
print((df["Price"] < 0).sum())

print("\nRemaining zero quantities:")
print((df["Quantity"] == 0).sum())

print("\nRemaining zero-price transactions:")
print((df["Price"] == 0).sum())

df["Sales Amount"] = (
    df["Quantity"] * df["Price"]
)

print("\nSales Amount column created.")

print("\nSample Sales Amount:")
print(
    df[
        [
            "Invoice",
            "StockCode",
            "Quantity",
            "Price",
            "Sales Amount"
        ]
    ].head()
)

print("\nSales Amount statistics:")
print(df["Sales Amount"].describe())

print("\nTotal Sales Amount:")
print(
    round(df["Sales Amount"].sum(), 2)
)
# Step 42: Customer and zero-price analysis

print("\n" + "=" * 60)
print("STEP 42 - CUSTOMER & ZERO-PRICE ANALYSIS")
print("=" * 60)

# Customer coverage
customer_transactions = df["Customer ID"].notna().sum()
missing_customer = df["Customer ID"].isna().sum()

print("\nTransactions with Customer ID:")
print(customer_transactions)

print("\nTransactions without Customer ID:")
print(missing_customer)

print("\nPercentage without Customer ID:")
print(round(missing_customer / len(df) * 100, 2), "%")


# Unique customers
print("\nUnique customers:")
print(df["Customer ID"].nunique())


# Zero-price sales impact
zero_price = df[df["Price"] == 0]

print("\nZero-price transactions:")
print(len(zero_price))

print("\nZero-price Sales Amount:")
print(zero_price["Sales Amount"].sum())

print("\nZero-price transactions with Customer ID:")
print(zero_price["Customer ID"].notna().sum())

print("\nZero-price transactions without Customer ID:")
print(zero_price["Customer ID"].isna().sum())


# Non-zero price transactions
non_zero_price = df[df["Price"] > 0]

print("\nNon-zero-price transactions:")
print(len(non_zero_price))

print("\nNon-zero-price total sales:")
print(round(non_zero_price["Sales Amount"].sum(), 2))


# Top 10 customers by sales
customer_sales = (
    df[df["Customer ID"].notna()]
    .groupby("Customer ID")["Sales Amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 customers by Sales Amount:")
print(customer_sales.head(10))
# Step 43: Country and monthly sales analysis

print("\n" + "=" * 60)
print("STEP 43 - COUNTRY & MONTHLY SALES ANALYSIS")
print("=" * 60)

# ------------------------------------------------------------
# SALES BY COUNTRY
# ------------------------------------------------------------

country_sales = (
    df.groupby("Country")["Sales Amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 countries by Sales Amount:")
print(country_sales.head(10))


print("\nSales by Country:")
print(country_sales)


# ------------------------------------------------------------
# TRANSACTIONS BY COUNTRY
# ------------------------------------------------------------

country_transactions = (
    df.groupby("Country")
    .size()
    .sort_values(ascending=False)
)

print("\nTop 10 countries by number of transactions:")
print(country_transactions.head(10))


# ------------------------------------------------------------
# MONTHLY SALES
# ------------------------------------------------------------

df["YearMonth"] = df["InvoiceDate"].dt.to_period("M")

monthly_sales = (
    df.groupby("YearMonth")["Sales Amount"]
    .sum()
)

print("\nMonthly Sales:")
print(monthly_sales)


# ------------------------------------------------------------
# TOP 10 MONTHS
# ------------------------------------------------------------

print("\nTop 10 months by Sales Amount:")
print(monthly_sales.sort_values(ascending=False).head(10))


# ------------------------------------------------------------
# BEST MONTH
# ------------------------------------------------------------

best_month = monthly_sales.idxmax()
best_month_sales = monthly_sales.max()

print("\nBest month:")
print(best_month)

print("\nBest month Sales Amount:")
print(round(best_month_sales, 2))


# ------------------------------------------------------------
# LOWEST MONTH
# ------------------------------------------------------------

lowest_month = monthly_sales.idxmin()
lowest_month_sales = monthly_sales.min()

print("\nLowest month:")
print(lowest_month)

print("\nLowest month Sales Amount:")
print(round(lowest_month_sales, 2))
# Step 44: Product and customer performance analysis

print("\n" + "=" * 60)
print("STEP 44 - PRODUCT & CUSTOMER PERFORMANCE")
print("=" * 60)

# ------------------------------------------------------------
# TOP PRODUCTS BY SALES
# ------------------------------------------------------------

product_sales = (
    df.groupby(["StockCode", "Description"])["Sales Amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 products by Sales Amount:")
print(product_sales.head(10))


# ------------------------------------------------------------
# TOP PRODUCTS BY QUANTITY
# ------------------------------------------------------------

product_quantity = (
    df.groupby(["StockCode", "Description"])["Quantity"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 products by Quantity Sold:")
print(product_quantity.head(10))


# ------------------------------------------------------------
# TOP CUSTOMERS BY SALES
# ------------------------------------------------------------

customer_sales = (
    df[df["Customer ID"].notna()]
    .groupby("Customer ID")["Sales Amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 customers by Sales Amount:")
print(customer_sales.head(10))


# ------------------------------------------------------------
# TOP CUSTOMERS BY NUMBER OF TRANSACTIONS
# ------------------------------------------------------------

customer_transactions = (
    df[df["Customer ID"].notna()]
    .groupby("Customer ID")
    .size()
    .sort_values(ascending=False)
)

print("\nTop 10 customers by number of transactions:")
print(customer_transactions.head(10))


# ------------------------------------------------------------
# AVERAGE TRANSACTION VALUE
# ------------------------------------------------------------

average_transaction_value = df["Sales Amount"].mean()

print("\nAverage transaction value:")
print(round(average_transaction_value, 2))


# ------------------------------------------------------------
# TOTAL QUANTITY SOLD
# ------------------------------------------------------------

total_quantity = df["Quantity"].sum()

print("\nTotal quantity sold:")
print(total_quantity)
# Step 45: Product quality and sales concentration analysis

print("\n" + "=" * 60)
print("STEP 45 - PRODUCT QUALITY & SALES CONCENTRATION")
print("=" * 60)

# ------------------------------------------------------------
# UNIQUE PRODUCTS
# ------------------------------------------------------------

unique_products = df["StockCode"].nunique()

print("\nUnique Stock Codes:")
print(unique_products)


# ------------------------------------------------------------
# MISSING PRODUCT DESCRIPTIONS
# ------------------------------------------------------------

missing_description = df["Description"].isna().sum()

print("\nMissing product descriptions:")
print(missing_description)


# ------------------------------------------------------------
# TOP 10 PRODUCTS BY SALES - EXCLUDING NON-PRODUCT CODES
# ------------------------------------------------------------

excluded_codes = ["M", "POST", "DOT"]

product_df = df[~df["StockCode"].isin(excluded_codes)].copy()

real_product_sales = (
    product_df.groupby(["StockCode", "Description"])["Sales Amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 actual products by Sales Amount:")
print(real_product_sales.head(10))


# ------------------------------------------------------------
# TOP 10 ACTUAL PRODUCTS BY QUANTITY
# ------------------------------------------------------------

real_product_quantity = (
    product_df.groupby(["StockCode", "Description"])["Quantity"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 actual products by Quantity:")
print(real_product_quantity.head(10))


# ------------------------------------------------------------
# TOP 10 PRODUCTS SALES CONTRIBUTION
# ------------------------------------------------------------

top_10_product_sales = real_product_sales.head(10).sum()
total_product_sales = product_df["Sales Amount"].sum()

print("\nTop 10 products total sales:")
print(round(top_10_product_sales, 2))

print("\nTotal actual product sales:")
print(round(total_product_sales, 2))

print("\nTop 10 products sales contribution:")
print(
    round(
        top_10_product_sales / total_product_sales * 100,
        2
    ),
    "%"
)


# ------------------------------------------------------------
# UNIQUE CUSTOMERS WITH SALES
# ------------------------------------------------------------

customers_with_sales = df[df["Customer ID"].notna()]["Customer ID"].nunique()

print("\nCustomers with identified Customer ID:")
print(customers_with_sales)
# Step 46: Final business KPIs

print("\n" + "=" * 60)
print("STEP 46 - FINAL BUSINESS KPIs")
print("=" * 60)

# Total sales
total_sales = df["Sales Amount"].sum()

# Total quantity
total_quantity = df["Quantity"].sum()

# Total transactions
total_transactions = df["Invoice"].nunique()

# Total products
total_products = df["StockCode"].nunique()

# Total customers
total_customers = df["Customer ID"].nunique()

# Average order value
average_order_value = total_sales / total_transactions

# Best country
best_country = country_sales.idxmax()
best_country_sales = country_sales.max()

# Best month
best_month = monthly_sales.idxmax()
best_month_sales = monthly_sales.max()

# Best product
best_product = real_product_sales.idxmax()
best_product_sales = real_product_sales.max()

# Best customer
best_customer = customer_sales.idxmax()
best_customer_sales = customer_sales.max()


print("\nTotal Sales:")
print(round(total_sales, 2))

print("\nTotal Quantity Sold:")
print(total_quantity)

print("\nTotal Unique Invoices:")
print(total_transactions)

print("\nTotal Unique Products:")
print(total_products)

print("\nTotal Unique Customers:")
print(total_customers)

print("\nAverage Order Value:")
print(round(average_order_value, 2))

print("\nBest Country:")
print(best_country)

print("\nBest Country Sales:")
print(round(best_country_sales, 2))

print("\nBest Month:")
print(best_month)

print("\nBest Month Sales:")
print(round(best_month_sales, 2))

print("\nBest Product:")
print(best_product)

print("\nBest Product Sales:")
print(round(best_product_sales, 2))

print("\nBest Customer:")
print(best_customer)

print("\nBest Customer Sales:")
print(round(best_customer_sales, 2))
# Step 47: Create summary tables for visualization

print("\n" + "=" * 60)
print("STEP 47 - CREATE SUMMARY TABLES")
print("=" * 60)

# ------------------------------------------------------------
# 1. MONTHLY SALES TABLE
# ------------------------------------------------------------

monthly_sales_table = (
    df.groupby("YearMonth", as_index=False)["Sales Amount"]
    .sum()
)

print("\nMonthly Sales Table:")
print(monthly_sales_table)


# ------------------------------------------------------------
# 2. COUNTRY SALES TABLE
# ------------------------------------------------------------

country_sales_table = (
    df.groupby("Country", as_index=False)["Sales Amount"]
    .sum()
    .sort_values("Sales Amount", ascending=False)
)

print("\nTop 10 Country Sales Table:")
print(country_sales_table.head(10))


# ------------------------------------------------------------
# 3. PRODUCT SALES TABLE
# ------------------------------------------------------------

product_sales_table = (
    product_df.groupby(
        ["StockCode", "Description"],
        as_index=False
    )["Sales Amount"]
    .sum()
    .sort_values("Sales Amount", ascending=False)
)

print("\nTop 10 Product Sales Table:")
print(product_sales_table.head(10))


# ------------------------------------------------------------
# 4. CUSTOMER SALES TABLE
# ------------------------------------------------------------

customer_sales_table = (
    df[df["Customer ID"].notna()]
    .groupby("Customer ID", as_index=False)["Sales Amount"]
    .sum()
    .sort_values("Sales Amount", ascending=False)
)

print("\nTop 10 Customer Sales Table:")
print(customer_sales_table.head(10))


# ------------------------------------------------------------
# 5. SAVE SUMMARY TABLES
# ------------------------------------------------------------

monthly_sales_table.to_csv(
    "data/processed/monthly_sales.csv",
    index=False
)

country_sales_table.to_csv(
    "data/processed/country_sales.csv",
    index=False
)

product_sales_table.to_csv(
    "data/processed/product_sales.csv",
    index=False
)

customer_sales_table.to_csv(
    "data/processed/customer_sales.csv",
    index=False
)

print("\nSummary tables saved successfully.")
# Step 48: Create business charts

import matplotlib.pyplot as plt

print("\n" + "=" * 60)
print("STEP 48 - CREATE BUSINESS CHARTS")
print("=" * 60)


# ------------------------------------------------------------
# CHART 1: MONTHLY SALES TREND
# ------------------------------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales_table["YearMonth"].astype(str),
    monthly_sales_table["Sales Amount"],
    marker="o"
)

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales Amount")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("data/processed/monthly_sales_trend.png")
plt.show()


# ------------------------------------------------------------
# CHART 2: TOP 10 COUNTRIES
# ------------------------------------------------------------

top_countries = country_sales_table.head(10)

plt.figure(figsize=(10, 6))

plt.barh(
    top_countries["Country"][::-1],
    top_countries["Sales Amount"][::-1]
)

plt.title("Top 10 Countries by Sales")
plt.xlabel("Sales Amount")
plt.ylabel("Country")
plt.tight_layout()

plt.savefig("data/processed/top_10_countries.png")
plt.show()


# ------------------------------------------------------------
# CHART 3: TOP 10 PRODUCTS
# ------------------------------------------------------------

top_products = product_sales_table.head(10)

product_labels = (
    top_products["Description"]
    .fillna("Unknown")
    .str[:30]
)

plt.figure(figsize=(10, 6))

plt.barh(
    product_labels[::-1],
    top_products["Sales Amount"][::-1]
)

plt.title("Top 10 Products by Sales")
plt.xlabel("Sales Amount")
plt.ylabel("Product")
plt.tight_layout()

plt.savefig("data/processed/top_10_products.png")
plt.show()


# ------------------------------------------------------------
# CHART 4: TOP 10 CUSTOMERS
# ------------------------------------------------------------

top_customers = customer_sales_table.head(10)

plt.figure(figsize=(10, 6))

plt.bar(
    top_customers["Customer ID"].astype(str),
    top_customers["Sales Amount"]
)

plt.title("Top 10 Customers by Sales")
plt.xlabel("Customer ID")
plt.ylabel("Sales Amount")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("data/processed/top_10_customers.png")
plt.show()


print("\nAll 4 charts created successfully.")
# Step 49: RFM Customer Analysis

print("\n" + "=" * 60)
print("STEP 49 - RFM CUSTOMER ANALYSIS")
print("=" * 60)

# Use only transactions with Customer ID
customer_df = df[df["Customer ID"].notna()].copy()

# Reference date = day after the last transaction
reference_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

# Calculate RFM metrics
rfm = customer_df.groupby("Customer ID").agg(
    Recency=("InvoiceDate", lambda x: (reference_date - x.max()).days),
    Frequency=("Invoice", "nunique"),
    Monetary=("Sales Amount", "sum")
)

print("\nRFM table:")
print(rfm.head())

print("\nRFM shape:")
print(rfm.shape)

print("\nRFM statistics:")
print(rfm.describe())

# Top customers by Monetary value
print("\nTop 10 customers by Monetary Value:")
print(rfm.sort_values("Monetary", ascending=False).head(10))

# Most frequent customers
print("\nTop 10 customers by Frequency:")
print(rfm.sort_values("Frequency", ascending=False).head(10))

# Most recent customers
print("\nTop 10 most recent customers:")
print(rfm.sort_values("Recency", ascending=True).head(10))

# Save RFM table
rfm.to_csv("data/processed/rfm_customer_analysis.csv")

print("\nRFM analysis saved successfully.")
# ============================================================
# STEP 50 - RFM CUSTOMER SEGMENTATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 50 - RFM CUSTOMER SEGMENTATION")
print("=" * 60)

# Create RFM scores
rfm["R_Score"] = pd.qcut(
    rfm["Recency"],
    5,
    labels=[5, 4, 3, 2, 1],
    duplicates="drop"
).astype(int)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# Total RFM score
rfm["RFM_Score"] = (
    rfm["R_Score"]
    + rfm["F_Score"]
    + rfm["M_Score"]
)

# Customer segmentation
def segment_customer(row):

    if row["RFM_Score"] >= 13:
        return "VIP / Champions"

    elif row["RFM_Score"] >= 10:
        return "Loyal Customers"

    elif row["RFM_Score"] >= 7:
        return "Potential Loyalists"

    elif row["RFM_Score"] >= 5:
        return "At Risk"

    else:
        return "Lost / Hibernating"


rfm["Customer_Segment"] = rfm.apply(segment_customer, axis=1)

# Display sample
print("\nRFM segmentation sample:")
print(rfm.head(10))

# Count customers in each segment
print("\nCustomer segment counts:")
print(rfm["Customer_Segment"].value_counts())

# Percentage of customers in each segment
print("\nCustomer segment percentages:")
print(
    (rfm["Customer_Segment"].value_counts(normalize=True) * 100)
    .round(2)
)

# Segment summary
segment_summary = rfm.groupby("Customer_Segment").agg(
    Customers=("Customer_Segment", "count"),
    Avg_Recency=("Recency", "mean"),
    Avg_Frequency=("Frequency", "mean"),
    Avg_Monetary=("Monetary", "mean")
).round(2)

print("\nCustomer segment summary:")
print(segment_summary)

# Save segmented customer data
rfm.to_csv("data/processed/rfm_customer_segments.csv")

print("\nRFM customer segmentation completed successfully.")
# ============================================================
# STEP 51 - CUSTOMER SEGMENT PERFORMANCE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 51 - CUSTOMER SEGMENT PERFORMANCE ANALYSIS")
print("=" * 60)

# Segment performance summary
segment_performance = rfm.groupby("Customer_Segment").agg(
    Customers=("Customer_Segment", "count"),
    Total_Revenue=("Monetary", "sum"),
    Average_Revenue=("Monetary", "mean"),
    Average_Frequency=("Frequency", "mean"),
    Average_Recency=("Recency", "mean")
).round(2)

# Sort by total revenue
segment_performance = segment_performance.sort_values(
    "Total_Revenue",
    ascending=False
)

print("\nCustomer Segment Performance:")
print(segment_performance)

# Revenue percentage contributed by each segment
segment_performance["Revenue_Percentage"] = (
    segment_performance["Total_Revenue"]
    / segment_performance["Total_Revenue"].sum()
    * 100
).round(2)

print("\nRevenue contribution by segment:")
print(
    segment_performance[
        ["Customers", "Total_Revenue", "Revenue_Percentage"]
    ]
)

# Customer percentage
segment_performance["Customer_Percentage"] = (
    segment_performance["Customers"]
    / segment_performance["Customers"].sum()
    * 100
).round(2)

print("\nCustomer distribution by segment:")
print(
    segment_performance[
        ["Customers", "Customer_Percentage"]
    ]
)

# Highest revenue segment
highest_revenue_segment = segment_performance[
    "Total_Revenue"
].idxmax()

print(
    "\nHighest revenue segment:",
    highest_revenue_segment
)

# Largest customer segment
largest_customer_segment = segment_performance[
    "Customers"
].idxmax()

print(
    "Largest customer segment:",
    largest_customer_segment
)

# Save analysis
segment_performance.to_csv(
    "data/processed/customer_segment_performance.csv"
)

print("\nCustomer segment performance analysis completed successfully.")
# ============================================================
# STEP 52 - CUSTOMER SEGMENT VISUALIZATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 52 - CUSTOMER SEGMENT VISUALIZATION")
print("=" * 60)

import matplotlib.pyplot as plt

# 1. Customer count by segment
plt.figure(figsize=(10, 6))

segment_performance["Customers"].plot(
    kind="bar"
)

plt.title("Number of Customers by RFM Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("data/processed/customer_count_by_segment.png")
plt.show()


# 2. Total revenue by segment
plt.figure(figsize=(10, 6))

segment_performance["Total_Revenue"].plot(
    kind="bar"
)

plt.title("Total Revenue by RFM Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("data/processed/revenue_by_segment.png")
plt.show()


# 3. Revenue contribution
plt.figure(figsize=(8, 8))

segment_performance["Revenue_Percentage"].plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.title("Revenue Contribution by Customer Segment")
plt.ylabel("")
plt.tight_layout()

plt.savefig("data/processed/revenue_contribution_by_segment.png")
plt.show()

print("\nCustomer segment visualizations created successfully.")
# ============================================================
# STEP 53 - PRODUCT PERFORMANCE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 53 - PRODUCT PERFORMANCE ANALYSIS")
print("=" * 60)

# Create Revenue column
df["Revenue"] = df["Quantity"] * df["Price"]

# Product-level analysis
product_analysis = df.groupby(
    ["StockCode", "Description"]
).agg(
    Total_Quantity=("Quantity", "sum"),
    Total_Revenue=("Revenue", "sum"),
    Average_Price=("Price", "mean"),
    Transactions=("Invoice", "nunique")
).reset_index()

# Top 10 products by revenue
top_products_revenue = product_analysis.sort_values(
    "Total_Revenue",
    ascending=False
).head(10)

print("\nTop 10 products by Revenue:")
print(top_products_revenue)

# Top 10 products by quantity
top_products_quantity = product_analysis.sort_values(
    "Total_Quantity",
    ascending=False
).head(10)

print("\nTop 10 products by Quantity Sold:")
print(top_products_quantity)

# Top 10 products by number of transactions
top_products_transactions = product_analysis.sort_values(
    "Transactions",
    ascending=False
).head(10)

print("\nTop 10 products by Transactions:")
print(top_products_transactions)

# Product analysis statistics
print("\nProduct analysis statistics:")
print(product_analysis[
    ["Total_Quantity", "Total_Revenue", "Average_Price", "Transactions"]
].describe())

# Save product analysis
product_analysis.to_csv(
    "data/processed/product_analysis.csv",
    index=False
)

# Save top products
top_products_revenue.to_csv(
    "data/processed/top_10_products_revenue.csv",
    index=False
)

top_products_quantity.to_csv(
    "data/processed/top_10_products_quantity.csv",
    index=False
)

print("\nProduct performance analysis completed successfully.")
# ============================================================
# STEP 54 - PRODUCT PERFORMANCE VISUALIZATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 54 - PRODUCT PERFORMANCE VISUALIZATION")
print("=" * 60)

import matplotlib.pyplot as plt

# Top 10 products by revenue
plt.figure(figsize=(12, 7))

plt.barh(
    top_products_revenue["Description"].astype(str),
    top_products_revenue["Total_Revenue"]
)

plt.title("Top 10 Products by Revenue")
plt.xlabel("Total Revenue")
plt.ylabel("Product")
plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig("data/processed/top_10_products_revenue.png")
plt.show()


# Top 10 products by quantity
plt.figure(figsize=(12, 7))

plt.barh(
    top_products_quantity["Description"].astype(str),
    top_products_quantity["Total_Quantity"]
)

plt.title("Top 10 Products by Quantity Sold")
plt.xlabel("Quantity Sold")
plt.ylabel("Product")
plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig("data/processed/top_10_products_quantity.png")
plt.show()


# Top 10 products by transactions
plt.figure(figsize=(12, 7))

plt.barh(
    top_products_transactions["Description"].astype(str),
    top_products_transactions["Transactions"]
)

plt.title("Top 10 Products by Transactions")
plt.xlabel("Number of Transactions")
plt.ylabel("Product")
plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig("data/processed/top_10_products_transactions.png")
plt.show()

print("\nProduct performance visualizations created successfully.")
# ============================================================
# STEP 55 - COUNTRY-WISE SALES ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 55 - COUNTRY-WISE SALES ANALYSIS")
print("=" * 60)

# Country-wise sales analysis
country_analysis = df.groupby("Country").agg(
    Customers=("Customer ID", "nunique"),
    Orders=("Invoice", "nunique"),
    Quantity_Sold=("Quantity", "sum"),
    Total_Revenue=("Revenue", "sum")
).reset_index()

# Sort by revenue
country_analysis = country_analysis.sort_values(
    "Total_Revenue",
    ascending=False
)

# Top 10 countries by revenue
print("\nTop 10 Countries by Revenue:")
print(country_analysis.head(10))

# Top 10 countries by customers
top_countries_customers = country_analysis.sort_values(
    "Customers",
    ascending=False
).head(10)

print("\nTop 10 Countries by Number of Customers:")
print(top_countries_customers)

# Revenue percentage
country_analysis["Revenue_Percentage"] = (
    country_analysis["Total_Revenue"]
    / country_analysis["Total_Revenue"].sum()
    * 100
).round(2)

print("\nRevenue contribution of top 10 countries:")
print(
    country_analysis[
        ["Country", "Total_Revenue", "Revenue_Percentage"]
    ].head(10)
)

# Save country analysis
country_analysis.to_csv(
    "data/processed/country_analysis.csv",
    index=False
)

print("\nCountry-wise sales analysis completed successfully.")
# ============================================================
# STEP 56 - COUNTRY-WISE SALES VISUALIZATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 56 - COUNTRY-WISE SALES VISUALIZATION")
print("=" * 60)

import matplotlib.pyplot as plt

# Top 10 countries by revenue
top_10_countries = country_analysis.head(10)

plt.figure(figsize=(12, 7))

plt.barh(
    top_10_countries["Country"],
    top_10_countries["Total_Revenue"]
)

plt.title("Top 10 Countries by Revenue")
plt.xlabel("Total Revenue")
plt.ylabel("Country")
plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig("data/processed/top_10_countries_revenue.png")
plt.show()


# Top 10 countries by customers
plt.figure(figsize=(12, 7))

plt.barh(
    top_countries_customers["Country"],
    top_countries_customers["Customers"]
)

plt.title("Top 10 Countries by Number of Customers")
plt.xlabel("Number of Customers")
plt.ylabel("Country")
plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig("data/processed/top_10_countries_customers.png")
plt.show()

print("\nCountry-wise sales visualizations created successfully.")
# ============================================================
# STEP 57 - MONTHLY SALES TREND
# ============================================================

print("\n" + "=" * 60)
print("STEP 57 - MONTHLY SALES TREND")
print("=" * 60)

# Create Year-Month column
df["YearMonth"] = df["InvoiceDate"].dt.to_period("M")

# Monthly sales analysis
monthly_sales = df.groupby("YearMonth").agg(
    Orders=("Invoice", "nunique"),
    Customers=("Customer ID", "nunique"),
    Quantity_Sold=("Quantity", "sum"),
    Total_Revenue=("Revenue", "sum")
).reset_index()

# Convert YearMonth to string for easier display/saving
monthly_sales["YearMonth"] = monthly_sales["YearMonth"].astype(str)

print("\nMonthly Sales:")
print(monthly_sales)

print("\nTop 10 Months by Revenue:")
print(
    monthly_sales.sort_values(
        "Total_Revenue",
        ascending=False
    ).head(10)
)

# Save monthly analysis
monthly_sales.to_csv(
    "data/processed/monthly_sales.csv",
    index=False
)

print("\nMonthly sales trend analysis completed successfully.")
# ============================================================
# STEP 58 - MONTHLY SALES VISUALIZATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 58 - MONTHLY SALES VISUALIZATION")
print("=" * 60)

import matplotlib.pyplot as plt

# Monthly revenue trend
plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["YearMonth"],
    monthly_sales["Total_Revenue"],
    marker="o"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("data/processed/monthly_revenue_trend.png")
plt.show()


# Monthly orders trend
plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["YearMonth"],
    monthly_sales["Orders"],
    marker="o"
)

plt.title("Monthly Orders Trend")
plt.xlabel("Month")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("data/processed/monthly_orders_trend.png")
plt.show()

print("\nMonthly sales visualizations created successfully.")
# ============================================================
# STEP 59 - SALES GROWTH ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 59 - SALES GROWTH ANALYSIS")
print("=" * 60)

# Calculate month-over-month revenue growth
monthly_sales["Revenue_Growth_%"] = (
    monthly_sales["Total_Revenue"]
    .pct_change()
    * 100
).round(2)

# Overall business metrics
total_revenue = df["Revenue"].sum()
total_orders = df["Invoice"].nunique()
total_customers = df["Customer ID"].nunique()
average_monthly_revenue = monthly_sales["Total_Revenue"].mean()

print("\nOverall Sales Metrics:")
print(f"Total Revenue: £{total_revenue:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Total Customers: {total_customers:,}")
print(f"Average Monthly Revenue: £{average_monthly_revenue:,.2f}")

# Monthly growth
print("\nMonthly Revenue Growth:")
print(
    monthly_sales[
        ["YearMonth", "Total_Revenue", "Revenue_Growth_%"]
    ]
)

# Best month
best_month = monthly_sales.loc[
    monthly_sales["Total_Revenue"].idxmax()
]

print("\nBest Month:")
print(best_month)

# Worst month
worst_month = monthly_sales.loc[
    monthly_sales["Total_Revenue"].idxmin()
]

print("\nWorst Month:")
print(worst_month)

# Highest growth month
growth_data = monthly_sales.dropna(
    subset=["Revenue_Growth_%"]
)

highest_growth_month = growth_data.loc[
    growth_data["Revenue_Growth_%"].idxmax()
]

print("\nHighest Month-over-Month Growth:")
print(highest_growth_month)

# Save growth analysis
monthly_sales.to_csv(
    "data/processed/monthly_sales_growth.csv",
    index=False
)

print("\nSales growth analysis completed successfully.")
# ============================================================
# STEP 60 - AVERAGE ORDER VALUE & CUSTOMER SPENDING
# ============================================================

print("\n" + "=" * 60)
print("STEP 60 - AVERAGE ORDER VALUE & CUSTOMER SPENDING")
print("=" * 60)

# ------------------------------------------------------------
# 1. CREATE ORDER-LEVEL ANALYSIS
# ------------------------------------------------------------

order_analysis = df.groupby("Invoice").agg(
    Order_Revenue=("Revenue", "sum"),
    Items=("Quantity", "sum"),
    Customer=("Customer ID", "first")
).reset_index()

print("\nOrder-level analysis:")
print(order_analysis.head())


# ------------------------------------------------------------
# 2. AVERAGE ORDER VALUE
# ------------------------------------------------------------

average_order_value = order_analysis["Order_Revenue"].mean()

print("\nAverage Order Value:")
print(f"£{average_order_value:,.2f}")


# ------------------------------------------------------------
# 3. MEDIAN ORDER VALUE
# ------------------------------------------------------------

median_order_value = order_analysis["Order_Revenue"].median()

print("\nMedian Order Value:")
print(f"£{median_order_value:,.2f}")


# ------------------------------------------------------------
# 4. HIGHEST ORDER VALUE
# ------------------------------------------------------------

maximum_order_value = order_analysis["Order_Revenue"].max()

print("\nMaximum Order Value:")
print(f"£{maximum_order_value:,.2f}")


# ------------------------------------------------------------
# 5. LOWEST ORDER VALUE
# ------------------------------------------------------------

minimum_order_value = order_analysis["Order_Revenue"].min()

print("\nMinimum Order Value:")
print(f"£{minimum_order_value:,.2f}")


# ------------------------------------------------------------
# 6. TOP 10 ORDERS BY REVENUE
# ------------------------------------------------------------

top_orders = order_analysis.sort_values(
    "Order_Revenue",
    ascending=False
).head(10)

print("\nTop 10 Orders by Revenue:")
print(top_orders)


# ------------------------------------------------------------
# 7. CUSTOMER AVERAGE ORDER VALUE
# ------------------------------------------------------------

customer_spending = rfm[
    ["Recency", "Frequency", "Monetary"]
].copy()

customer_spending["Average_Order_Value"] = (
    customer_spending["Monetary"]
    / customer_spending["Frequency"]
)

print("\nTop 10 Customers by Average Order Value:")

print(
    customer_spending
    .sort_values(
        "Average_Order_Value",
        ascending=False
    )
    .head(10)
)


# ------------------------------------------------------------
# 8. CUSTOMER SPENDING STATISTICS
# ------------------------------------------------------------

print("\nCustomer Spending Statistics:")

print(
    customer_spending[
        ["Monetary", "Frequency", "Average_Order_Value"]
    ].describe()
)


# ------------------------------------------------------------
# 9. SAVE ORDER ANALYSIS
# ------------------------------------------------------------

order_analysis.to_csv(
    "data/processed/order_analysis.csv",
    index=False
)


# ------------------------------------------------------------
# 10. SAVE CUSTOMER SPENDING ANALYSIS
# ------------------------------------------------------------

customer_spending.to_csv(
    "data/processed/customer_spending_analysis.csv"
)


print("\nOrder analysis saved successfully.")
print("Customer spending analysis saved successfully.")

print("\nAverage order value and customer spending analysis completed successfully.")
# ============================================================
# STEP 61 - CUSTOMER PURCHASE BEHAVIOR ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 61 - CUSTOMER PURCHASE BEHAVIOR ANALYSIS")
print("=" * 60)

# ------------------------------------------------------------
# 1. CUSTOMER PURCHASE SUMMARY
# ------------------------------------------------------------

customer_behavior = rfm[
    ["Recency", "Frequency", "Monetary", "Customer_Segment"]
].copy()

# Average order value
customer_behavior["Average_Order_Value"] = (
    customer_behavior["Monetary"]
    / customer_behavior["Frequency"]
)

print("\nCustomer purchase behavior sample:")
print(customer_behavior.head(10))


# ------------------------------------------------------------
# 2. MOST FREQUENT CUSTOMERS
# ------------------------------------------------------------

print("\nTop 10 Most Frequent Customers:")

print(
    customer_behavior
    .sort_values(
        "Frequency",
        ascending=False
    )
    .head(10)
)


# ------------------------------------------------------------
# 3. HIGHEST SPENDING CUSTOMERS
# ------------------------------------------------------------

print("\nTop 10 Highest Spending Customers:")

print(
    customer_behavior
    .sort_values(
        "Monetary",
        ascending=False
    )
    .head(10)
)


# ------------------------------------------------------------
# 4. MOST RECENT CUSTOMERS
# ------------------------------------------------------------

print("\nTop 10 Most Recent Customers:")

print(
    customer_behavior
    .sort_values(
        "Recency",
        ascending=True
    )
    .head(10)
)


# ------------------------------------------------------------
# 5. CUSTOMER PURCHASE BEHAVIOR STATISTICS
# ------------------------------------------------------------

print("\nCustomer Purchase Behavior Statistics:")

print(
    customer_behavior[
        [
            "Recency",
            "Frequency",
            "Monetary",
            "Average_Order_Value"
        ]
    ].describe()
)


# ------------------------------------------------------------
# 6. AVERAGE METRICS BY CUSTOMER SEGMENT
# ------------------------------------------------------------

behavior_by_segment = customer_behavior.groupby(
    "Customer_Segment"
).agg(
    Customers=("Customer_Segment", "count"),
    Average_Recency=("Recency", "mean"),
    Average_Frequency=("Frequency", "mean"),
    Average_Spending=("Monetary", "mean"),
    Average_Order_Value=("Average_Order_Value", "mean")
).round(2)

print("\nPurchase Behavior by Customer Segment:")
print(behavior_by_segment)


# ------------------------------------------------------------
# 7. SAVE ANALYSIS
# ------------------------------------------------------------

customer_behavior.to_csv(
    "data/processed/customer_purchase_behavior.csv"
)

behavior_by_segment.to_csv(
    "data/processed/purchase_behavior_by_segment.csv"
)


print("\nCustomer purchase behavior analysis completed successfully.")
# ============================================================
# STEP 62 - CUSTOMER RETENTION & REPEAT PURCHASE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 62 - CUSTOMER RETENTION & REPEAT PURCHASE ANALYSIS")
print("=" * 60)

# ------------------------------------------------------------
# 1. CLASSIFY CUSTOMERS BY NUMBER OF ORDERS
# ------------------------------------------------------------

customer_orders = (
    df[df["Customer ID"].notna()]
    .groupby("Customer ID")["Invoice"]
    .nunique()
)

repeat_customers = customer_orders[customer_orders > 1]
one_time_customers = customer_orders[customer_orders == 1]

# ------------------------------------------------------------
# 2. CUSTOMER COUNTS
# ------------------------------------------------------------

total_identified_customers = customer_orders.count()

repeat_customer_count = len(repeat_customers)

one_time_customer_count = len(one_time_customers)

print("\nCustomer Retention Summary:")

print(
    f"Total Identified Customers: {total_identified_customers:,}"
)

print(
    f"Repeat Customers: {repeat_customer_count:,}"
)

print(
    f"One-Time Customers: {one_time_customer_count:,}"
)


# ------------------------------------------------------------
# 3. CUSTOMER PERCENTAGES
# ------------------------------------------------------------

repeat_customer_percentage = (
    repeat_customer_count
    / total_identified_customers
    * 100
)

one_time_customer_percentage = (
    one_time_customer_count
    / total_identified_customers
    * 100
)

print("\nRepeat Customer Percentage:")
print(f"{repeat_customer_percentage:.2f}%")

print("\nOne-Time Customer Percentage:")
print(f"{one_time_customer_percentage:.2f}%")


# ------------------------------------------------------------
# 4. ORDER FREQUENCY DISTRIBUTION
# ------------------------------------------------------------

print("\nCustomer Order Frequency Distribution:")

print(
    customer_orders
    .value_counts()
    .sort_index()
    .head(20)
)


# ------------------------------------------------------------
# 5. AVERAGE ORDERS PER CUSTOMER
# ------------------------------------------------------------

average_orders_per_customer = customer_orders.mean()

print("\nAverage Orders per Customer:")
print(f"{average_orders_per_customer:.2f}")


# ------------------------------------------------------------
# 6. MAXIMUM ORDERS BY ONE CUSTOMER
# ------------------------------------------------------------

maximum_customer_orders = customer_orders.max()

print("\nMaximum Orders by One Customer:")
print(maximum_customer_orders)


# ------------------------------------------------------------
# 7. TOP 10 REPEAT CUSTOMERS
# ------------------------------------------------------------

top_repeat_customers = (
    customer_orders
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Customers by Number of Orders:")
print(top_repeat_customers)


# ------------------------------------------------------------
# 8. SAVE RETENTION ANALYSIS
# ------------------------------------------------------------

retention_summary = pd.DataFrame({
    "Metric": [
        "Total Identified Customers",
        "Repeat Customers",
        "One-Time Customers",
        "Repeat Customer Percentage",
        "One-Time Customer Percentage",
        "Average Orders per Customer",
        "Maximum Orders by One Customer"
    ],
    "Value": [
        total_identified_customers,
        repeat_customer_count,
        one_time_customer_count,
        round(repeat_customer_percentage, 2),
        round(one_time_customer_percentage, 2),
        round(average_orders_per_customer, 2),
        maximum_customer_orders
    ]
})

retention_summary.to_csv(
    "data/processed/customer_retention_analysis.csv",
    index=False
)

top_repeat_customers.to_csv(
    "data/processed/top_repeat_customers.csv",
)

print("\nCustomer retention analysis saved successfully.")

print("\nCustomer retention and repeat purchase analysis completed successfully.")
# ============================================================
# STEP 63 - CUSTOMER RETENTION BY SEGMENT
# ============================================================

print("\n" + "=" * 60)
print("STEP 63 - CUSTOMER RETENTION BY SEGMENT")
print("=" * 60)

# Customer order counts
customer_order_count = (
    df[df["Customer ID"].notna()]
    .groupby("Customer ID")["Invoice"]
    .nunique()
    .rename("Order_Count")
)

# Combine with RFM segmentation
retention_segment = rfm[
    ["Customer_Segment"]
].join(customer_order_count)

# Classify repeat customers
retention_segment["Customer_Type"] = retention_segment[
    "Order_Count"
].apply(
    lambda x: "Repeat Customer" if x > 1 else "One-Time Customer"
)

# Segment retention summary
retention_by_segment = retention_segment.groupby(
    "Customer_Segment"
).agg(
    Total_Customers=("Customer_Segment", "count"),
    Repeat_Customers=("Customer_Type", lambda x: (x == "Repeat Customer").sum()),
    One_Time_Customers=("Customer_Type", lambda x: (x == "One-Time Customer").sum()),
    Average_Orders=("Order_Count", "mean")
).round(2)

# Repeat percentage
retention_by_segment["Repeat_Customer_Percentage"] = (
    retention_by_segment["Repeat_Customers"]
    / retention_by_segment["Total_Customers"]
    * 100
).round(2)

print("\nRetention by Customer Segment:")
print(retention_by_segment)

# Highest retention segment
highest_retention_segment = retention_by_segment[
    "Repeat_Customer_Percentage"
].idxmax()

print("\nHighest Repeat Customer Segment:")
print(highest_retention_segment)

print(
    "\nHighest Repeat Customer Percentage:"
)
print(
    retention_by_segment.loc[
        highest_retention_segment,
        "Repeat_Customer_Percentage"
    ],
    "%"
)

# Save results
retention_by_segment.to_csv(
    "data/processed/customer_retention_by_segment.csv"
)

retention_segment.to_csv(
    "data/processed/customer_retention_customer_level.csv"
)

print("\nCustomer retention by segment analysis completed successfully.")
# ============================================================
# STEP 64 - CUSTOMER RETENTION VISUALIZATION
# ============================================================

print("\n" + "=" * 60)
print("STEP 64 - CUSTOMER RETENTION VISUALIZATION")
print("=" * 60)

import matplotlib.pyplot as plt

# ------------------------------------------------------------
# CHART 1: REPEAT VS ONE-TIME CUSTOMERS
# ------------------------------------------------------------

retention_counts = pd.Series({
    "Repeat Customers": repeat_customer_count,
    "One-Time Customers": one_time_customer_count
})

plt.figure(figsize=(8, 8))

retention_counts.plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.title("Repeat vs One-Time Customers")
plt.ylabel("")
plt.tight_layout()

plt.savefig(
    "data/processed/repeat_vs_one_time_customers.png"
)

plt.show()


# ------------------------------------------------------------
# CHART 2: RETENTION BY CUSTOMER SEGMENT
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

retention_by_segment = retention_by_segment.sort_values(
    "Repeat_Customer_Percentage",
    ascending=True
)

plt.barh(
    retention_by_segment.index,
    retention_by_segment["Repeat_Customer_Percentage"]
)

plt.title("Repeat Customer Percentage by Segment")
plt.xlabel("Repeat Customer Percentage (%)")
plt.ylabel("Customer Segment")
plt.tight_layout()

plt.savefig(
    "data/processed/retention_by_customer_segment.png"
)

plt.show()


# ------------------------------------------------------------
# SAVE RETENTION ANALYSIS
# ------------------------------------------------------------

retention_by_segment.to_csv(
    "data/processed/customer_retention_by_segment.csv"
)

print("\nRetention visualizations created successfully.")
print("Charts saved in the data folder.")
# ============================================================
# STEP 65 - FINAL PROJECT SUMMARY & BUSINESS INSIGHTS
# ============================================================

print("\n" + "=" * 70)
print("STEP 65 - FINAL PROJECT SUMMARY & BUSINESS INSIGHTS")
print("=" * 70)

# ------------------------------------------------------------
# FINAL BUSINESS METRICS
# ------------------------------------------------------------

total_revenue = df["Revenue"].sum()
total_orders = df["Invoice"].nunique()
total_customers = df["Customer ID"].nunique()
total_products = df["StockCode"].nunique()
total_quantity = df["Quantity"].sum()

average_order_value = total_revenue / total_orders

repeat_customers = (
    (rfm["Frequency"] > 1).sum()
)

one_time_customers = (
    (rfm["Frequency"] == 1).sum()
)

repeat_percentage = (
    repeat_customers / total_customers * 100
)

# Best country
best_country = country_analysis.iloc[0]

# Best product
best_product = product_analysis.sort_values(
    "Total_Revenue",
    ascending=False
).iloc[0]

# Best customer
best_customer = rfm.sort_values(
    "Monetary",
    ascending=False
).iloc[0]

# Best month
best_month = monthly_sales.loc[
    monthly_sales["Total_Revenue"].idxmax()
]

# Best customer segment
best_segment = segment_performance.sort_values(
    "Total_Revenue",
    ascending=False
).iloc[0]


# ------------------------------------------------------------
# PRINT FINAL KPIs
# ------------------------------------------------------------

print("\nFINAL BUSINESS KPIs")
print("-" * 50)

print(f"Total Revenue: £{total_revenue:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Total Customers: {total_customers:,}")
print(f"Total Products: {total_products:,}")
print(f"Total Quantity Sold: {total_quantity:,}")
print(f"Average Order Value: £{average_order_value:,.2f}")

print(f"\nRepeat Customers: {repeat_customers:,}")
print(f"One-Time Customers: {one_time_customers:,}")
print(f"Repeat Customer Percentage: {repeat_percentage:.2f}%")


# ------------------------------------------------------------
# KEY BUSINESS INSIGHTS
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("KEY BUSINESS INSIGHTS")
print("=" * 70)

print("\n1. BEST COUNTRY")
print(f"Country: {best_country['Country']}")
print(f"Revenue: £{best_country['Total_Revenue']:,.2f}")

print("\n2. BEST PRODUCT")
print(f"Product: {best_product['Description']}")
print(f"Revenue: £{best_product['Total_Revenue']:,.2f}")

print("\n3. TOP CUSTOMER")
print(f"Customer ID: {best_customer.name}")
print(f"Customer Spending: £{best_customer['Monetary']:,.2f}")
print(f"Customer Frequency: {best_customer['Frequency']}")

print("\n4. BEST MONTH")
print(f"Month: {best_month['YearMonth']}")
print(f"Revenue: £{best_month['Total_Revenue']:,.2f}")

print("\n5. BEST CUSTOMER SEGMENT")
print(f"Segment: {best_segment.name}")
print(f"Customers: {best_segment['Customers']:,}")
print(f"Revenue: £{best_segment['Total_Revenue']:,.2f}")
print(f"Revenue Contribution: {best_segment['Revenue_Percentage']:.2f}%")

print("\n6. CUSTOMER RETENTION")
print(f"Repeat Customer Rate: {repeat_percentage:.2f}%")

print("\n7. MAIN BUSINESS OBSERVATION")
print(
    "VIP / Champions generate the largest share of customer revenue, "
    "making customer retention and VIP engagement important business priorities."
)

print("\n" + "=" * 70)
print("PROJECT 2 COMPLETED SUCCESSFULLY!")
print("=" * 70)

print("\nOnline Retail Data Analysis Project")
print("All 65 steps completed successfully.")
print("\n" + "=" * 70)
print("COMPLETE PROJECT OUTPUT SAVED SUCCESSFULLY")
print("=" * 70)

sys.stdout.close()