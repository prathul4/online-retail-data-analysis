-- RetailPulse: RFM scoring via window functions (NTILE quintiles).
-- Recency is computed relative to the day after the last invoice in the
-- cleaned dataset. Higher R/F/M scores are always "better" for the customer.

WITH reference_date AS (
    SELECT date(MAX(InvoiceDate), '+1 day') AS ref_date
    FROM transactions_clean
),
customer_agg AS (
    SELECT
        CustomerID,
        CAST(
            julianday((SELECT ref_date FROM reference_date))
            - julianday(MAX(InvoiceDate))
            AS INTEGER
        ) AS Recency,
        COUNT(DISTINCT Invoice) AS Frequency,
        SUM(Revenue) AS Monetary
    FROM transactions_clean
    WHERE CustomerID IS NOT NULL AND CustomerID != ''
    GROUP BY CustomerID
),
scored AS (
    SELECT
        CustomerID,
        Recency,
        Frequency,
        Monetary,
        NTILE(5) OVER (ORDER BY Recency DESC) AS R_Score,
        NTILE(5) OVER (ORDER BY Frequency ASC) AS F_Score,
        NTILE(5) OVER (ORDER BY Monetary ASC) AS M_Score
    FROM customer_agg
)
SELECT
    CustomerID,
    Recency,
    Frequency,
    Monetary,
    R_Score,
    F_Score,
    M_Score,
    (R_Score + F_Score + M_Score) AS RFM_Score,
    RANK() OVER (ORDER BY Monetary DESC) AS Spend_Rank
FROM scored
ORDER BY RFM_Score DESC;
