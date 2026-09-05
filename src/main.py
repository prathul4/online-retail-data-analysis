"""RetailPulse pipeline entry point.

Runs the full customer analytics workflow end to end: load raw data, clean
it, build the SQLite modeling layer, run sales/product/country analysis,
RFM + K-Means customer segmentation, cohort retention, and revenue
forecasting. All CSV/PNG outputs land in data/processed/; a full run log
is written to data/processed/full_project_output.txt.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import cleaning, cohort, config, data_loader, database, forecasting, rfm, sales_analysis


class Tee:
    """Write to multiple streams at once (console + log file)."""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)

    def flush(self):
        for stream in self.streams:
            stream.flush()


def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def run_pipeline():
    section("RETAILPULSE - CUSTOMER ANALYTICS & REVENUE INTELLIGENCE PIPELINE")

    section("1. LOAD RAW DATA")
    raw_df = data_loader.load_raw_data()
    print(f"Loaded {raw_df.shape[0]:,} rows, {raw_df.shape[1]} columns.")

    section("2. CLEAN TRANSACTIONS")
    df, cleaning_log = cleaning.clean_transactions(raw_df)
    for key, value in cleaning_log.items():
        print(f"{key}: {value}")
    product_df = cleaning.build_product_df(df)

    section("3. BUILD SQL MODELING LAYER (SQLite)")
    database.build_database(df)
    print(f"Loaded {df.shape[0]:,} clean rows into {config.DB_PATH.name}")
    sql_rfm = database.run_sql_file("02_rfm.sql")
    sql_rfm.to_csv(config.PROCESSED_DIR / "sql_rfm_scores.csv", index=False)
    print("Saved SQL-derived RFM scores -> sql_rfm_scores.csv")

    section("4. SALES, PRODUCT & COUNTRY ANALYSIS")
    simple_tables = sales_analysis.simple_sales_tables(df, product_df)
    monthly_kpis = sales_analysis.monthly_kpi_analysis()
    sales_analysis.product_performance_analysis(df)
    country_analysis = sales_analysis.country_performance_analysis(df)
    print("Sales/product/country tables and charts saved to data/processed/")

    section("5. RFM CUSTOMER ANALYSIS (RULE-BASED)")
    rfm_base = rfm.compute_rfm(df)
    rfm_segments = rfm.add_rule_based_segments(rfm_base)
    segment_performance = rfm.segment_performance_report(rfm_segments)
    rfm.purchase_behavior_by_segment(rfm_segments)
    sales_analysis.order_value_analysis(df, rfm_segments)
    print(segment_performance)

    section("6. K-MEANS CUSTOMER SEGMENTATION")
    _, kmeans_profile, k = rfm.kmeans_segmentation(rfm_base)
    print(f"Selected k={k} clusters via the elbow method")
    print(kmeans_profile)

    section("7. CUSTOMER RETENTION & COHORT ANALYSIS")
    retention_summary = cohort.repeat_customer_analysis(df, rfm_segments)
    print(f"Repeat customer rate: {retention_summary['repeat_percentage']}%")
    cohort_result = cohort.cohort_retention_matrix()
    if cohort_result["avg_month1_retention"] is not None:
        print(f"Average month-1 retention across cohorts: {cohort_result['avg_month1_retention']:.2f}%")

    section("8. REVENUE FORECASTING")
    forecast_result = forecasting.forecast_revenue(monthly_kpis, max_invoice_date=df["InvoiceDate"].max())
    if forecast_result["excluded_partial_month"] is not None:
        print(
            f"Excluded {forecast_result['excluded_partial_month']} from forecasting: "
            "raw data cuts off mid-month, making it an incomplete period."
        )
    if forecast_result["mape"] is not None:
        print(f"Backtest MAPE ({forecast_result['horizon_months']}-month holdout): {forecast_result['mape']:.2f}%")
    print(forecast_result["forecast"])

    section("9. FINAL KPIs")
    kpis = sales_analysis.compute_kpis(
        df, product_df, country_analysis, monthly_kpis, simple_tables["customer"]
    )
    for key, value in kpis.items():
        print(f"{key}: {value}")

    section("PIPELINE COMPLETED SUCCESSFULLY")
    return kpis


def main():
    config.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    with open(config.LOG_PATH, "w", encoding="utf-8") as log_file:
        original_stdout = sys.stdout
        sys.stdout = Tee(original_stdout, log_file)
        try:
            run_pipeline()
        finally:
            sys.stdout = original_stdout


if __name__ == "__main__":
    main()
