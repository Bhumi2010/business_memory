import pandas as pd
import numpy as np


# -----------------------------
# Configuration
# -----------------------------

NUM_PRODUCTS = 1000
RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)


# -----------------------------
# Product data
# -----------------------------

categories = {
    "Beverages": [
        "Juice",
        "Soft Drink",
        "Energy Drink",
        "Tea",
        "Coffee"
    ],
    "Snacks": [
        "Chips",
        "Biscuits",
        "Namkeen",
        "Chocolate",
        "Cookies"
    ],
    "Personal Care": [
        "Shampoo",
        "Soap",
        "Toothpaste",
        "Face Wash",
        "Lotion"
    ],
    "Household": [
        "Detergent",
        "Cleaner",
        "Dishwash",
        "Air Freshener",
        "Floor Cleaner"
    ],
    "Packaged Food": [
        "Rice",
        "Pasta",
        "Noodles",
        "Spices",
        "Cereal"
    ],
    "Dairy": [
        "Milk",
        "Curd",
        "Butter",
        "Cheese",
        "Paneer"
    ]
}


brands = [
    "FreshCo",
    "DailyChoice",
    "PrimeFoods",
    "PureLife",
    "SmartBuy",
    "UrbanMart",
    "GoodDay",
    "ValuePlus"
]


# -----------------------------
# Generate products
# -----------------------------

products = []

for i in range(1, NUM_PRODUCTS + 1):

    category = np.random.choice(
        list(categories.keys())
    )

    product_type = np.random.choice(
        categories[category]
    )

    brand = np.random.choice(brands)

    product_name = f"{brand} {product_type} {i}"

    supplier_id = f"S{np.random.randint(1, 21):03d}"

    cost_price = round(
        np.random.uniform(20, 1000),
        2
    )

    # Selling price is above cost
    margin = np.random.uniform(0.05, 0.35)

    selling_price = round(
        cost_price * (1 + margin),
        2
    )

    products.append({
        "product_id": f"P{i:05d}",
        "product_name": product_name,
        "category": category,
        "brand": brand,
        "supplier_id": supplier_id,
        "cost_price": cost_price,
        "selling_price": selling_price
    })


# -----------------------------
# Create DataFrame
# -----------------------------

products_df = pd.DataFrame(products)


# -----------------------------
# Save
# -----------------------------

products_df.to_csv(
    "data/raw/products.csv",
    index=False
)


# -----------------------------
# Summary
# -----------------------------

print("Product dataset created successfully!")

print(f"Number of products: {len(products_df)}")

print("\nProducts by category:")
print(products_df["category"].value_counts())

print("\nAverage selling price:")
print(
    round(products_df["selling_price"].mean(), 2)
)

print("\nFirst 5 products:")
print(products_df.head())

print("\nSaved to:")
print("data/raw/products.csv")