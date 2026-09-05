-- RetailPulse: monthly cohort activity counts.
-- Each customer's cohort is their first-purchase month; this query returns
-- the distinct active-customer count per (cohort month, activity month)
-- pair. The retention-percentage matrix itself is computed in Python
-- (src/cohort.py) since it needs a pivot the customer would otherwise have
-- to fake with conditional aggregation across an unbounded number of months.

WITH customer_orders AS (
    SELECT DISTINCT
        CustomerID,
        strftime('%Y-%m', InvoiceDate) AS OrderMonth
    FROM transactions_clean
    WHERE CustomerID IS NOT NULL AND CustomerID != ''
),
first_purchase AS (
    SELECT
        CustomerID,
        MIN(OrderMonth) AS CohortMonth
    FROM customer_orders
    GROUP BY CustomerID
)
SELECT
    f.CohortMonth,
    co.OrderMonth,
    COUNT(DISTINCT co.CustomerID) AS ActiveCustomers
FROM customer_orders co
JOIN first_purchase f ON f.CustomerID = co.CustomerID
GROUP BY f.CohortMonth, co.OrderMonth
ORDER BY f.CohortMonth, co.OrderMonth;
