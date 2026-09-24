import sys
from pathlib import Path

import pandas as pd


# -------------------------------------------------
# Make project root available for analytics imports
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))


from analytics.data_loader import (
    load_sales,
    load_transaction_data,
    load_enriched_transactions
)


# -------------------------------------------------
# Overview
# -------------------------------------------------

def get_overview():
    """
    Return high-level business metrics.
    """

    sales = load_sales()
    transactions = load_transaction_data()

    total_revenue = transactions["line_total"].sum()

    total_orders = sales["sale_id"].nunique()

    total_units_sold = transactions["quantity"].sum()

    total_customers = transactions["customer_id"].nunique()

    average_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )

    return {
        "total_revenue": round(float(total_revenue), 2),
        "total_orders": int(total_orders),
        "total_units_sold": int(total_units_sold),
        "total_customers": int(total_customers),
        "average_order_value": round(float(average_order_value), 2)
    }

    # -------------------------------------------------
# Revenue Analysis
# -------------------------------------------------

def get_revenue_analysis():
    """
    Return July vs August revenue,
    orders, and AOV performance.
    """

    sales = load_sales()
    transactions = load_transaction_data()

    previous_month = pd.Period("2026-07")
    current_month = pd.Period("2026-08")

    # -----------------------------
    # Revenue
    # -----------------------------

    monthly_revenue = (
        transactions
        .groupby("month")["line_total"]
        .sum()
    )

    july_revenue = monthly_revenue.get(previous_month, 0)
    august_revenue = monthly_revenue.get(current_month, 0)

    revenue_change = august_revenue - july_revenue

    revenue_change_percent = (
        revenue_change / july_revenue * 100
        if july_revenue != 0
        else 0
    )

    # -----------------------------
    # Orders
    # -----------------------------

    sales["month"] = sales["sale_date"].dt.to_period("M")

    monthly_orders = (
        sales
        .groupby("month")["sale_id"]
        .nunique()
    )

    july_orders = monthly_orders.get(previous_month, 0)
    august_orders = monthly_orders.get(current_month, 0)

    orders_change = august_orders - july_orders

    orders_change_percent = (
        orders_change / july_orders * 100
        if july_orders != 0
        else 0
    )

    # -----------------------------
    # Average Order Value
    # -----------------------------

    july_aov = (
        july_revenue / july_orders
        if july_orders != 0
        else 0
    )

    august_aov = (
        august_revenue / august_orders
        if august_orders != 0
        else 0
    )

    aov_change = august_aov - july_aov

    aov_change_percent = (
        aov_change / july_aov * 100
        if july_aov != 0
        else 0
    )

    # -----------------------------
    # Return API response
    # -----------------------------

    return {
        "period": "2026-07 to 2026-08",

        "revenue": {
            "july": round(float(july_revenue), 2),
            "august": round(float(august_revenue), 2),
            "change": round(float(revenue_change), 2),
            "change_percent": round(float(revenue_change_percent), 2)
        },

        "orders": {
            "july": int(july_orders),
            "august": int(august_orders),
            "change": int(orders_change),
            "change_percent": round(float(orders_change_percent), 2)
        },

        "average_order_value": {
            "july": round(float(july_aov), 2),
            "august": round(float(august_aov), 2),
            "change": round(float(aov_change), 2),
            "change_percent": round(float(aov_change_percent), 2)
        }
    }

    # -------------------------------------------------
# Customer Analysis
# -------------------------------------------------

