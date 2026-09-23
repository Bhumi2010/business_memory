import pandas as pd

from data_loader import (
    load_sales,
    load_transaction_data,
    load_enriched_transactions
)


# ============================================================
# LOAD DATA
# ============================================================

sales = load_sales()
transactions = load_transaction_data()
enriched_transactions = load_enriched_transactions()


# ============================================================
# PERIODS
# ============================================================

previous_month = pd.Period("2026-07")
current_month = pd.Period("2026-08")


# ============================================================
# 1. OVERALL BUSINESS METRICS
# ============================================================

monthly_revenue = (
    transactions
    .groupby("month")["line_total"]
    .sum()
)

monthly_orders = (
    sales
    .assign(
        month=sales["sale_date"].dt.to_period("M")
    )
    .groupby("month")["sale_id"]
    .nunique()
)

monthly_aov = (
    monthly_revenue
    / monthly_orders
)


previous_revenue = monthly_revenue.get(
    previous_month,
    0
)

current_revenue = monthly_revenue.get(
    current_month,
    0
)

previous_orders = monthly_orders.get(
    previous_month,
    0
)

current_orders = monthly_orders.get(
    current_month,
    0
)

previous_aov = monthly_aov.get(
    previous_month,
    0
)

current_aov = monthly_aov.get(
    current_month,
    0
)


revenue_change = (
    current_revenue
    - previous_revenue
)

orders_change = (
    current_orders
    - previous_orders
)

aov_change = (
    current_aov
    - previous_aov
)


revenue_change_percent = (
    revenue_change
    / previous_revenue
    * 100
    if previous_revenue != 0
    else 0
)

orders_change_percent = (
    orders_change
    / previous_orders
    * 100
    if previous_orders != 0
    else 0
)

aov_change_percent = (
    aov_change
    / previous_aov
    * 100
    if previous_aov != 0
    else 0
)


# ============================================================
# 2. CUSTOMER-LEVEL REVENUE MOVEMENT
# ============================================================

customer_revenue = (
    transactions[
        transactions["month"].isin(
            [
                previous_month,
                current_month
            ]
        )
    ]
    .groupby(
        ["customer_id", "month"]
    )["line_total"]
    .sum()
    .unstack(fill_value=0)
)


if previous_month not in customer_revenue.columns:
    customer_revenue[previous_month] = 0

if current_month not in customer_revenue.columns:
    customer_revenue[current_month] = 0


customer_revenue_change = (
    customer_revenue[current_month]
    - customer_revenue[previous_month]
)


# ------------------------------------------------------------
# Customer groups
# ------------------------------------------------------------

customer_status = pd.DataFrame({

    "previous_revenue":
        customer_revenue[previous_month],

    "current_revenue":
        customer_revenue[current_month]

})


def determine_customer_status(row):

    if (
        row["previous_revenue"] > 0
        and row["current_revenue"] > 0
    ):
        return "Active"

    if (
        row["previous_revenue"] > 0
        and row["current_revenue"] == 0
    ):
        return "Churned"

    if (
        row["previous_revenue"] == 0
        and row["current_revenue"] > 0
    ):
        return "New / Returning"

    return "No Activity"


customer_status["status"] = (
    customer_status.apply(
        determine_customer_status,
        axis=1
    )
)


churned_revenue_loss = (
    customer_status.loc[
        customer_status["status"] == "Churned",
        "current_revenue"
    ]
    -
    customer_status.loc[
        customer_status["status"] == "Churned",
        "previous_revenue"
    ]
).sum()


active_customer_change = (
    customer_status.loc[
        customer_status["status"] == "Active",
        "current_revenue"
    ]
    -
    customer_status.loc[
        customer_status["status"] == "Active",
        "previous_revenue"
    ]
).sum()


new_returning_revenue = (
    customer_status.loc[
        customer_status["status"] == "New / Returning",
        "current_revenue"
    ].sum()
)


# ============================================================
# 3. CATEGORY CONTRIBUTION
# ============================================================

category_revenue = (
    enriched_transactions[
        enriched_transactions["month"].isin(
            [
                previous_month,
                current_month
            ]
        )
    ]
    .groupby(
        ["category", "month"]
    )["line_total"]
    .sum()
    .unstack(fill_value=0)
)


if previous_month not in category_revenue.columns:
    category_revenue[previous_month] = 0

if current_month not in category_revenue.columns:
    category_revenue[current_month] = 0


category_revenue["change"] = (
    category_revenue[current_month]
    - category_revenue[previous_month]
)


# ============================================================
# 4. PRODUCT CONTRIBUTION
# ============================================================

