import pandas as pd
import numpy as np


# -----------------------------
# Configuration
# -----------------------------

NUM_SUPPLIERS = 20
RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)


# -----------------------------
# Sample data
# -----------------------------

supplier_prefixes = [
    "Shree",
    "National",
    "Global",
    "United",
    "Modern",
    "Prime",
    "Reliable",
    "Royal",
    "New",
    "Metro"
]

supplier_words = [
    "Foods",
    "Consumer Products",
    "Distributors",
    "Industries",
    "Supplies",
    "Enterprises"
]

locations = [
    ("Meerut", "Uttar Pradesh"),
    ("Delhi", "Delhi"),
    ("Ghaziabad", "Uttar Pradesh"),
    ("Noida", "Uttar Pradesh"),
    ("Agra", "Uttar Pradesh"),
    ("Jaipur", "Rajasthan"),
    ("Gurgaon", "Haryana"),
    ("Kanpur", "Uttar Pradesh"),
    ("Lucknow", "Uttar Pradesh"),
    ("Haridwar", "Uttarakhand")
]

supplier_types = [
    "Manufacturer",
    "Wholesaler",
    "Importer"
]


# -----------------------------
# Generate suppliers
# -----------------------------

suppliers = []

for i in range(1, NUM_SUPPLIERS + 1):

    prefix = np.random.choice(supplier_prefixes)
    word = np.random.choice(supplier_words)

    supplier_name = f"{prefix} {word}"

    city, state = locations[
        np.random.randint(0, len(locations))
    ]

    supplier_type = np.random.choice(
        supplier_types,
        p=[0.50, 0.35, 0.15]
    )

    suppliers.append({
        "supplier_id": f"S{i:03d}",
        "supplier_name": supplier_name,
        "city": city,
        "state": state,
        "supplier_type": supplier_type
    })


# -----------------------------
# Create DataFrame
# -----------------------------

suppliers_df = pd.DataFrame(suppliers)


# -----------------------------
# Save
# -----------------------------

suppliers_df.to_csv(
    "data/raw/suppliers.csv",
    index=False
)


# -----------------------------
# Summary
# -----------------------------

print("Supplier dataset created successfully!")

print(f"Number of suppliers: {len(suppliers_df)}")

print("\nSupplier types:")
print(suppliers_df["supplier_type"].value_counts())

print("\nFirst 5 suppliers:")
print(suppliers_df.head())

print("\nSaved to:")
print("data/raw/suppliers.csv")