def get_customer_analysis():
    """
    Return customer movement between July and August.
    """

    transactions = load_transaction_data()

    previous_month = pd.Period("2026-07")
    current_month = pd.Period("2026-08")

    comparison = transactions[
        transactions["month"].isin(
            [previous_month, current_month]
        )
    ].copy()

    customer_revenue = (
        comparison
        .groupby(["customer_id", "month"])["line_total"]
        .sum()
        .unstack(fill_value=0)
    )

    if previous_month not in customer_revenue.columns:
        customer_revenue[previous_month] = 0

    if current_month not in customer_revenue.columns:
        customer_revenue[current_month] = 0

    july_revenue = customer_revenue[previous_month]
    august_revenue = customer_revenue[current_month]

    customer_analysis = pd.DataFrame({
        "july_revenue": july_revenue,
        "august_revenue": august_revenue
    })

    customer_analysis["change_amount"] = (
        customer_analysis["august_revenue"]
        - customer_analysis["july_revenue"]
    )

    def determine_status(row):
        if row["july_revenue"] > 0 and row["august_revenue"] > 0:
            return "Active"

        if row["july_revenue"] > 0 and row["august_revenue"] == 0:
            return "Inactive"

        if row["july_revenue"] == 0 and row["august_revenue"] > 0:
            return "New or Returning"

        return "No Activity"

    customer_analysis["status"] = (
        customer_analysis
        .apply(determine_status, axis=1)
    )

    active_count = int(
        (customer_analysis["status"] == "Active").sum()
    )

    inactive_count = int(
        (customer_analysis["status"] == "Inactive").sum()
    )

    new_returning_count = int(
        (customer_analysis["status"] == "New or Returning").sum()
    )

    inactive_revenue_impact = customer_analysis.loc[
        customer_analysis["status"] == "Inactive",
        "change_amount"
    ].sum()

    active_customer_change = customer_analysis.loc[
        customer_analysis["status"] == "Active",
        "change_amount"
    ].sum()

    new_returning_revenue = customer_analysis.loc[
        customer_analysis["status"] == "New or Returning",
        "august_revenue"
    ].sum()

    return {
        "period": "2026-07 to 2026-08",

        "customer_counts": {
            "active": active_count,
            "inactive": inactive_count,
            "new_or_returning": new_returning_count
        },

        "revenue_impact": {
            "inactive_customers": round(
                float(inactive_revenue_impact), 2
            ),
            "active_customers": round(
                float(active_customer_change), 2
            ),
            "new_or_returning": round(
                float(new_returning_revenue), 2
            )
        }
    }


# -------------------------------------------------
# Retention Analysis
# -------------------------------------------------

def get_retention_analysis():
    """
    Return customer retention and churn metrics.
    """

    transactions = load_transaction_data()

    previous_month = pd.Period("2026-07")
    current_month = pd.Period("2026-08")

    july_customers = set(
        transactions.loc[
            transactions["month"] == previous_month,
            "customer_id"
        ].unique()
    )

    august_customers = set(
        transactions.loc[
            transactions["month"] == current_month,
            "customer_id"
        ].unique()
    )

    retained_customers = (
        july_customers & august_customers
    )

    churned_customers = (
        july_customers - august_customers
    )

    new_returning_customers = (
        august_customers - july_customers
    )

    july_customer_count = len(july_customers)

    retained_count = len(retained_customers)
    churned_count = len(churned_customers)
    new_returning_count = len(new_returning_customers)

    retention_rate = (
        retained_count / july_customer_count * 100
        if july_customer_count
        else 0
    )

    churn_rate = (
        churned_count / july_customer_count * 100
        if july_customer_count
        else 0
    )

    customer_revenue = (
        transactions[
            transactions["month"].isin(
                [previous_month, current_month]
            )
        ]
        .groupby(["customer_id", "month"])["line_total"]
        .sum()
        .unstack(fill_value=0)
    )

    if previous_month not in customer_revenue.columns:
        customer_revenue[previous_month] = 0

    if current_month not in customer_revenue.columns:
        customer_revenue[current_month] = 0

    churned_revenue_loss = (
        customer_revenue
        .loc[
            list(churned_customers),
            current_month
        ]
        .sub(
            customer_revenue.loc[
                list(churned_customers),
                previous_month
            ]
        )
        .sum()
    )

    retained_august_revenue = (
        customer_revenue
        .loc[
            list(retained_customers),
            current_month
        ]
        .sum()
    )

    new_returning_august_revenue = (
        customer_revenue
        .loc[
            list(new_returning_customers),
            current_month
        ]
        .sum()
    )

    return {
        "period": "2026-07 to 2026-08",

        "customers": {
            "july": july_customer_count,
            "august": len(august_customers),
            "retained": retained_count,
            "churned": churned_count,
            "new_or_returning": new_returning_count
        },

        "rates": {
            "retention_rate": round(
                float(retention_rate), 2
            ),
            "churn_rate": round(
                float(churn_rate), 2
            )
        },

        "revenue_impact": {
            "churned_revenue_loss": round(
                float(churned_revenue_loss), 2
            ),
            "retained_august_revenue": round(
                float(retained_august_revenue), 2
            ),
            "new_or_returning_august_revenue": round(
                float(new_returning_august_revenue), 2
            )
        }
    }

    # -------------------------------------------------
# Customer Segmentation
# -------------------------------------------------