product_revenue = (
    enriched_transactions[
        enriched_transactions["month"].isin(
            [
                previous_month,
                current_month
            ]
        )
    ]
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


if previous_month not in product_revenue.columns:
    product_revenue[previous_month] = 0

if current_month not in product_revenue.columns:
    product_revenue[current_month] = 0


product_revenue["change"] = (
    product_revenue[current_month]
    - product_revenue[previous_month]
)


# ============================================================
# DISPLAY ROOT-CAUSE ANALYSIS
# ============================================================

print("BUSINESS MEMORY - ROOT CAUSE ANALYSIS")
print("=====================================")

print()
print(
    f"PERIOD: "
    f"{previous_month} → {current_month}"
)

print()
print("1. REVENUE MOVEMENT")
print("-------------------")

print(
    f"Previous Revenue : "
    f"₹{previous_revenue:,.2f}"
)

print(
    f"Current Revenue  : "
    f"₹{current_revenue:,.2f}"
)

print(
    f"Revenue Change   : "
    f"₹{revenue_change:+,.2f}"
)

print(
    f"Revenue Change % : "
    f"{revenue_change_percent:+.2f}%"
)


print()
print("2. ORDERS & AOV")
print("---------------")

print(
    f"Previous Orders : "
    f"{previous_orders:,.0f}"
)

print(
    f"Current Orders  : "
    f"{current_orders:,.0f}"
)

print(
    f"Orders Change  : "
    f"{orders_change:+,.0f} "
    f"({orders_change_percent:+.2f}%)"
)

print()

print(
    f"Previous AOV : "
    f"₹{previous_aov:,.2f}"
)

print(
    f"Current AOV  : "
    f"₹{current_aov:,.2f}"
)

print(
    f"AOV Change   : "
    f"₹{aov_change:+,.2f} "
    f"({aov_change_percent:+.2f}%)"
)


# ============================================================
# CUSTOMER DRIVERS
# ============================================================

print()
print("3. CUSTOMER DRIVERS")
print("-------------------")

print(
    f"Churned customers revenue impact : "
    f"₹{churned_revenue_loss:+,.2f}"
)

print(
    f"Active customer movement        : "
    f"₹{active_customer_change:+,.2f}"
)

print(
    f"New/Returning customer revenue  : "
    f"₹{new_returning_revenue:+,.2f}"
)


# ============================================================
# TOP CATEGORY DECLINES
# ============================================================

declining_categories = (
    category_revenue[
        category_revenue["change"] < 0
    ]
    .sort_values(
        "change",
        ascending=True
    )
    .head(5)
)


print()
print("4. TOP CATEGORY DECLINES")
print("------------------------")

if declining_categories.empty:

    print("No category declines found.")

else:

    for category, row in declining_categories.iterrows():

        print(
            f"{category:<20} "
            f"₹{row['change']:+,.2f}"
        )


# ============================================================
# TOP CATEGORY GROWTH
# ============================================================

growing_categories = (
    category_revenue[
        category_revenue["change"] > 0
    ]
    .sort_values(
        "change",
        ascending=False
    )
    .head(5)
)


print()
print("5. TOP CATEGORY GROWTH")
print("----------------------")

if growing_categories.empty:

    print("No category growth found.")

else:

    for category, row in growing_categories.iterrows():

        print(
            f"{category:<20} "
            f"₹{row['change']:+,.2f}"
        )


# ============================================================
# TOP PRODUCT DECLINES
# ============================================================

declining_products = (
    product_revenue[
        product_revenue["change"] < 0
    ]
    .sort_values(
        "change",
        ascending=True
    )
    .head(5)
)


print()
print("6. TOP PRODUCT DECLINES")
print("-----------------------")

if declining_products.empty:

    print("No product declines found.")

else:

    for (
        product_id,
        product_name,
        category
    ), row in declining_products.iterrows():

        print(
            f"{product_name} "
            f"({category}) : "
            f"₹{row['change']:+,.2f}"
        )


# ============================================================
# TOP PRODUCT GROWTH
# ============================================================

growing_products = (
    product_revenue[
        product_revenue["change"] > 0
    ]
    .sort_values(
        "change",
        ascending=False
    )
    .head(5)
)


print()
print("7. TOP PRODUCT GROWTH")
print("---------------------")

if growing_products.empty:

    print("No product growth found.")

else:

    for (
        product_id,
        product_name,
        category
    ), row in growing_products.iterrows():

        print(
            f"{product_name} "
            f"({category}) : "
            f"₹{row['change']:+,.2f}"
        )


# ============================================================
# BUSINESS DIAGNOSTIC SUMMARY
# ============================================================

print()
print("8. BUSINESS DIAGNOSTIC SUMMARY")
print("-------------------------------")

if revenue_change < 0:

    print(
        f"• Revenue decreased by "
        f"₹{abs(revenue_change):,.2f} "
        f"({abs(revenue_change_percent):.2f}%)."
    )

elif revenue_change > 0:

    print(
        f"• Revenue increased by "
        f"₹{revenue_change:,.2f} "
        f"({revenue_change_percent:.2f}%)."
    )

else:

    print("• Revenue remained unchanged.")


if orders_change < 0:

    print(
        f"• Order volume decreased by "
        f"{abs(orders_change_percent):.2f}%."
    )

elif orders_change > 0:

    print(
        f"• Order volume increased by "
        f"{orders_change_percent:.2f}%."
    )


if aov_change < 0:

    print(
        f"• Average order value decreased by "
        f"{abs(aov_change_percent):.2f}%."
    )

elif aov_change > 0:

    print(
        f"• Average order value increased by "
        f"{aov_change_percent:.2f}%."
    )


print()
print("ROOT-CAUSE ANALYSIS COMPLETE")
print("============================")