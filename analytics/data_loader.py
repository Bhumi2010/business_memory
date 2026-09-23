import pandas as pd
from pathlib import Path


# -----------------------------
# Project paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "raw"


# -----------------------------
# Load sales data
# -----------------------------

def load_sales():
    """
    Load sales transaction data.
    """

    sales_file = RAW_DATA / "sales.csv"

    sales = pd.read_csv(sales_file)

    sales["sale_date"] = pd.to_datetime(
        sales["sale_date"],
        errors="coerce"
    )

    return sales


# -----------------------------
# Load sale items
# -----------------------------

def load_sale_items():
    """
    Load individual sale item data.
    """

    sale_items_file = RAW_DATA / "sale_items.csv"

    sale_items = pd.read_csv(sale_items_file)

    return sale_items


# -----------------------------
# Prepare transaction data
# -----------------------------

def load_transaction_data():
    """
    Load sales and sale items
    and combine them into a
    transaction-level dataset.
    """

    sales = load_sales()
    sale_items = load_sale_items()

    transactions = sale_items.merge(
        sales[["sale_id", "customer_id", "warehouse_id", "sale_date", "payment_status"]],
        on="sale_id",
        how="left"
    )

    transactions["month"] = (
        transactions["sale_date"]
        .dt.to_period("M")
    )

    return transactions
    


    # -----------------------------
# Load products
# -----------------------------

def load_products():
    """
    Load product master data.
    """

    products_file = RAW_DATA / "products.csv"

    products = pd.read_csv(products_file)

    return products


# -----------------------------
# Load enriched transaction data
# -----------------------------

def load_enriched_transactions():
    """
    Load transaction data with
    product information attached.
    """

    transactions = load_transaction_data()
    products = load_products()

    transactions = transactions.merge(
        products[
            [
                "product_id",
                "product_name",
                "category",
                "brand",
                "supplier_id",
                "cost_price",
                "selling_price"
            ]
        ],
        on="product_id",
        how="left"
    )

    return transactions