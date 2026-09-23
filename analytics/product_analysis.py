import pandas as pd

from data_loader import load_enriched_transactions


# -----------------------------
# Load prepared transaction data
# -----------------------------

transactions = load_enriched_transactions()


# -----------------------------
# Analyze Household
# -----------------------------

comparison = transactions[
    (transactions["category"] == "Household")
    &
    (
        transactions["month"].isin(
            [
                pd.Period("2026-07"),
                pd.Period("2026-08")
            ]
        )
    )
]


# -----------------------------
# Revenue by product and month
# -----------------------------

product_revenue = (
    comparison
    .groupby(
        [
            "product_id",
            "product_name",
            "month"
        ]
    )["line_total"]
    .sum()
    .unstack(fill_value=0)
)


# -----------------------------
# Make sure both months exist
# -----------------------------

july = pd.Period("2026-07")
august = pd.Period("2026-08")

if july not in product_revenue.columns:
    product_revenue[july] = 0

if august not in product_revenue.columns:
    product_revenue[august] = 0


# -----------------------------
# Calculate product changes
# -----------------------------

product_analysis = pd.DataFrame({
    "july_revenue": product_revenue[july],
    "august_revenue": product_revenue[august]
})


product_analysis["change_amount"] = (
    product_analysis["august_revenue"]
    - product_analysis["july_revenue"]
)


product_analysis["change_percent"] = (
    product_analysis["change_amount"]
    /
    product_analysis["july_revenue"].replace(0, pd.NA)
    * 100
)


# -----------------------------
# Sort by largest decline
# -----------------------------

declining_products = (
    product_analysis[
        product_analysis["change_amount"] < 0
    ]
    .sort_values(
        "change_amount",
        ascending=True
    )
    .head(10)
)


# -----------------------------
# Display
# -----------------------------

print("HOUSEHOLD PRODUCT ANALYSIS")
print("==========================")

print()
print("TOP DECLINING PRODUCTS")
print("-----------------------")


if declining_products.empty:

    print("No declining products found.")

else:

    for (product_id, product_name), row in declining_products.iterrows():

        print()
        print(f"Product  : {product_name}")
        print(f"ID       : {product_id}")
        print(f"July     : ₹{row['july_revenue']:,.2f}")
        print(f"August   : ₹{row['august_revenue']:,.2f}")
        print(f"Change   : ₹{row['change_amount']:+,.2f}")

        if pd.notna(row["change_percent"]):
            print(
                f"Change % : {row['change_percent']:+.2f}%"
            )

        print("-----------------------")