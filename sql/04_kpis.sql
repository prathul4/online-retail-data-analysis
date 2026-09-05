-- RetailPulse: monthly KPI rollup with month-over-month growth (LAG) and a
-- revenue ranking (RANK) across months.

WITH monthly AS (
    SELECT
        YearMonth,
        COUNT(DISTINCT Invoice) AS Orders,
        COUNT(DISTINCT CustomerID) AS Customers,
        SUM(Quantity) AS Quantity_Sold,
        SUM(Revenue) AS Total_Revenue
    FROM transactions_clean
    GROUP BY YearMonth
)
SELECT
    YearMonth,
    Orders,
    Customers,
    Quantity_Sold,
    Total_Revenue,
    ROUND(
        (Total_Revenue - LAG(Total_Revenue) OVER (ORDER BY YearMonth))
        / LAG(Total_Revenue) OVER (ORDER BY YearMonth) * 100,
        2
    ) AS Revenue_Growth_Pct,
    RANK() OVER (ORDER BY Total_Revenue DESC) AS Revenue_Rank
FROM monthly
ORDER BY YearMonth;
