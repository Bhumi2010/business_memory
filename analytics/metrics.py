import pandas as pd

from data_loader import load_sales, load_transaction_data


# -----------------------------
# Load prepared data
# -----------------------------

sales = load_sales()
transactions = load_transaction_data()


# -----------------------------
# Revenue
# -----------------------------

total_revenue = transactions["line_total"].sum()


# -----------------------------
# Orders
# -----------------------------

total_orders = sales["sale_id"].nunique()


# -----------------------------
# Units Sold
# -----------------------------

total_units_sold = transactions["quantity"].sum()


# -----------------------------
# Average Order Value
# -----------------------------

average_order_value = total_revenue / total_orders


# -----------------------------
# Display metrics
# ----------------------------

print("BUSINESS MEMORY - METRICS")
print("--------------------------")

print(f"Total Revenue      : ₹{total_revenue:,.2f}")
print(f"Total Orders       : {total_orders:,}")
print(f"Total Units Sold   : {total_units_sold:,}")
print(f"Average Order Value: ₹{average_order_value:,.2f}")


# -----------------------------
# Monthly Revenue
# -----------------------------

monthly_revenue = (
    transactions
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