import pandas as pd

from data_loader import load_enriched_transactions


# -----------------------------
# Load prepared transaction data
# -----------------------------

transactions = load_enriched_transactions()


# -----------------------------
# Select July & August 2026
# -----------------------------

july = pd.Period("2026-07")
august = pd.Period("2026-08")

comparison = transactions[
    transactions["month"].isin([july, august])
].copy()


# ============================================================
# CATEGORY ANALYSIS
# ============================================================

category_revenue = (
    comparison
    .groupby(
        ["category", "month"]
    )["line_total"]
    .sum()
    .unstack(fill_value=0)
)


# Make sure both months exist

if july not in category_revenue.columns:
    category_revenue[july] = 0

if august not in category_revenue.columns:
    category_revenue[august] = 0


category_analysis = pd.DataFrame({
    "july_revenue": category_revenue[july],
    "august_revenue": category_revenue[august]
})


category_analysis["change_amount"] = (
    category_analysis["august_revenue"]
    - category_analysis["july_revenue"]
)


category_analysis["change_percent"] = (
    category_analysis["change_amount"]
    /
    category_analysis["july_revenue"].replace(0, pd.NA)
    * 100
)


# -----------------------------
# Category totals
# -----------------------------

category_analysis["total_revenue"] = (
    category_analysis["july_revenue"]
    + category_analysis["august_revenue"]
)


# ============================================================
# PRODUCT ANALYSIS
# ============================================================

product_revenue = (
    comparison
    .groupby(
        [
            "product_id",
            "product_name",
            "category",
            "month"
        ]
    )["line_total"]
    .sum()
    .unstack(fill_value=0)
)


# Make sure both months exist

if july not in product_revenue.columns:
    product_revenue[july] = 0

if august not in product_revenue.columns:
    product_revenue[august] = 0


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


product_analysis["total_revenue"] = (
    product_analysis["july_revenue"]
    + product_analysis["august_revenue"]
)


# ============================================================
# DISPLAY CATEGORY ANALYSIS
# ============================================================

print("PRODUCT & CATEGORY ANALYSIS")
print("===========================")


print()
print("CATEGORY PERFORMANCE")
print("--------------------")


category_display = (
    category_analysis
    .sort_values(
        "total_revenue",
        ascending=False
    )
)


for category, row in category_display.iterrows():

    print()
    print(f"Category       : {category}")

    print(
        f"July Revenue   : "
        f"₹{row['july_revenue']:,.2f}"
    )

    print(
        f"August Revenue : "
        f"₹{row['august_revenue']:,.2f}"
    )

    print(
        f"Change         : "
        f"₹{row['change_amount']:+,.2f}"
    )

    if pd.notna(row["change_percent"]):

        print(
            f"Change %       : "
            f"{row['change_percent']:+.2f}%"
        )

    print("--------------------")


# ============================================================
# TOP GROWING CATEGORIES
# ============================================================

growing_categories = (
    category_analysis[
        category_analysis["change_amount"] > 0
    ]
    .sort_values(
        "change_amount",
        ascending=False
    )
    .head(5)
)


print()
print("TOP GROWING CATEGORIES")
print("----------------------")


if growing_categories.empty:

    print("No growing categories found.")

else:

    for category, row in growing_categories.iterrows():

        print()
        print(f"Category : {category}")

        print(
            f"Growth   : "
            f"₹{row['change_amount']:+,.2f}"
        )

        if pd.notna(row["change_percent"]):

            print(
                f"Growth % : "
                f"{row['change_percent']:+.2f}%"
            )

        print("----------------------")


# ============================================================
# TOP DECLINING CATEGORIES
# ============================================================

declining_categories = (
    category_analysis[
        category_analysis["change_amount"] < 0
    ]
    .sort_values(
        "change_amount",
        ascending=True
    )
    .head(5)
)


print()
print("TOP DECLINING CATEGORIES")
print("------------------------")


if declining_categories.empty:

    print("No declining categories found.")

else:

    for category, row in declining_categories.iterrows():

        print()
        print(f"Category : {category}")

        print(
            f"Decline  : "
            f"₹{row['change_amount']:+,.2f}"
        )

        if pd.notna(row["change_percent"]):

            print(
                f"Change % : "
                f"{row['change_percent']:+.2f}%"
            )

        print("------------------------")


# ============================================================
# TOP GROWING PRODUCTS
# ============================================================

growing_products = (
    product_analysis[
        product_analysis["change_amount"] > 0
    ]
    .sort_values(
        "change_amount",
        ascending=False
    )
    .head(10)
)


print()
print("TOP 10 GROWING PRODUCTS")
print("-----------------------")


if growing_products.empty:

    print("No growing products found.")

else:

    for (
        product_id,
        product_name,
        category
    ), row in growing_products.iterrows():

        print()
        print(f"Product  : {product_name}")
        print(f"ID       : {product_id}")
        print(f"Category : {category}")

        print(
            f"July     : "
            f"₹{row['july_revenue']:,.2f}"
        )

        print(
            f"August   : "
            f"₹{row['august_revenue']:,.2f}"
        )

        print(
            f"Growth   : "
            f"₹{row['change_amount']:+,.2f}"
        )

        if pd.notna(row["change_percent"]):

            print(
                f"Growth % : "
                f"{row['change_percent']:+.2f}%"
            )

        print("-----------------------")


# ============================================================
# TOP DECLINING PRODUCTS
# ============================================================

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


print()
print("TOP 10 DECLINING PRODUCTS")
print("-------------------------")


if declining_products.empty:

    print("No declining products found.")

else:

    for (
        product_id,
        product_name,
        category
    ), row in declining_products.iterrows():

        print()
        print(f"Product  : {product_name}")
        print(f"ID       : {product_id}")
        print(f"Category : {category}")

        print(
            f"July     : "
            f"₹{row['july_revenue']:,.2f}"
        )

        print(
            f"August   : "
            f"₹{row['august_revenue']:,.2f}"
        )

        print(
            f"Change   : "
            f"₹{row['change_amount']:+,.2f}"
        )

        if pd.notna(row["change_percent"]):

            print(
                f"Change % : "
                f"{row['change_percent']:+.2f}%"
            )

        print("-------------------------")