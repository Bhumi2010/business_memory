import pandas as pd
from pathlib import Path


# -----------------------------
# Paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "raw"

SALES_FILE = RAW_DATA / "sales.csv"
SALE_ITEMS_FILE = RAW_DATA / "sale_items.csv"
PRODUCTS_FILE = RAW_DATA / "products.csv"


# -----------------------------
# Load data
# -----------------------------

sales = pd.read_csv(SALES_FILE)
sale_items = pd.read_csv(SALE_ITEMS_FILE)
products = pd.read_csv(PRODUCTS_FILE)


# -----------------------------
# Prepare dates
# -----------------------------

sales["sale_date"] = pd.to_datetime(sales["sale_date"])


# -----------------------------
# Attach date to sale items
# -----------------------------

sale_items = sale_items.merge(
    sales[["sale_id", "sale_date"]],
    on="sale_id",
    how="left"
)


# -----------------------------
# Attach product category
# -----------------------------

sale_items = sale_items.merge(
    products[["product_id", "category"]],
    on="product_id",
    how="left"
)


# -----------------------------
# Create month
# -----------------------------

sale_items["month"] = (
    sale_items["sale_date"]
    .dt.to_period("M")
)


# -----------------------------
# Select July & August
# -----------------------------

comparison = sale_items[
    sale_items["month"].isin(
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

category_change = (
    pd.DataFrame({
        "july_revenue": july,
        "august_revenue": august
    })
)


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