def get_customer_segments():
    """
    Return customer segmentation between July and August.
    """

    transactions = load_transaction_data()

    previous_month = pd.Period("2026-07")
    current_month = pd.Period("2026-08")

    comparison = transactions[
        transactions["month"].isin(
            [previous_month, current_month]
        )
    ].copy()


    # ---------------------------------------------
    # Revenue by customer and month
    # ---------------------------------------------

    customer_revenue = (
        comparison
        .groupby(["customer_id", "month"])["line_total"]
        .sum()
        .unstack(fill_value=0)
    )

    if previous_month not in customer_revenue.columns:
        customer_revenue[previous_month] = 0

    if current_month not in customer_revenue.columns:
        customer_revenue[current_month] = 0

    customer_analysis = pd.DataFrame({
        "july_revenue": customer_revenue[previous_month],
        "august_revenue": customer_revenue[current_month]
    })

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
        / customer_analysis["july_revenue"].replace(0, pd.NA)
        * 100
    )

    # ---------------------------------------------
    # Orders
    # ---------------------------------------------

    customer_orders = (
        comparison
        .groupby(["customer_id", "month"])["sale_id"]
        .nunique()
        .unstack(fill_value=0)
    )

    if previous_month not in customer_orders.columns:
        customer_orders[previous_month] = 0

    if current_month not in customer_orders.columns:
        customer_orders[current_month] = 0

    customer_analysis["total_orders"] = (
        customer_orders[previous_month]
        + customer_orders[current_month]
    )

    # ---------------------------------------------
    # Customer status
    # ---------------------------------------------

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

    # ---------------------------------------------
    # Data-driven thresholds
    # ---------------------------------------------

    active_customers = customer_analysis[
        customer_analysis["status"] == "Active"
    ]

    high_value_threshold = (
        active_customers["total_revenue"]
        .quantile(0.75)
    )

    high_frequency_threshold = (
        active_customers["total_orders"]
        .quantile(0.75)
    )

    # ---------------------------------------------
    # Segment assignment
    # ---------------------------------------------

    def assign_segment(row):

        status = row["status"]

        high_value = (
            row["total_revenue"]
            >= high_value_threshold
        )

        high_frequency = (
            row["total_orders"]
            >= high_frequency_threshold
        )

        if status == "Churned":

            if high_value:
                return "High Value Churn"

            return "Churned"

        if status == "New / Returning":

            if high_value:
                return "High Value New/Returning"

            return "New / Returning"

        if status == "Active":

            revenue_decline = (
                row["revenue_change_percent"]
                if pd.notna(
                    row["revenue_change_percent"]
                )
                else 0
            )

            # Check At Risk FIRST
            if revenue_decline <= -50:
                return "At Risk"

            if (
                high_value
                and high_frequency
            ):
                return "High Value Loyal"

            if (
                high_value
                and not high_frequency
            ):
                return "High Value"

            if (
                not high_value
                and high_frequency
            ):
                return "Regular Active"

            return "Loyal"

        return "No Activity"

    customer_analysis["segment"] = (
        customer_analysis.apply(
            assign_segment,
            axis=1
        )
    )

    # ---------------------------------------------
    # Segment summary
    # ---------------------------------------------

    segment_summary = (
        customer_analysis
        .groupby("segment")
        .agg(
            customer_count=("segment", "size"),
            total_revenue=("total_revenue", "sum"),
            average_revenue=("total_revenue", "mean"),
            total_orders=("total_orders", "sum")
        )
        .reset_index()
        .sort_values(
            "total_revenue",
            ascending=False
        )
    )

    segments = []

    for _, row in segment_summary.iterrows():

        segments.append({
            "segment": row["segment"],
            "customer_count": int(
                row["customer_count"]
            ),
            "total_revenue": round(
                float(row["total_revenue"]),
                2
            ),
            "average_revenue": round(
                float(row["average_revenue"]),
                2
            ),
            "total_orders": int(
                row["total_orders"]
            )
        })

    return {
        "period": "2026-07 to 2026-08",

        "thresholds": {
            "high_value_revenue": round(
                float(high_value_threshold),
                2
            ),
            "high_frequency_orders": int(
                high_frequency_threshold
            )
        },

        "segments": segments
    }
# -------------------------------------------------
# Category Analysis
# -------------------------------------------------

