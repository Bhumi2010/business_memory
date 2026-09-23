import pandas as pd

from data_loader import load_sales, load_transaction_data


# -----------------------------
# Load prepared data
# -----------------------------

sales = load_sales()
transactions = load_transaction_data()


# -----------------------------
# Calculate monthly revenue
# -----------------------------

monthly_revenue = (
    transactions
    .groupby("month")["line_total"]
    .sum()
)


# -----------------------------
# Calculate monthly orders
# -----------------------------

monthly_orders = (
    sales
    .assign(
        month=sales["sale_date"].dt.to_period("M")
    )
    .groupby("month")["sale_id"]
    .nunique()
)


# -----------------------------
# Calculate monthly AOV
# -----------------------------

monthly_aov = (
    monthly_revenue / monthly_orders
)


# -----------------------------
# Create monthly summary
# -----------------------------

monthly_summary = pd.DataFrame({
    "revenue": monthly_revenue,
    "orders": monthly_orders,
    "aov": monthly_aov
})


# -----------------------------
# Calculate changes
# -----------------------------

monthly_summary["revenue_change"] = (
    monthly_summary["revenue"].pct_change() * 100
)

monthly_summary["orders_change"] = (
    monthly_summary["orders"].pct_change() * 100
)

monthly_summary["aov_change"] = (
    monthly_summary["aov"].pct_change() * 100
)


# -----------------------------
# Select latest complete event
# -----------------------------

latest_date = sales["sale_date"].max()
latest_month = latest_date.to_period("M")

complete_months = monthly_summary[
    monthly_summary.index < latest_month
]


# -----------------------------
# Select August 2026
# -----------------------------

current_month = pd.Period("2026-08")

current = complete_months.loc[current_month]

previous = complete_months.loc[current_month - 1]


# -----------------------------
# Display analysis
# -----------------------------

print("ROOT-CAUSE ANALYSIS")
print("===================")

print()
print(f"Period: {current_month}")

print()
print("REVENUE")
print(f"Previous : ₹{previous['revenue']:,.2f}")
print(f"Current  : ₹{current['revenue']:,.2f}")
print(
    f"Change   : {current['revenue_change']:+.2f}%"
)

print()
print("ORDERS")
print(f"Previous : {previous['orders']:,.0f}")
print(f"Current  : {current['orders']:,.0f}")
print(
    f"Change   : {current['orders_change']:+.2f}%"
)

print()
print("AVERAGE ORDER VALUE")
print(f"Previous : ₹{previous['aov']:,.2f}")
print(f"Current  : ₹{current['aov']:,.2f}")
print(
    f"Change   : {current['aov_change']:+.2f}%"
)


# -----------------------------
# Basic interpretation
# -----------------------------

print()
print("POSSIBLE DRIVERS")
print("-----------------")

if current["orders_change"] < 0:
    print(
        f"• Order volume decreased "
        f"by {abs(current['orders_change']):.2f}%."
    )

if current["aov_change"] < 0:
    print(
        f"• Average order value decreased "
        f"by {abs(current['aov_change']):.2f}%."
    )

if current["orders_change"] > 0:
    print(
        f"• Order volume increased "
        f"by {current['orders_change']:.2f}%."
    )

if current["aov_change"] > 0:
    print(
        f"• Average order value increased "
        f"by {current['aov_change']:.2f}%."
    )