"""Sales, product, country, and order-level analysis and charts."""

import pandas as pd

from src import config, database, visualize


def simple_sales_tables(df, product_df):
    """Single-metric 'Sales Amount' tables used for the headline charts."""
    monthly = (
        df.groupby("YearMonth", as_index=False)["Revenue"]
        .sum()
        .rename(columns={"Revenue": "Sales Amount"})
    )
    monthly["YearMonth"] = monthly["YearMonth"].astype(str)

    country = (
        df.groupby("Country", as_index=False)["Revenue"].sum()
        .rename(columns={"Revenue": "Sales Amount"})
        .sort_values("Sales Amount", ascending=False)
    )

    product = (
        product_df.groupby(["StockCode", "Description"], as_index=False)["Revenue"].sum()
        .rename(columns={"Revenue": "Sales Amount"})
        .sort_values("Sales Amount", ascending=False)
    )

    customer = (
        df[df["Customer ID"].notna()]
        .groupby("Customer ID", as_index=False)["Revenue"].sum()
        .rename(columns={"Revenue": "Sales Amount"})
        .sort_values("Sales Amount", ascending=False)
    )

    country.to_csv(config.PROCESSED_DIR / "country_sales.csv", index=False)
    product.to_csv(config.PROCESSED_DIR / "product_sales.csv", index=False)
    customer.to_csv(config.PROCESSED_DIR / "customer_sales.csv", index=False)

    visualize.line_chart(
        monthly["YearMonth"], monthly["Sales Amount"],
        "Monthly Sales Trend", "Month", "Sales Amount", "monthly_sales_trend.png",
    )
    visualize.bar_chart(
        country["Country"].head(10)[::-1], country["Sales Amount"].head(10)[::-1],
        "Top 10 Countries by Sales", "Sales Amount", "Country",
        "top_10_countries.png", horizontal=True,
    )
    labels = product["Description"].head(10).fillna("Unknown").str[:30]
    visualize.bar_chart(
        labels[::-1], product["Sales Amount"].head(10)[::-1],
        "Top 10 Products by Sales", "Sales Amount", "Product",
        "top_10_products.png", horizontal=True,
    )
    visualize.bar_chart(
        customer["Customer ID"].head(10).astype(str), customer["Sales Amount"].head(10),
        "Top 10 Customers by Sales", "Customer ID", "Sales Amount",
        "top_10_customers.png",
    )

    return {"monthly": monthly, "country": country, "product": product, "customer": customer}


def monthly_kpi_analysis():
    """Monthly Orders/Customers/Revenue + MoM growth, sourced from SQL (04_kpis.sql)."""
    monthly = database.run_sql_file("04_kpis.sql")

    monthly.drop(columns=["Revenue_Growth_Pct", "Revenue_Rank"]).to_csv(
        config.PROCESSED_DIR / "monthly_sales.csv", index=False
    )
    monthly.rename(columns={"Revenue_Growth_Pct": "Revenue_Growth_%"}).to_csv(
        config.PROCESSED_DIR / "monthly_sales_growth.csv", index=False
    )

    visualize.line_chart(
        monthly["YearMonth"], monthly["Total_Revenue"],
        "Monthly Revenue Trend", "Month", "Total Revenue", "monthly_revenue_trend.png",
    )
    visualize.line_chart(
        monthly["YearMonth"], monthly["Orders"],
        "Monthly Orders Trend", "Month", "Number of Orders", "monthly_orders_trend.png",
    )

    return monthly


def product_performance_analysis(df):
    product_analysis = df.groupby(["StockCode", "Description"]).agg(
        Total_Quantity=("Quantity", "sum"),
        Total_Revenue=("Revenue", "sum"),
        Average_Price=("Price", "mean"),
        Transactions=("Invoice", "nunique"),
    ).reset_index()

    top_revenue = product_analysis.sort_values("Total_Revenue", ascending=False).head(10)
    top_quantity = product_analysis.sort_values("Total_Quantity", ascending=False).head(10)
    top_transactions = product_analysis.sort_values("Transactions", ascending=False).head(10)

    product_analysis.to_csv(config.PROCESSED_DIR / "product_analysis.csv", index=False)
    top_revenue.to_csv(config.PROCESSED_DIR / "top_10_products_revenue.csv", index=False)
    top_quantity.to_csv(config.PROCESSED_DIR / "top_10_products_quantity.csv", index=False)

    visualize.bar_chart(
        top_revenue["Description"].astype(str), top_revenue["Total_Revenue"],
        "Top 10 Products by Revenue", "Total Revenue", "Product",
        "top_10_products_revenue.png", horizontal=True, invert=True, figsize=(12, 7),
    )
    visualize.bar_chart(
        top_quantity["Description"].astype(str), top_quantity["Total_Quantity"],
        "Top 10 Products by Quantity Sold", "Quantity Sold", "Product",
        "top_10_products_quantity.png", horizontal=True, invert=True, figsize=(12, 7),
    )
    visualize.bar_chart(
        top_transactions["Description"].astype(str), top_transactions["Transactions"],
        "Top 10 Products by Transactions", "Number of Transactions", "Product",
        "top_10_products_transactions.png", horizontal=True, invert=True, figsize=(12, 7),
    )

    return product_analysis