def get_category_analysis():
    """
    Return July vs August revenue performance by category.
    """

    transactions = load_enriched_transactions()

    previous_month = pd.Period("2026-07")
    current_month = pd.Period("2026-08")

    comparison = transactions[
        transactions["month"].isin(
            [previous_month, current_month]
        )
    ].copy()

    category_revenue = (
        comparison
        .groupby(["category", "month"])["line_total"]
        .sum()
        .unstack(fill_value=0)
    )

    if previous_month not in category_revenue.columns:
        category_revenue[previous_month] = 0

    if current_month not in category_revenue.columns:
        category_revenue[current_month] = 0

    category_analysis = pd.DataFrame({
        "july_revenue": category_revenue[previous_month],
        "august_revenue": category_revenue[current_month]
    })

    category_analysis["change"] = (
        category_analysis["august_revenue"]
        - category_analysis["july_revenue"]
    )

    category_analysis["change_percent"] = (
        category_analysis["change"]
        / category_analysis["july_revenue"].replace(0, pd.NA)
        * 100
    )

    category_analysis = (
        category_analysis
        .reset_index()
        .sort_values("change")
    )

    categories = []

    for _, row in category_analysis.iterrows():

        categories.append({
            "category": row["category"],
            "july_revenue": round(
                float(row["july_revenue"]), 2
            ),
            "august_revenue": round(
                float(row["august_revenue"]), 2
            ),
            "change": round(
                float(row["change"]), 2
            ),
            "change_percent": (
                round(float(row["change_percent"]), 2)
                if pd.notna(row["change_percent"])
                else None
            )
        })

    return {
        "period": "2026-07 to 2026-08",
        "categories": categories
    }
def get_product_analysis():
    """
    Return July vs August revenue performance by product.
    """

    transactions = load_enriched_transactions()

    previous_month = pd.Period("2026-07")
    current_month = pd.Period("2026-08")

    comparison = transactions[
        transactions["month"].isin(
            [previous_month, current_month]
        )
    ].copy()

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

    if previous_month not in product_revenue.columns:
        product_revenue[previous_month] = 0

    if current_month not in product_revenue.columns:
        product_revenue[current_month] = 0

    product_analysis = pd.DataFrame({
        "july_revenue": product_revenue[previous_month],
        "august_revenue": product_revenue[current_month]
    })

    product_analysis["change"] = (
        product_analysis["august_revenue"]
        - product_analysis["july_revenue"]
    )

    product_analysis["change_percent"] = (
        product_analysis["change"]
        / product_analysis["july_revenue"].replace(0, pd.NA)
        * 100
    )

    product_analysis = (
        product_analysis
        .reset_index()
        .sort_values("change")
    )

    products = []

    for _, row in product_analysis.iterrows():

        products.append({
            "product_id": row["product_id"],
            "product_name": row["product_name"],
            "category": row["category"],
            "july_revenue": round(
                float(row["july_revenue"]), 2
            ),
            "august_revenue": round(
                float(row["august_revenue"]), 2
            ),
            "change": round(
                float(row["change"]), 2
            ),
            "change_percent": (
                round(float(row["change_percent"]), 2)
                if pd.notna(row["change_percent"])
                else None
            )
        })

    return {
        "period": "2026-07 to 2026-08",
        "products": products
    }


