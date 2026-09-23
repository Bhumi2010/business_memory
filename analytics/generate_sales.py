import pandas as pd
import numpy as np
from pathlib import Path


# -----------------------------
# Configuration
# -----------------------------

RANDOM_SEED = 42
NUM_SALES = 10000

np.random.seed(RANDOM_SEED)


# -----------------------------
# Paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "raw"

CUSTOMERS_FILE = RAW_DATA / "customers.csv"
WAREHOUSES_FILE = RAW_DATA / "warehouses.csv"

SALES_FILE = RAW_DATA / "sales.csv"


# -----------------------------
# Load master data
# -----------------------------

customers = pd.read_csv(CUSTOMERS_FILE)
warehouses = pd.read_csv(WAREHOUSES_FILE)


# -----------------------------
# Generate sales
# -----------------------------

sale_ids = [
    f"S{i:06d}"
    for i in range(1, NUM_SALES + 1)
]

customer_ids = np.random.choice(
    customers["customer_id"],
    size=NUM_SALES
)

warehouse_ids = np.random.choice(
    warehouses["warehouse_id"],
    size=NUM_SALES,
    p=[0.7, 0.3]
)

sale_dates = pd.to_datetime(
    np.random.choice(
        pd.date_range(
            start="2025-01-01",
            end="2026-09-15"
        ),
        size=NUM_SALES
    )
)

payment_status = np.random.choice(
    ["Paid", "Pending", "Partial"],
    size=NUM_SALES,
    p=[0.75, 0.15, 0.10]
)


# -----------------------------
# Create dataframe
# -----------------------------

sales = pd.DataFrame({
    "sale_id": sale_ids,
    "customer_id": customer_ids,
    "warehouse_id": warehouse_ids,
    "sale_date": sale_dates,
    "payment_status": payment_status
})


# -----------------------------
# Sort by date
# -----------------------------

sales = sales.sort_values("sale_date").reset_index(drop=True)


# -----------------------------
# Save
# -----------------------------

sales.to_csv(SALES_FILE, index=False)


print("Sales dataset generated successfully!")
print("----------------------------------------")
print(f"Rows       : {len(sales)}")
print(f"Columns    : {len(sales.columns)}")
print(f"Date range : {sales['sale_date'].min().date()} to {sales['sale_date'].max().date()}")
print()
print("Payment status:")
print(sales["payment_status"].value_counts())
print()
print(f"Saved to: {SALES_FILE}")