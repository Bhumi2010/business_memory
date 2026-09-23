import pandas as pd
import numpy as np


# -----------------------------
# Configuration
# -----------------------------

NUM_CUSTOMERS = 500
RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)


# -----------------------------
# Sample business data
# -----------------------------

first_names = [
    "Amit", "Rahul", "Rohit", "Ankit", "Vikas",
    "Pankaj", "Manish", "Suresh", "Rajesh", "Deepak",
    "Neeraj", "Arjun", "Karan", "Mohit", "Nitin"
]

business_words = [
    "Traders",
    "Enterprises",
    "Store",
    "Distributors",
    "Mart",
    "Agency",
    "Wholesalers"
]

locations = [
    ("Meerut", "Uttar Pradesh"),
    ("Delhi", "Delhi"),
    ("Ghaziabad", "Uttar Pradesh"),
    ("Noida", "Uttar Pradesh"),
    ("Muzaffarnagar", "Uttar Pradesh"),
    ("Hapur", "Uttar Pradesh"),
    ("Bulandshahr", "Uttar Pradesh"),
    ("Agra", "Uttar Pradesh"),
    ("Lucknow", "Uttar Pradesh"),
    ("Jaipur", "Rajasthan")
]

customer_types = [
    "Retailer",
    "Wholesaler",
    "Distributor"
]


# -----------------------------
# Generate customers
# -----------------------------

customers = []

for i in range(1, NUM_CUSTOMERS + 1):

    first_name = np.random.choice(first_names)
    business_type = np.random.choice(business_words)

    customer_name = f"{first_name} {business_type}"

    city, state = locations[
        np.random.randint(0, len(locations))
    ]

    customer_type = np.random.choice(
        customer_types,
        p=[0.60, 0.30, 0.10]
    )

    credit_limit = np.random.choice([
        25000,
        50000,
        75000,
        100000,
        150000,
        250000,
        500000
    ])

    created_at = pd.Timestamp(
        np.random.choice(
            pd.date_range(
                start="2022-01-01",
                end="2026-08-31"
            )
        )
    )

    customers.append({
        "customer_id": f"C{i:05d}",
        "customer_name": customer_name,
        "city": city,
        "state": state,
        "customer_type": customer_type,
        "credit_limit": credit_limit,
        "created_at": created_at
    })


# -----------------------------
# Convert to DataFrame
# -----------------------------

customers_df = pd.DataFrame(customers)


# -----------------------------
# Save dataset
# -----------------------------

customers_df.to_csv(
    "data/raw/customers.csv",
    index=False
)


# -----------------------------
# Basic information
# -----------------------------

print("Customer dataset created successfully!")
print(f"Number of customers: {len(customers_df)}")
print(f"Number of columns: {len(customers_df.columns)}")

print("\nFirst 5 customers:")
print(customers_df.head())

print("\nCustomer types:")
print(customers_df["customer_type"].value_counts())

print("\nDataset saved to:")
print("data/raw/customers.csv")