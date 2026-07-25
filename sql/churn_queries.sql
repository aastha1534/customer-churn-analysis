/* =====================================================================
   CUSTOMER CHURN ANALYSIS — SQL QUERIES
   Dataset : data/telco_customer_churn.csv  (load as table `customer_churn`)
   Dialect : ANSI SQL — tested on SQLite, works on MySQL / PostgreSQL /
             SQL Server / BigQuery with only minor date-function tweaks.

   Load into SQLite quickly:
     sqlite3 churn.db
     .mode csv
     .import data/telco_customer_churn.csv customer_churn
   ===================================================================== */

-- 1. Overall churn rate --------------------------------------------------
SELECT
    COUNT(*)                                              AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)         AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customer_churn;

-- 2. Churn rate by contract type -----------------------------------------
SELECT
    Contract,
    COUNT(*)                                              AS customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)         AS churned,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customer_churn
GROUP BY Contract
ORDER BY churn_rate_pct DESC;

-- 3. Churn rate by internet service type -----------------------------------
SELECT
    InternetService,
    COUNT(*)                                              AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2)                         AS avg_monthly_charges
FROM customer_churn
GROUP BY InternetService
ORDER BY churn_rate_pct DESC;

-- 4. Churn rate by payment method ------------------------------------------
SELECT
    PaymentMethod,
    COUNT(*)                                              AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customer_churn
GROUP BY PaymentMethod
ORDER BY churn_rate_pct DESC;

-- 5. Tenure cohort analysis (bucketed) -------------------------------------
SELECT
    CASE
        WHEN tenure <= 12 THEN '0-12 months'
        WHEN tenure <= 24 THEN '13-24 months'
        WHEN tenure <= 48 THEN '25-48 months'
        ELSE '49-72 months'
    END                                                     AS tenure_cohort,
    COUNT(*)                                                AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customer_churn
GROUP BY tenure_cohort
ORDER BY MIN(tenure);

-- 6. Revenue at risk from churned customers --------------------------------
SELECT
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS monthly_revenue_lost,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END) * 12, 2) AS annualized_revenue_lost,
    ROUND(SUM(MonthlyCharges), 2)                          AS total_monthly_revenue,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END) / SUM(MonthlyCharges), 2) AS pct_revenue_at_risk
FROM customer_churn;

-- 7. Impact of add-on services (tech support / online security) on churn --
SELECT
    TechSupport,
    OnlineSecurity,
    COUNT(*)                                                AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customer_churn
WHERE InternetService != 'No'
GROUP BY TechSupport, OnlineSecurity
ORDER BY churn_rate_pct DESC;

-- 8. Senior citizens vs. non-seniors ---------------------------------------
SELECT
    CASE WHEN SeniorCitizen = 1 THEN 'Senior' ELSE 'Non-Senior' END AS customer_group,
    COUNT(*)                                                AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2)                           AS avg_monthly_charges
FROM customer_churn
GROUP BY customer_group;

-- 9. High-value customers at risk (top 25% spend, still on month-to-month) --
WITH ranked AS (
    SELECT *,
           NTILE(4) OVER (ORDER BY MonthlyCharges) AS spend_quartile
    FROM customer_churn
)
SELECT
    customerID, tenure, Contract, MonthlyCharges, Churn
FROM ranked
WHERE spend_quartile = 4
  AND Contract = 'Month-to-month'
  AND Churn = 'Yes'
ORDER BY MonthlyCharges DESC
LIMIT 50;

-- 10. Churn rate by number of add-on services subscribed --------------------
SELECT
    (CASE WHEN OnlineSecurity   = 'Yes' THEN 1 ELSE 0 END +
     CASE WHEN OnlineBackup     = 'Yes' THEN 1 ELSE 0 END +
     CASE WHEN DeviceProtection = 'Yes' THEN 1 ELSE 0 END +
     CASE WHEN TechSupport      = 'Yes' THEN 1 ELSE 0 END +
     CASE WHEN StreamingTV      = 'Yes' THEN 1 ELSE 0 END +
     CASE WHEN StreamingMovies  = 'Yes' THEN 1 ELSE 0 END)  AS num_addons,
    COUNT(*)                                                AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customer_churn
GROUP BY num_addons
ORDER BY num_addons;

-- 11. Paperless billing vs. churn -------------------------------------------
SELECT
    PaperlessBilling,
    COUNT(*)                                                AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customer_churn
GROUP BY PaperlessBilling;

-- 12. Average tenure: churned vs. retained -----------------------------------
SELECT
    Churn,
    COUNT(*)                                                AS customers,
    ROUND(AVG(tenure), 1)                                   AS avg_tenure_months,
    ROUND(AVG(MonthlyCharges), 2)                            AS avg_monthly_charges,
    ROUND(AVG(TotalCharges), 2)                              AS avg_total_charges
FROM customer_churn
GROUP BY Churn;
