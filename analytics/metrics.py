import pandas as pd
from pathlib import Path


# -----------------------------
# Paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "raw"

SALES_FILE = RAW_DATA / "sales.csv"
SALE_ITEMS_FILE = RAW_DATA / "sale_items.csv"


# -----------------------------
# Load transaction data
# -----------------------------

sales = pd.read_csv(SALES_FILE)
sale_items = pd.read_csv(SALE_ITEMS_FILE)


# -----------------------------
# Revenue
# -----------------------------

total_revenue = sale_items["line_total"].sum()


# -----------------------------
# Orders
# -----------------------------

total_orders = sales["sale_id"].nunique()


# -----------------------------
# Units Sold
# -----------------------------

total_units_sold = sale_items["quantity"].sum()


# -----------------------------
# Average Order Value
# -----------------------------

average_order_value = total_revenue / total_orders


# -----------------------------
# Display metrics
# -----------------------------

print("BUSINESS MEMORY - METRICS")
print("--------------------------")

print(f"Total Revenue      : ₹{total_revenue:,.2f}")
print(f"Total Orders       : {total_orders:,}")
print(f"Total Units Sold   : {total_units_sold:,}")
print(f"Average Order Value: ₹{average_order_value:,.2f}")


# -----------------------------
# Monthly Revenue
# -----------------------------

sales["sale_date"] = pd.to_datetime(sales["sale_date"])

sale_items_with_dates = sale_items.merge(
    sales[["sale_id", "sale_date"]],
    on="sale_id",
    how="left"
)

sale_items_with_dates["month"] = (
    sale_items_with_dates["sale_date"]
    .dt.to_period("M")
)

monthly_revenue = (
    sale_items_with_dates
    .groupby("month")["line_total"]
    .sum()
    .sort_index()
)


# -----------------------------
# Display monthly revenue
# -----------------------------

print()
print("MONTHLY REVENUE")
print("----------------")

for month, revenue in monthly_revenue.items():
    print(f"{month}: ₹{revenue:,.2f}")


    # -----------------------------
# Month-over-Month Revenue Change
# -----------------------------

monthly_change = monthly_revenue.pct_change() * 100

print()
print("MONTH-OVER-MONTH REVENUE CHANGE")
print("--------------------------------")

for month, change in monthly_change.items():

    if pd.isna(change):
        print(f"{month}: N/A")

    else:
        print(f"{month}: {change:+.2f}%")