def country_performance_analysis(df):
    country_analysis = df.groupby("Country").agg(
        Customers=("Customer ID", "nunique"),
        Orders=("Invoice", "nunique"),
        Quantity_Sold=("Quantity", "sum"),
        Total_Revenue=("Revenue", "sum"),
    ).reset_index().sort_values("Total_Revenue", ascending=False)

    country_analysis["Revenue_Percentage"] = (
        country_analysis["Total_Revenue"] / country_analysis["Total_Revenue"].sum() * 100
    ).round(2)

    country_analysis.to_csv(config.PROCESSED_DIR / "country_analysis.csv", index=False)

    top_10 = country_analysis.head(10)
    top_10_by_customers = country_analysis.sort_values("Customers", ascending=False).head(10)

    visualize.bar_chart(
        top_10["Country"], top_10["Total_Revenue"],
        "Top 10 Countries by Revenue", "Total Revenue", "Country",
        "top_10_countries_revenue.png", horizontal=True, invert=True, figsize=(12, 7),
    )
    visualize.bar_chart(
        top_10_by_customers["Country"], top_10_by_customers["Customers"],
        "Top 10 Countries by Number of Customers", "Number of Customers", "Country",
        "top_10_countries_customers.png", horizontal=True, invert=True, figsize=(12, 7),
    )

    return country_analysis


def order_value_analysis(df, rfm):
    order_analysis = df.groupby("Invoice").agg(
        Order_Revenue=("Revenue", "sum"),
        Items=("Quantity", "sum"),
        Customer=("Customer ID", "first"),
    ).reset_index()
    order_analysis.to_csv(config.PROCESSED_DIR / "order_analysis.csv", index=False)

    customer_spending = rfm[["Recency", "Frequency", "Monetary"]].copy()
    customer_spending["Average_Order_Value"] = (
        customer_spending["Monetary"] / customer_spending["Frequency"]
    )
    customer_spending.to_csv(config.PROCESSED_DIR / "customer_spending_analysis.csv")

    return order_analysis, customer_spending


def compute_kpis(df, product_df, country_analysis, monthly_kpis, customer_sales):
    real_product_sales = (
        product_df.groupby(["StockCode", "Description"])["Revenue"]
        .sum().sort_values(ascending=False)
    )

    total_sales = df["Revenue"].sum()
    total_transactions = df["Invoice"].nunique()

    best_month_row = monthly_kpis.loc[monthly_kpis["Total_Revenue"].idxmax()]
    best_country_row = country_analysis.iloc[0]
    best_product_key = real_product_sales.idxmax()
    best_customer_id = customer_sales.iloc[0]["Customer ID"]

    return {
        "total_sales": round(float(total_sales), 2),
        "total_quantity": int(df["Quantity"].sum()),
        "total_transactions": int(total_transactions),
        "total_products": int(df["StockCode"].nunique()),
        "total_customers": int(df["Customer ID"].nunique()),
        "average_order_value": round(float(total_sales / total_transactions), 2),
        "best_country": best_country_row["Country"],
        "best_country_revenue": round(float(best_country_row["Total_Revenue"]), 2),
        "best_month": best_month_row["YearMonth"],
        "best_month_revenue": round(float(best_month_row["Total_Revenue"]), 2),
        "best_product": best_product_key[1],
        "best_product_revenue": round(float(real_product_sales.max()), 2),
        "best_customer_id": best_customer_id,
        "best_customer_revenue": round(float(customer_sales.iloc[0]["Sales Amount"]), 2),
    }