def get_root_cause_analysis():
    """
    Explain the main drivers behind the July to August revenue change.
    """

    transactions = load_enriched_transactions()

    previous_month = pd.Period("2026-07")
    current_month = pd.Period("2026-08")

    comparison = transactions[
        transactions["month"].isin(
            [previous_month, current_month]
        )
    ].copy()

    # ---------------------------------------------------------
    # 1. Revenue Analysis
    # ---------------------------------------------------------

    monthly_revenue = (
        comparison
        .groupby("month")["line_total"]
        .sum()
    )

    july_revenue = float(monthly_revenue.get(previous_month, 0))
    august_revenue = float(monthly_revenue.get(current_month, 0))

    revenue_change = august_revenue - july_revenue

    revenue_change_percent = (
        (revenue_change / july_revenue) * 100
        if july_revenue != 0
        else None
    )

    # ---------------------------------------------------------
    # 2. Order Analysis
    # ---------------------------------------------------------

    monthly_orders = (
        comparison
        .groupby("month")["sale_id"]
        .nunique()
    )

    july_orders = int(monthly_orders.get(previous_month, 0))
    august_orders = int(monthly_orders.get(current_month, 0))

    order_change = august_orders - july_orders

    order_change_percent = (
        (order_change / july_orders) * 100
        if july_orders != 0
        else None
    )

    # ---------------------------------------------------------
    # 3. Average Order Value
    # ---------------------------------------------------------

    july_aov = (
        july_revenue / july_orders
        if july_orders != 0
        else 0
    )

    august_aov = (
        august_revenue / august_orders
        if august_orders != 0
        else 0
    )

    aov_change = august_aov - july_aov

    aov_change_percent = (
        (aov_change / july_aov) * 100
        if july_aov != 0
        else None
    )

    # ---------------------------------------------------------
    # 4. Customer Impact
    # ---------------------------------------------------------

    july_customers = set(
        comparison.loc[
            comparison["month"] == previous_month,
            "customer_id"
        ].dropna()
    )

    august_customers = set(
        comparison.loc[
            comparison["month"] == current_month,
            "customer_id"
        ].dropna()
    )

    retained_customers = july_customers & august_customers
    churned_customers = july_customers - august_customers
    new_or_returning_customers = august_customers - july_customers

    churned_revenue = (
    comparison[
        (comparison["month"] == previous_month)
        & (comparison["customer_id"].isin(churned_customers))
    ]["line_total"]
    .sum()
)

    # Revenue generated by customers who were not present in July
    new_returning_revenue = (
        comparison[
            (comparison["month"] == current_month)
            & (
                comparison["customer_id"]
                .isin(new_or_returning_customers)
            )
        ]["line_total"]
        .sum()
    )

    # ---------------------------------------------------------
    # 5. Category Impact
    # ---------------------------------------------------------

    category_revenue = (
        comparison
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

    category_changes = (
        category_revenue[
            ["change"]
        ]
        .reset_index()
        .sort_values("change")
    )

    category_declines = []

    for _, row in category_changes.head(5).iterrows():
        category_declines.append({
            "category": row["category"],
            "change": round(float(row["change"]), 2)
        })

    category_growth = []

    for _, row in category_changes.tail(5).sort_values(
        "change",
        ascending=False
    ).iterrows():

        if row["change"] > 0:
            category_growth.append({
                "category": row["category"],
                "change": round(float(row["change"]), 2)
            })

    # ---------------------------------------------------------
    # 6. Product Impact
    # ---------------------------------------------------------

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

    if previous_month not in product_revenue.columns:
        product_revenue[previous_month] = 0

    if current_month not in product_revenue.columns:
        product_revenue[current_month] = 0

    product_revenue["change"] = (
        product_revenue[current_month]
        - product_revenue[previous_month]
    )

    product_changes = (
        product_revenue[
            ["change"]
        ]
        .reset_index()
        .sort_values("change")
    )

    product_declines = []

    for _, row in product_changes.head(5).iterrows():
        product_declines.append({
            "product_id": row["product_id"],
            "product_name": row["product_name"],
            "category": row["category"],
            "change": round(float(row["change"]), 2)
        })

    product_growth = []

    for _, row in product_changes.tail(5).sort_values(
        "change",
        ascending=False
    ).iterrows():

        if row["change"] > 0:
            product_growth.append({
                "product_id": row["product_id"],
                "product_name": row["product_name"],
                "category": row["category"],
                "change": round(float(row["change"]), 2)
            })

    # ---------------------------------------------------------
    # 7. Return Business Explanation
    # ---------------------------------------------------------

    return {
        "period": "2026-07 to 2026-08",

        "revenue": {
            "july": round(july_revenue, 2),
            "august": round(august_revenue, 2),
            "change": round(revenue_change, 2),
            "change_percent": round(
                revenue_change_percent, 2
            ) if revenue_change_percent is not None else None
        },

        "orders": {
            "july": july_orders,
            "august": august_orders,
            "change": order_change,
            "change_percent": round(
                order_change_percent, 2
            ) if order_change_percent is not None else None
        },

        "average_order_value": {
            "july": round(july_aov, 2),
            "august": round(august_aov, 2),
            "change": round(aov_change, 2),
            "change_percent": round(
                aov_change_percent, 2
            ) if aov_change_percent is not None else None
        },

        "customer_impact": {
            "retained_customers": len(retained_customers),
            "churned_customers": len(churned_customers),
            "new_or_returning_customers": len(
                new_or_returning_customers
            ),
            "churned_revenue_impact": round(
                -abs(float(churned_revenue)),
                2
            ),
            "new_or_returning_revenue": round(
                float(new_returning_revenue),
                2
            )
        },

        "category_impact": {
            "declines": category_declines,
            "growth": category_growth
        },

        "product_impact": {
            "declines": product_declines,
            "growth": product_growth
        }
    }