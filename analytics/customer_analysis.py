import pandas as pd

from data_loader import load_transaction_data


# -----------------------------
# Load prepared transaction data
# -----------------------------

transactions = load_transaction_data()


# -----------------------------
# Select July & August 2026
# -----------------------------

july = pd.Period("2026-07")
august = pd.Period("2026-08")

comparison = transactions[
    transactions["month"].isin([july, august])
].copy()


# -----------------------------
# Revenue by customer and month
# -----------------------------

customer_revenue = (
    comparison
    .groupby(
        ["customer_id", "month"]
    )["line_total"]
    .sum()
    .unstack(fill_value=0)
)


# -----------------------------
# Make sure both months exist
# -----------------------------

if july not in customer_revenue.columns:
    customer_revenue[july] = 0

if august not in customer_revenue.columns:
    customer_revenue[august] = 0


# -----------------------------
# Customer revenue comparison
# -----------------------------

customer_analysis = pd.DataFrame({
    "july_revenue": customer_revenue[july],
    "august_revenue": customer_revenue[august]
})


customer_analysis["change_amount"] = (
    customer_analysis["august_revenue"]
    - customer_analysis["july_revenue"]
)


customer_analysis["change_percent"] = (
    customer_analysis["change_amount"]
    /
    customer_analysis["july_revenue"].replace(0, pd.NA)
    * 100
)


# -----------------------------
# Orders by customer and month
# -----------------------------

customer_orders = (
    comparison
    .groupby(
        ["customer_id", "month"]
    )["sale_id"]
    .nunique()
    .unstack(fill_value=0)
)


# -----------------------------
# Make sure both months exist
# -----------------------------

if july not in customer_orders.columns:
    customer_orders[july] = 0

if august not in customer_orders.columns:
    customer_orders[august] = 0


# -----------------------------
# Add order counts
# -----------------------------

customer_analysis["july_orders"] = (
    customer_orders[july]
)

customer_analysis["august_orders"] = (
    customer_orders[august]
)

customer_analysis["order_change"] = (
    customer_analysis["august_orders"]
    - customer_analysis["july_orders"]
)


# -----------------------------
# Customer activity status
# -----------------------------

def determine_status(row):

    if row["july_revenue"] > 0 and row["august_revenue"] > 0:
        return "Active"

    if row["july_revenue"] > 0 and row["august_revenue"] == 0:
        return "Inactive"

    if row["july_revenue"] == 0 and row["august_revenue"] > 0:
        return "New or Returning"

    return "No Activity"


customer_analysis["status"] = (
    customer_analysis.apply(
        determine_status,
        axis=1
    )
)


# -----------------------------
# Top declining customers
# -----------------------------

declining_customers = (
    customer_analysis[
        customer_analysis["change_amount"] < 0
    ]
    .sort_values(
        "change_amount",
        ascending=True
    )
    .head(10)
)

# -----------------------------
# Revenue impact by customer status
# -----------------------------

inactive_revenue_loss = (
    customer_analysis.loc[
        customer_analysis["status"] == "Inactive",
        "change_amount"
    ].sum()
)

active_customer_change = (
    customer_analysis.loc[
        customer_analysis["status"] == "Active",
        "change_amount"
    ].sum()
)

new_returning_revenue = (
    customer_analysis.loc[
        customer_analysis["status"] == "New or Returning",
        "august_revenue"
    ].sum()
)

# -----------------------------
# Reconcile customer changes
# -----------------------------

total_customer_change = (
    inactive_revenue_loss
    + active_customer_change
    + new_returning_revenue
)

july_total = customer_analysis["july_revenue"].sum()
august_total = customer_analysis["august_revenue"].sum()

overall_change = august_total - july_total


# -----------------------------
# Display customer analysis
# -----------------------------

print("CUSTOMER ANALYSIS")
print("=================")


# -----------------------------
# Customer status
# -----------------------------

print()
print("CUSTOMER STATUS")
print("----------------")

status_counts = customer_analysis["status"].value_counts()

for status, count in status_counts.items():
    print(f"{status:<18}: {count}")

print()
print("REVENUE IMPACT BY CUSTOMER STATUS")

print(
    f"Inactive customers : ₹{inactive_revenue_loss:,.2f}"
)

print(
    f"Active customers   : ₹{active_customer_change:,.2f}"
)

print(
    f"New/Returning      : ₹{new_returning_revenue:,.2f}"
)
print()
print("REVENUE RECONCILIATION")
print("----------------------")

print(
    f"July total revenue    : ₹{july_total:,.2f}"
)

print(
    f"August total revenue  : ₹{august_total:,.2f}"
)

print(
    f"Overall revenue change: ₹{overall_change:+,.2f}"
)

print(
    f"Customer-level change : ₹{total_customer_change:+,.2f}"
)

print(
    f"Reconciliation gap    : "
    f"₹{overall_change - total_customer_change:+,.2f}"
)


# -----------------------------
# Top declining customers
# -----------------------------

print()
print("TOP DECLINING CUSTOMERS")
print("-----------------------")

for customer_id, row in declining_customers.iterrows():

    print()
    print(f"Customer ID : {customer_id}")
    print(f"July Revenue: ₹{row['july_revenue']:,.2f}")
    print(f"August      : ₹{row['august_revenue']:,.2f}")
    print(f"Revenue Chg : ₹{row['change_amount']:+,.2f}")

    if pd.notna(row["change_percent"]):
        print(
            f"Revenue %   : {row['change_percent']:+.2f}%"
        )

    print(f"July Orders : {row['july_orders']:.0f}")
    print(f"Aug Orders  : {row['august_orders']:.0f}")
    print(f"Order Chg   : {row['order_change']:+.0f}")
    print(f"Status      : {row['status']}")

    print("-----------------------")