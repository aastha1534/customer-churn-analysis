"""
generate_data.py
-----------------
Generates a realistic, synthetic Telco Customer Churn dataset that follows
the same schema as the widely-used IBM Telco Customer Churn dataset.
Churn probability is driven by realistic business logic (contract type,
tenure, internet service, monthly charges, support add-ons, etc.) so that
every downstream tool (SQL, Excel, Power BI, Tableau, Python ML) produces
sensible, consistent insights.

Run:
    python generate_data.py
Output:
    ../data/telco_customer_churn.csv
"""

import numpy as np
import pandas as pd

np.random.seed(42)

N = 7043  # same row count as the classic IBM Telco dataset

genders = np.random.choice(["Male", "Female"], N)
senior = np.random.choice([0, 1], N, p=[0.84, 0.16])
partner = np.random.choice(["Yes", "No"], N, p=[0.48, 0.52])
dependents = np.random.choice(["Yes", "No"], N, p=[0.30, 0.70])

tenure = np.random.gamma(shape=2.0, scale=16, size=N).astype(int)
tenure = np.clip(tenure, 0, 72)

phone_service = np.random.choice(["Yes", "No"], N, p=[0.90, 0.10])
multiple_lines = np.where(
    phone_service == "No", "No phone service",
    np.random.choice(["Yes", "No"], N, p=[0.42, 0.58])
)

internet_service = np.random.choice(
    ["DSL", "Fiber optic", "No"], N, p=[0.34, 0.44, 0.22]
)

def addon(col_bias):
    return np.where(
        internet_service == "No", "No internet service",
        np.random.choice(["Yes", "No"], N, p=[col_bias, 1 - col_bias])
    )

online_security = addon(0.29)
online_backup = addon(0.34)
device_protection = addon(0.34)
tech_support = addon(0.29)
streaming_tv = addon(0.38)
streaming_movies = addon(0.39)

contract = np.random.choice(
    ["Month-to-month", "One year", "Two year"], N, p=[0.55, 0.21, 0.24]
)
paperless_billing = np.random.choice(["Yes", "No"], N, p=[0.59, 0.41])
payment_method = np.random.choice(
    ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
    N, p=[0.34, 0.23, 0.22, 0.21]
)

# ---- Monthly charges: base + add-ons ----
base = np.where(internet_service == "Fiber optic", 70,
        np.where(internet_service == "DSL", 45, 20))
addon_cost = (
    (online_security == "Yes") * 5 + (online_backup == "Yes") * 5 +
    (device_protection == "Yes") * 5 + (tech_support == "Yes") * 5 +
    (streaming_tv == "Yes") * 8 + (streaming_movies == "Yes") * 8 +
    (multiple_lines == "Yes") * 6
)
noise = np.random.normal(0, 5, N)
monthly_charges = np.clip(base + addon_cost + noise, 18.25, 118.75).round(2)

total_charges = np.clip(monthly_charges * tenure + np.random.normal(0, 20, N), 0, None).round(2)
total_charges = np.where(tenure == 0, 0.0, total_charges)

# ---- Churn probability (business logic) ----
logit = (
    -3.0
    + 1.9 * (contract == "Month-to-month")
    + 0.6 * (contract == "One year")
    + 0.0 * (contract == "Two year")
    + 0.9 * (internet_service == "Fiber optic")
    - 0.6 * (internet_service == "No")
    - 0.03 * tenure
    + 0.012 * monthly_charges
    - 0.5 * (tech_support == "Yes")
    - 0.4 * (online_security == "Yes")
    + 0.35 * (paperless_billing == "Yes")
    + 0.45 * (payment_method == "Electronic check")
    + 0.3 * (senior == 1)
    - 0.25 * (partner == "Yes")
    - 0.2 * (dependents == "Yes")
    + np.random.normal(0, 0.6, N)
)
prob = 1 / (1 + np.exp(-logit))
churn = (np.random.rand(N) < prob).astype(int)
churn_label = np.where(churn == 1, "Yes", "No")

customer_id = [f"{np.random.randint(1000,9999)}-{''.join(np.random.choice(list('ABCDEFGHJKLMNPQRSTUVWXYZ'), 5))}" for _ in range(N)]

df = pd.DataFrame({
    "customerID": customer_id,
    "gender": genders,
    "SeniorCitizen": senior,
    "Partner": partner,
    "Dependents": dependents,
    "tenure": tenure,
    "PhoneService": phone_service,
    "MultipleLines": multiple_lines,
    "InternetService": internet_service,
    "OnlineSecurity": online_security,
    "OnlineBackup": online_backup,
    "DeviceProtection": device_protection,
    "TechSupport": tech_support,
    "StreamingTV": streaming_tv,
    "StreamingMovies": streaming_movies,
    "Contract": contract,
    "PaperlessBilling": paperless_billing,
    "PaymentMethod": payment_method,
    "MonthlyCharges": monthly_charges,
    "TotalCharges": total_charges,
    "Churn": churn_label,
})

df.drop_duplicates(subset="customerID", inplace=True)
df.to_csv("../data/telco_customer_churn.csv", index=False)
print(f"Generated {len(df)} rows -> ../data/telco_customer_churn.csv")
print(df["Churn"].value_counts(normalize=True).round(3))
