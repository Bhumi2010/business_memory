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
# Revenue by customer
# -----------------------------

customer_revenue = (
    comparison
    .groupby(
        ["customer_id", "month"]
    )["line_total"]
    .sum()
    .unstack(fill_value=0)
)


# Make sure both months exist

if july not in customer_revenue.columns:
    customer_revenue[july] = 0

if august not in customer_revenue.columns:
    customer_revenue[august] = 0


# -----------------------------
# Orders by customer
# -----------------------------

customer_orders = (
    comparison
    .groupby(
        ["customer_id", "month"]
    )["sale_id"]
    .nunique()
    .unstack(fill_value=0)
)


# Make sure both months exist

if july not in customer_orders.columns:
    customer_orders[july] = 0

if august not in customer_orders.columns:
    customer_orders[august] = 0


# -----------------------------
# Build customer dataset
# -----------------------------

customer_analysis = pd.DataFrame({

    "july_revenue":
        customer_revenue[july],

    "august_revenue":
        customer_revenue[august],

    "july_orders":
        customer_orders[july],

    "august_orders":
        customer_orders[august]
})


# -----------------------------
# Revenue metrics
# -----------------------------

customer_analysis["total_revenue"] = (
    customer_analysis["july_revenue"]
    + customer_analysis["august_revenue"]
)


customer_analysis["revenue_change"] = (
    customer_analysis["august_revenue"]
    - customer_analysis["july_revenue"]
)


customer_analysis["revenue_change_percent"] = (
    customer_analysis["revenue_change"]
    /
    customer_analysis["july_revenue"].replace(0, pd.NA)
    * 100
)


# -----------------------------
# Order metrics
# -----------------------------

customer_analysis["total_orders"] = (
    customer_analysis["july_orders"]
    + customer_analysis["august_orders"]
)


customer_analysis["order_change"] = (
    customer_analysis["august_orders"]
    - customer_analysis["july_orders"]
)


# -----------------------------
# Customer status
# -----------------------------

def determine_status(row):

    if (
        row["july_revenue"] > 0
        and row["august_revenue"] > 0
    ):
        return "Active"

    if (
        row["july_revenue"] > 0
        and row["august_revenue"] == 0
    ):
        return "Churned"

    if (
        row["july_revenue"] == 0
        and row["august_revenue"] > 0
    ):
        return "New / Returning"

    return "No Activity"


customer_analysis["status"] = (
    customer_analysis.apply(
        determine_status,
        axis=1
    )
)


# -----------------------------
# Segmentation thresholds
# -----------------------------

active_customers = customer_analysis[
    customer_analysis["status"] == "Active"
]


if not active_customers.empty:

    high_value_threshold = (
        active_customers["total_revenue"]
        .quantile(0.75)
    )

    high_frequency_threshold = (
        active_customers["total_orders"]
        .quantile(0.75)
    )

else:

    high_value_threshold = 0

    high_frequency_threshold = 0


# -----------------------------
# Customer segmentation
# -----------------------------

def determine_segment(row):

    status = row["status"]

    total_revenue = row["total_revenue"]
    total_orders = row["total_orders"]
    revenue_change = row["revenue_change"]

    # Churned customers
    if status == "Churned":

        if total_revenue >= high_value_threshold:
            return "High Value Churn"

        return "Churned"

    # New / returning customers
    if status == "New / Returning":

        if total_revenue >= high_value_threshold:
            return "High Value New/Returning"

        return "New / Returning"

    # Active customers
    if status == "Active":

        # Significant decline
        if (
            row["july_revenue"] > 0
            and row["revenue_change_percent"] <= -50
        ):
            return "At Risk"

        # High-value and frequent
        if (
            total_revenue >= high_value_threshold
            and total_orders >= high_frequency_threshold
        ):
            return "High Value Loyal"

        # High value
        if total_revenue >= high_value_threshold:
            return "High Value"

        # Frequent customers
        if total_orders >= high_frequency_threshold:
            return "Loyal"

        return "Regular Active"

    return "Other"


customer_analysis["segment"] = (
    customer_analysis.apply(
        determine_segment,
        axis=1
    )
)


# -----------------------------
# Segment summary
# -----------------------------

segment_summary = (
    customer_analysis
    .groupby("segment")
    .agg(
        customers=("segment", "size"),
        total_revenue=("total_revenue", "sum"),
        average_revenue=("total_revenue", "mean"),
        total_orders=("total_orders", "sum")
    )
    .sort_values(
        "total_revenue",
        ascending=False
    )
)


# -----------------------------
# Display analysis
# -----------------------------

print("CUSTOMER SEGMENTATION")
print("=====================")


print()
print("SEGMENT THRESHOLDS")
print("------------------")

print(
    f"High-value revenue threshold : "
    f"₹{high_value_threshold:,.2f}"
)

print(
    f"High-frequency order threshold : "
    f"{high_frequency_threshold:.0f}"
)


print()
print("CUSTOMER SEGMENTS")
print("-----------------")

for segment, row in segment_summary.iterrows():

    print()
    print(f"Segment       : {segment}")
    print(
        f"Customers     : "
        f"{row['customers']:.0f}"
    )
    print(
        f"Total Revenue : "
        f"₹{row['total_revenue']:,.2f}"
    )
    print(
        f"Avg Revenue   : "
        f"₹{row['average_revenue']:,.2f}"
    )
    print(
        f"Total Orders  : "
        f"{row['total_orders']:.0f}"
    )


# -----------------------------
# Top high-value customers
# -----------------------------

top_customers = (
    customer_analysis
    .sort_values(
        "total_revenue",
        ascending=False
    )
    .head(10)
)


print()
print("TOP 10 CUSTOMERS BY REVENUE")
print("---------------------------")

for customer_id, row in top_customers.iterrows():

    print()
    print(
        f"Customer ID : {customer_id}"
    )

    print(
        f"Total Revenue : "
        f"₹{row['total_revenue']:,.2f}"
    )

    print(
        f"Total Orders  : "
        f"{row['total_orders']:.0f}"
    )

    print(
        f"Revenue Change: "
        f"₹{row['revenue_change']:+,.2f}"
    )

    print(
        f"Status        : "
        f"{row['status']}"
    )

    print(
        f"Segment       : "
        f"{row['segment']}"
    )

    print("---------------------------")