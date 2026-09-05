"""RFM customer analysis: metrics, rule-based segmentation, and a
K-Means clustering alternative validated with the elbow method.
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from src import config, visualize

RULE_SEGMENT_LABELS = [
    (13, "VIP / Champions"),
    (10, "Loyal Customers"),
    (7, "Potential Loyalists"),
    (5, "At Risk"),
    (0, "Lost / Hibernating"),
]

KMEANS_K_RANGE = range(2, 9)


def compute_rfm(df):
    customer_df = df[df["Customer ID"].notna()].copy()
    reference_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    rfm = customer_df.groupby("Customer ID").agg(
        Recency=("InvoiceDate", lambda x: (reference_date - x.max()).days),
        Frequency=("Invoice", "nunique"),
        Monetary=("Revenue", "sum"),
    )

    rfm.to_csv(config.PROCESSED_DIR / "rfm_customer_analysis.csv")
    return rfm


def _segment_by_score(score):
    for threshold, label in RULE_SEGMENT_LABELS:
        if score >= threshold:
            return label
    return RULE_SEGMENT_LABELS[-1][1]


def add_rule_based_segments(rfm):
    rfm = rfm.copy()
    rfm["R_Score"] = pd.qcut(rfm["Recency"], 5, labels=[5, 4, 3, 2, 1], duplicates="drop").astype(int)
    rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["RFM_Score"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]
    rfm["Customer_Segment"] = rfm["RFM_Score"].apply(_segment_by_score)

    rfm.to_csv(config.PROCESSED_DIR / "rfm_customer_segments.csv")
    return rfm


def segment_performance_report(rfm):
    performance = rfm.groupby("Customer_Segment").agg(
        Customers=("Customer_Segment", "count"),
        Total_Revenue=("Monetary", "sum"),
        Average_Revenue=("Monetary", "mean"),
        Average_Frequency=("Frequency", "mean"),
        Average_Recency=("Recency", "mean"),
    ).round(2).sort_values("Total_Revenue", ascending=False)

    performance["Revenue_Percentage"] = (
        performance["Total_Revenue"] / performance["Total_Revenue"].sum() * 100
    ).round(2)
    performance["Customer_Percentage"] = (
        performance["Customers"] / performance["Customers"].sum() * 100
    ).round(2)

    performance.to_csv(config.PROCESSED_DIR / "customer_segment_performance.csv")

    visualize.bar_chart(
        performance.index, performance["Customers"],
        "Number of Customers by RFM Segment", "Customer Segment", "Number of Customers",
        "customer_count_by_segment.png",
    )
    visualize.bar_chart(
        performance.index, performance["Total_Revenue"],
        "Total Revenue by RFM Segment", "Customer Segment", "Total Revenue",
        "revenue_by_segment.png",
    )
    visualize.pie_chart(
        performance["Revenue_Percentage"],
        "Revenue Contribution by Customer Segment", "revenue_contribution_by_segment.png",
    )

    return performance


def purchase_behavior_by_segment(rfm_segments):
    behavior = rfm_segments[["Recency", "Frequency", "Monetary", "Customer_Segment"]].copy()
    behavior["Average_Order_Value"] = behavior["Monetary"] / behavior["Frequency"]
    behavior.to_csv(config.PROCESSED_DIR / "customer_purchase_behavior.csv")

    by_segment = behavior.groupby("Customer_Segment").agg(
        Customers=("Customer_Segment", "count"),
        Average_Recency=("Recency", "mean"),
        Average_Frequency=("Frequency", "mean"),
        Average_Spending=("Monetary", "mean"),
        Average_Order_Value=("Average_Order_Value", "mean"),
    ).round(2)
    by_segment.to_csv(config.PROCESSED_DIR / "purchase_behavior_by_segment.csv")

    return behavior, by_segment


def _find_elbow_k(k_values, inertias):
    """Elbow = point of max distance from the line joining the first and last point."""
    x = np.array(k_values, dtype=float)
    y = np.array(inertias, dtype=float)
    x_norm = (x - x.min()) / (x.max() - x.min())
    y_norm = (y - y.min()) / (y.max() - y.min())

    p1, p2 = np.array([x_norm[0], y_norm[0]]), np.array([x_norm[-1], y_norm[-1]])
    line_vec = (p2 - p1) / np.linalg.norm(p2 - p1)

    distances = []
    for xi, yi in zip(x_norm, y_norm):
        p = np.array([xi, yi]) - p1
        proj = np.dot(p, line_vec) * line_vec
        distances.append(np.linalg.norm(p - proj))

    return int(x[int(np.argmax(distances))])


def _label_clusters(centroids, k):
    """Name clusters by value (top half) and by staleness (bottom half).

    Top tier is ranked by a composite Frequency+Monetary-Recency score
    (higher = better). Bottom tier is ranked by Recency alone so the most
    genuinely stale cluster is called "Lost" rather than just "lower value".
    """
    value_score = (
        centroids["Frequency"].rank() + centroids["Monetary"].rank() - centroids["Recency"].rank()
    )
    n_top = max(1, k // 2)
    top_clusters = value_score.sort_values(ascending=False).index[:n_top]
    bottom_clusters = [c for c in centroids.index if c not in top_clusters]

    mapping = {}
    top_names = ["Champions", "Loyal Customers", "Promising Customers"]
    for i, cluster in enumerate(value_score.loc[top_clusters].sort_values(ascending=False).index):
        mapping[cluster] = top_names[i] if i < len(top_names) else f"High-Value Segment {i + 1}"

    bottom_names = ["Lost", "At Risk", "Needs Attention"]
    bottom_by_recency = centroids.loc[bottom_clusters, "Recency"].sort_values(ascending=False).index
    for i, cluster in enumerate(bottom_by_recency):
        mapping[cluster] = bottom_names[i] if i < len(bottom_names) else f"Low-Value Segment {i + 1}"

    return mapping


def kmeans_segmentation(rfm):
    """K-Means clustering on standardized RFM features, k chosen via elbow method."""
    features = rfm[["Recency", "Frequency", "Monetary"]]
    scaled = StandardScaler().fit_transform(features)

    inertias = []
    for k in KMEANS_K_RANGE:
        model = KMeans(n_clusters=k, random_state=42, n_init=10).fit(scaled)
        inertias.append(model.inertia_)

    visualize.line_chart(
        list(KMEANS_K_RANGE), inertias,
        "K-Means Elbow Method for RFM Segmentation", "Number of Clusters (k)", "Inertia",
        "rfm_kmeans_elbow.png", rotation=0,
    )

    k = _find_elbow_k(list(KMEANS_K_RANGE), inertias)
    final_model = KMeans(n_clusters=k, random_state=42, n_init=10).fit(scaled)

    result = rfm.copy()
    result["Cluster"] = final_model.labels_

    centroids = result.groupby("Cluster")[["Recency", "Frequency", "Monetary"]].mean()
    mapping = _label_clusters(centroids, k)
    result["KMeans_Segment"] = result["Cluster"].map(mapping)

    result.to_csv(config.PROCESSED_DIR / "rfm_kmeans_segments.csv")

    segment_profile = result.groupby("KMeans_Segment").agg(
        Customers=("KMeans_Segment", "count"),
        Avg_Recency=("Recency", "mean"),
        Avg_Frequency=("Frequency", "mean"),
        Avg_Monetary=("Monetary", "mean"),
        Total_Revenue=("Monetary", "sum"),
    ).round(2).sort_values("Total_Revenue", ascending=False)
    segment_profile.to_csv(config.PROCESSED_DIR / "rfm_kmeans_segment_profile.csv")

    visualize.bar_chart(
        segment_profile.index, segment_profile["Total_Revenue"],
        f"K-Means Segments (k={k}): Revenue by Segment", "Segment", "Total Revenue",
        "rfm_kmeans_segment_revenue.png",
    )

    return result, segment_profile, k
