"""Customer retention analysis: repeat-purchase rates and true monthly
cohort retention (percentage of each first-purchase cohort still buying
in subsequent months).
"""

import pandas as pd

from src import config, database, visualize


def repeat_customer_analysis(df, rfm_segments):
    customer_orders = (
        df[df["Customer ID"].notna()].groupby("Customer ID")["Invoice"].nunique()
    )
    repeat_customers = customer_orders[customer_orders > 1]
    one_time_customers = customer_orders[customer_orders == 1]

    total = customer_orders.count()
    repeat_count = len(repeat_customers)
    one_time_count = len(one_time_customers)
    repeat_pct = repeat_count / total * 100
    one_time_pct = one_time_count / total * 100

    summary = pd.DataFrame({
        "Metric": [
            "Total Identified Customers", "Repeat Customers", "One-Time Customers",
            "Repeat Customer Percentage", "One-Time Customer Percentage",
            "Average Orders per Customer", "Maximum Orders by One Customer",
        ],
        "Value": [
            total, repeat_count, one_time_count,
            round(repeat_pct, 2), round(one_time_pct, 2),
            round(customer_orders.mean(), 2), customer_orders.max(),
        ],
    })
    summary.to_csv(config.PROCESSED_DIR / "customer_retention_analysis.csv", index=False)

    customer_orders.sort_values(ascending=False).head(10).to_csv(
        config.PROCESSED_DIR / "top_repeat_customers.csv"
    )

    order_count = customer_orders.rename("Order_Count")
    retention_segment = rfm_segments[["Customer_Segment"]].join(order_count)
    retention_segment["Customer_Type"] = retention_segment["Order_Count"].apply(
        lambda x: "Repeat Customer" if x > 1 else "One-Time Customer"
    )
    retention_segment.to_csv(config.PROCESSED_DIR / "customer_retention_customer_level.csv")

    by_segment = retention_segment.groupby("Customer_Segment").agg(
        Total_Customers=("Customer_Segment", "count"),
        Repeat_Customers=("Customer_Type", lambda x: (x == "Repeat Customer").sum()),
        One_Time_Customers=("Customer_Type", lambda x: (x == "One-Time Customer").sum()),
        Average_Orders=("Order_Count", "mean"),
    ).round(2)
    by_segment["Repeat_Customer_Percentage"] = (
        by_segment["Repeat_Customers"] / by_segment["Total_Customers"] * 100
    ).round(2)
    by_segment = by_segment.sort_values("Repeat_Customer_Percentage")
    by_segment.to_csv(config.PROCESSED_DIR / "customer_retention_by_segment.csv")

    visualize.pie_chart(
        pd.Series({"Repeat Customers": repeat_count, "One-Time Customers": one_time_count}),
        "Repeat vs One-Time Customers", "repeat_vs_one_time_customers.png",
    )
    visualize.bar_chart(
        by_segment.index, by_segment["Repeat_Customer_Percentage"],
        "Repeat Customer Percentage by Segment", "Repeat Customer Percentage (%)", "Customer Segment",
        "retention_by_customer_segment.png", horizontal=True,
    )

    return {
        "total_customers": int(total),
        "repeat_customers": int(repeat_count),
        "one_time_customers": int(one_time_count),
        "repeat_percentage": round(repeat_pct, 2),
        "by_segment": by_segment,
    }


def cohort_retention_matrix():
    """True monthly cohort retention: % of each cohort active N months later.

    Sources cohort/activity counts from sql/03_cohort_retention.sql, then
    pivots into a CohortMonth x months-since-first-purchase matrix in pandas.
    """
    activity = database.run_sql_file("03_cohort_retention.sql")

    activity["CohortMonth"] = pd.PeriodIndex(activity["CohortMonth"], freq="M")
    activity["OrderMonth"] = pd.PeriodIndex(activity["OrderMonth"], freq="M")
    activity["CohortIndex"] = (
        (activity["OrderMonth"].dt.year - activity["CohortMonth"].dt.year) * 12
        + (activity["OrderMonth"].dt.month - activity["CohortMonth"].dt.month)
    )

    counts = activity.pivot(index="CohortMonth", columns="CohortIndex", values="ActiveCustomers")
    cohort_sizes = counts[0]
    retention_pct = counts.divide(cohort_sizes, axis=0).mul(100).round(2)

    counts.to_csv(config.PROCESSED_DIR / "cohort_customer_counts.csv")
    retention_pct.to_csv(config.PROCESSED_DIR / "cohort_retention_matrix.csv")

    visualize.heatmap(
        retention_pct.values,
        "Monthly Cohort Retention (%)", "Months Since First Purchase", "Cohort Month",
        "cohort_retention_heatmap.png",
        xticklabels=retention_pct.columns, yticklabels=retention_pct.index.astype(str),
        cbar_label="Retention %",
    )

    month1_retention = retention_pct[1].mean() if 1 in retention_pct.columns else None
    return {"matrix": retention_pct, "avg_month1_retention": month1_retention}
