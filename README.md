# Tableau Setup Guide

Tableau workbook files (`.twbx`) are a proprietary packaged format that only
Tableau Desktop/Public can write, so this folder ships the workbook as
**source components** — the exact calculated fields and a build guide — that
you assemble in Tableau in a few minutes.

## Steps

1. Open **Tableau Desktop** (or Tableau Public) → *Connect → Text File* →
   select `data/telco_customer_churn.csv`.
2. Confirm field types: `SeniorCitizen` → keep as number or convert to
   boolean; `MonthlyCharges` / `TotalCharges` → Number (decimal); `tenure` →
   Number (whole).
3. Create each calculated field from
   [`Calculated_Fields.txt`](./Calculated_Fields.txt) via
   *Analysis → Create Calculated Field*.
4. Build these sheets, then combine into a dashboard:

   | Sheet | Chart type | Fields |
   |---|---|---|
   | Churn Overview | Pie/Donut | `Churn` (color), `CNT(Churn)` (angle) |
   | Churn by Contract | Bar | `Contract` (rows), `Churn Rate` (columns), color = `Churn` |
   | Churn by Internet Service | Bar | `Internet Service` (rows), `Churn Rate` (columns) |
   | Tenure Cohort Trend | Line/Bar | `Tenure Cohort` (columns), `Churn Rate` (rows) |
   | Revenue at Risk | KPI text/Bar | `SUM(Revenue At Risk)` |
   | High Risk Customers | Table/Scatter | `High Risk Flag`, `Monthly Charges`, `Tenure` |

5. Assemble into **Dashboard → New Dashboard**, add filters for `Contract`,
   `Internet Service`, `Senior Citizen`, `Tenure Cohort` and set them to apply
   to all sheets using this data source.
6. Color palette: churned = `#E74C3C`, retained = `#2ECC71`, accent =
   `#1F4E78` (matches the Excel/Power BI/Python theme for a consistent
   cross-tool look).
7. Save as `Customer_Churn_Dashboard.twbx` (packaged workbook, includes the
   data extract so it's shareable standalone).

## Files in this folder
- `Calculated_Fields.txt` — every calculated field used across the sheets
