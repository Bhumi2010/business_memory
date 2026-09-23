import pandas as pd
import numpy as np


# Load clean data
customers = pd.read_csv("data/raw/customers.csv")


# Make a copy so the original remains untouched
dirty_customers = customers.copy()


# -----------------------------
# 1. Missing values
# -----------------------------

dirty_customers.loc[10, "city"] = np.nan
dirty_customers.loc[25, "customer_type"] = np.nan


# -----------------------------
# 2. Inconsistent customer names
# -----------------------------

dirty_customers.loc[40, "customer_name"] = "  " + dirty_customers.loc[40, "customer_name"]
dirty_customers.loc[41, "customer_name"] = dirty_customers.loc[41, "customer_name"].upper()


# -----------------------------
# 3. Invalid credit limits
# -----------------------------

dirty_customers.loc[50, "credit_limit"] = -50000
dirty_customers.loc[51, "credit_limit"] = 0


# -----------------------------
# 4. Invalid date
# -----------------------------

dirty_customers.loc[60, "created_at"] = "not-a-date"


# -----------------------------
# 5. Duplicate records
# -----------------------------

duplicate_rows = dirty_customers.iloc[[70, 71]].copy()

dirty_customers = pd.concat(
    [dirty_customers, duplicate_rows],
    ignore_index=True
)


# -----------------------------
# Save dirty dataset
# -----------------------------

dirty_customers.to_csv(
    "data/raw/customers_dirty.csv",
    index=False
)


print("Dirty dataset created successfully!")
print(f"Original rows: {len(customers)}")
print(f"Dirty rows: {len(dirty_customers)}")
print("\nSaved to:")
print("data/raw/customers_dirty.csv")