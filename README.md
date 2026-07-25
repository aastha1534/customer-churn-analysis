# Power BI Setup Guide

Power BI report files (`.pbix`) are a proprietary binary format that can only
be saved by Power BI Desktop itself, so this folder ships the report as
**source components** you import in a few minutes rather than a pre-built
binary — this also means you can inspect every transform and measure before
running it, instead of trusting an opaque file.

## Steps

1. Open **Power BI Desktop** → *Get Data* → *Text/CSV* → select
   `data/telco_customer_churn.csv`. Click **Transform Data** (not Load).
2. In Power Query Editor: *Home → Advanced Editor*, replace the contents with
   [`PowerQuery_M_Script.pq`](./PowerQuery_M_Script.pq) (update the file path
   on the first line to match your machine), click **Done → Close & Apply**.
3. Go to **Model view** → *New Measure* and paste in each measure from
   [`DAX_Measures.dax`](./DAX_Measures.dax) one at a time.
4. Build the report page using these suggested visuals:

   | Visual | Fields |
   |---|---|
   | KPI Cards | `Total Customers`, `Churn Rate`, `Monthly Revenue at Risk` |
   | Donut chart | `Churn` (legend), `Total Customers` (values) |
   | Stacked bar | `Contract` (axis), `Churn Rate` (values), split by `Churn` |
   | Stacked bar | `InternetService` (axis), `Churn Rate` (values) |
   | Line/column | `TenureCohort` (axis), `Churn Rate` (values) |
   | Table | `PaymentMethod`, `Churn Rate`, `Total Customers` |
   | Slicers | `Contract`, `InternetService`, `SeniorCitizen`, `TenureCohort` |

5. Apply the color theme: churned = `#E74C3C`, retained = `#2ECC71`,
   accent = `#1F4E78` (View → Themes → Customize current theme).
6. Save as `Customer_Churn_Dashboard.pbix`.

## Files in this folder
- `PowerQuery_M_Script.pq` — data load + transform (cohort bucket, churn flag, add-on count)
- `DAX_Measures.dax` — all KPI and analytical measures
- `powerbi_layout_reference.png` — wireframe reference for page layout (see /images)
