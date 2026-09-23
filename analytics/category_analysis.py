import pandas as pd

from data_loader import load_enriched_transactions


# -----------------------------
# Load prepared transaction data
# -----------------------------

transactions = load_enriched_transactions()


# -----------------------------
# Select July & August
# -----------------------------

comparison = transactions[
    transactions["month"].isin(
        [
            pd.Period("2026-07"),
            pd.Period("2026-08")
        ]
    )
]


# -----------------------------
# Revenue by category
# -----------------------------

category_revenue = (
    comparison
    .groupby(["month", "category"])["line_total"]
    .sum()
    .unstack(fill_value=0)
)


# -----------------------------
# Calculate change
# -----------------------------

july = category_revenue.loc[pd.Period("2026-07")]

august = category_revenue.loc[pd.Period("2026-08")]

category_change = pd.DataFrame({
    "july_revenue": july,
    "august_revenue": august
})


category_change["change_amount"] = (
    category_change["august_revenue"]
    - category_change["july_revenue"]
)


category_change["change_percent"] = (
    category_change["change_amount"]
    / category_change["july_revenue"]
    * 100
)


# -----------------------------
# Sort by absolute impact
# -----------------------------

category_change["absolute_impact"] = (
    category_change["change_amount"].abs()
)

category_change = category_change.sort_values(
    "absolute_impact",
    ascending=False
)


# -----------------------------
# Display
# -----------------------------

print("CATEGORY REVENUE ANALYSIS")
print("=========================")

for category, row in category_change.iterrows():

    print()
    print(f"Category : {category}")
    print(f"July     : ₹{row['july_revenue']:,.2f}")
    print(f"August   : ₹{row['august_revenue']:,.2f}")
    print(f"Change   : ₹{row['change_amount']:+,.2f}")
    print(f"Change % : {row['change_percent']:+.2f}%")
    print("-------------------------")