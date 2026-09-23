import pandas as pd
import numpy as np
from pathlib import Path


# -----------------------------
# Configuration
# -----------------------------

RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)


# -----------------------------
# Paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "raw"

SALES_FILE = RAW_DATA / "sales.csv"
PRODUCTS_FILE = RAW_DATA / "products.csv"

SALE_ITEMS_FILE = RAW_DATA / "sale_items.csv"


# -----------------------------
# Load existing data
# -----------------------------

sales = pd.read_csv(SALES_FILE)

products = pd.read_csv(PRODUCTS_FILE)


# -----------------------------
# Generate sale items
# -----------------------------

sale_items = []

sale_item_counter = 1


for _, sale in sales.iterrows():

    # Each sale contains 1–5 different products
    number_of_products = np.random.randint(1, 6)

    selected_products = products.sample(
        n=number_of_products,
        replace=False
    )

    for _, product in selected_products.iterrows():

        quantity = np.random.randint(1, 21)

        unit_price = product["selling_price"]

        # Random discount between 0% and 15%
        discount = np.random.choice(
            [0, 5, 10, 15],
            p=[0.50, 0.25, 0.20, 0.05]
        )

        gross_amount = quantity * unit_price

        discount_amount = gross_amount * (discount / 100)

        line_total = gross_amount - discount_amount

        sale_items.append({
            "sale_item_id": f"SI{sale_item_counter:07d}",
            "sale_id": sale["sale_id"],
            "product_id": product["product_id"],
            "quantity": quantity,
            "unit_price": round(unit_price, 2),
            "discount_percent": discount,
            "line_total": round(line_total, 2)
        })

        sale_item_counter += 1


# -----------------------------
# Convert to DataFrame
# -----------------------------

sale_items = pd.DataFrame(sale_items)


# -----------------------------
# Save dataset
# -----------------------------

sale_items.to_csv(
    SALE_ITEMS_FILE,
    index=False
)


# -----------------------------
# Summary
# -----------------------------

print("Sale items dataset generated successfully!")
print("--------------------------------------------")
print(f"Rows           : {len(sale_items)}")
print(f"Columns        : {len(sale_items.columns)}")
print(f"Unique sales   : {sale_items['sale_id'].nunique()}")
print(f"Unique products: {sale_items['product_id'].nunique()}")
print(
    f"Total revenue  : ₹{sale_items['line_total'].sum():,.2f}"
)

print()
print("Discount distribution:")
print(sale_items["discount_percent"].value_counts().sort_index())

print()
print(f"Saved to: {SALE_ITEMS_FILE}")