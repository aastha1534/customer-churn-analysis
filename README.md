# Customer Churn Analysis — All 5 Tools

An end-to-end customer churn analysis project built with **five different
tools** — SQL, Python, Excel, Power BI, and Tableau — on a telecom customer
dataset. Each tool answers the same core business question in the way it's
best suited to: *who is churning, why, and how much revenue is at risk?*

## Business problem

Telecom providers lose a meaningful share of subscribers every month.
Acquiring a new customer costs far more than retaining one, so the goal of
this project is to quantify churn, find its strongest drivers, and flag
high-risk, high-value customers before they leave.

**Headline numbers** (see [`images/model_metrics.txt`](images/model_metrics.txt) for full model output):
| Metric | Value |
|---|---|
| Total customers | 7,043 |
| Overall churn rate | 22.3% |
| Highest-risk segment | Month-to-month + Fiber optic + <12mo tenure |
| Monthly revenue at risk | ~$113.6K |
| Best model (Random Forest) | 72.7% accuracy · 0.76 ROC-AUC |

## Project structure

```
customer-churn-project/
├── data/
│   └── telco_customer_churn.csv       # 7,043-row dataset (IBM Telco schema)
├── sql/
│   └── churn_queries.sql              # 12 analysis queries (churn rate, cohorts,
│                                       #   revenue at risk, segment breakdowns)
├── python/
│   ├── generate_data.py               # synthetic data generator
│   ├── eda_and_model.py                # EDA charts + Logistic Regression / Random Forest
│   └── requirements.txt
├── excel/
│   ├── Customer_Churn_Analysis.xlsx   # KPI dashboard, all live formulas
│   └── build_excel.py                 # regenerates the workbook from data/
├── powerbi/
│   ├── PowerQuery_M_Script.pq         # data load + transform (M)
│   ├── DAX_Measures.dax               # all KPI/analytical measures
│   └── README.md                      # step-by-step Power BI build guide
├── tableau/
│   ├── Calculated_Fields.txt          # every calculated field used
│   └── README.md                      # step-by-step Tableau build guide
├── dashboard/
│   ├── churn_dashboard.html           # standalone interactive web dashboard
│   └── dashboard_data.json            # pre-aggregated data behind it
├── images/                            # charts exported from the Python EDA
└── README.md
```

## The 5 tools

### 1. SQL — [`sql/churn_queries.sql`](sql/churn_queries.sql)
12 queries covering overall churn rate, churn by contract/internet
service/payment method, tenure-cohort analysis, revenue at risk,
add-on-service impact, and a query surfacing high-value customers who
already churned. Written in ANSI SQL, verified against SQLite; portable to
MySQL/PostgreSQL/BigQuery with only trivial syntax tweaks.

### 2. Python — [`python/`](python/)
`generate_data.py` builds the dataset; `eda_and_model.py` runs full EDA
(6 charts saved to `images/`) and trains two churn-prediction models
(Logistic Regression, Random Forest), saving a feature-importance chart,
confusion matrix, and metrics summary.

```bash
cd python
pip install -r requirements.txt
python generate_data.py      # only needed if you want to regenerate data/
python eda_and_model.py
```

### 3. Excel — [`excel/Customer_Churn_Analysis.xlsx`](excel/Customer_Churn_Analysis.xlsx)
A `RawData` sheet plus a `Dashboard` sheet with KPI cards and three
segment tables (contract, internet service, payment method) — every number
is a live `COUNTIF`/`COUNTIFS`/`AVERAGEIF`/`SUMIF` formula referencing
`RawData`, so the sheet recalculates automatically if the data changes.
Rebuild it anytime with `python excel/build_excel.py`.

### 4. Power BI — [`powerbi/`](powerbi/)
Since `.pbix` is a binary format only Power BI Desktop can save, this
folder ships the exact **Power Query M script** and **DAX measures** used,
plus a step-by-step guide in `powerbi/README.md` to assemble the report in
Power BI Desktop in a few minutes.

### 5. Tableau — [`tableau/`](tableau/)
Same approach as Power BI: `.twbx` is a packaged binary Tableau writes
itself, so this folder ships the **calculated field formulas** and a build
guide (`tableau/README.md`) to recreate the workbook in Tableau Desktop or
Tableau Public.

### Bonus: Interactive web dashboard — [`dashboard/churn_dashboard.html`](dashboard/churn_dashboard.html)
A standalone, dependency-light HTML dashboard (Chart.js) with KPI cards,
6 charts, and a high-risk-customer table — open it directly in any browser,
no server required.

## Key insights

- **Contract type is the single strongest churn driver.** Month-to-month
  customers churn at 31.5%, vs. 13.3% for one-year and 8.6% for two-year
  contracts.
- **Fiber optic customers churn more than DSL** (33.1% vs. 17.9%) despite
  paying more — likely a price/perceived-value gap worth investigating.
- **Tenure and churn are inversely related**: risk drops from 32.0%
  (0–12 months) to 10.7% (49–72 months) — the first year is the critical
  retention window.
- **Electronic check payers churn most** (26.6%); customers on automatic
  payment methods (bank transfer, credit card) churn noticeably less.
- **Zero add-on services correlates with lower churn** (12.7%) — likely a
  lower-engagement, lower-price, "nothing to lose" segment rather than a
  loyalty signal.

## About the data

This project uses a **synthetically generated dataset** (`python/generate_data.py`)
built to match the schema and statistical patterns of the widely-used public
[IBM Telco Customer Churn dataset](https://community.ibm.com/community/user/businessanalytics/blogs/steven-macko/2019/07/11/telco-customer-churn-1113) —
same columns, same realistic churn rate (~22%), same directional
relationships (contract type, tenure, and internet service driving churn).
It was generated this way so the project is fully reproducible end-to-end
with no external downloads required.

## Setup

```bash
git clone https://github.com/aastha1534/customer-churn-analysis.git
cd customer-churn-analysis
pip install -r python/requirements.txt
python python/eda_and_model.py
open dashboard/churn_dashboard.html   # or just double-click it
```

## Tech stack
`Python (pandas, scikit-learn, matplotlib, seaborn)` · `SQL` · `Excel (openpyxl)` · `Power BI (Power Query M, DAX)` · `Tableau` · `Chart.js`
