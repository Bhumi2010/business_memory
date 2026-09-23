import pandas as pd
import numpy as np


# -----------------------------------
# 1. Load dirty data
# -----------------------------------

df = pd.read_csv(
    "data/raw/customers_dirty.csv"
)

print(f"Original rows: {len(df)}")


# -----------------------------------
# 2. Remove exact duplicates
# -----------------------------------

df = df.drop_duplicates()

print(f"After removing duplicates: {len(df)}")


# -----------------------------------
# 3. Standardize customer names
# -----------------------------------

df["customer_name"] = (
    df["customer_name"]
    .str.strip()
    .str.title()
)


# -----------------------------------
# 4. Standardize city
# -----------------------------------

df["city"] = (
    df["city"]
    .str.strip()
    .str.title()
)

df["city"] = df["city"].fillna("Unknown")


# -----------------------------------
# 5. Standardize customer type
# -----------------------------------

df["customer_type"] = (
    df["customer_type"]
    .str.strip()
    .str.title()
)

df["customer_type"] = (
    df["customer_type"]
    .fillna("Unknown")
)


# -----------------------------------
# 6. Clean credit limits
# -----------------------------------

df.loc[
    df["credit_limit"] <= 0,
    "credit_limit"
] = np.nan


# -----------------------------------
# 7. Convert dates
# -----------------------------------

df["created_at"] = pd.to_datetime(
    df["created_at"],
    errors="coerce"
)


# -----------------------------------
# 8. Validate cleaned data
# -----------------------------------

print("\nCLEANING RESULTS")
print("-" * 40)

print(f"Rows: {len(df)}")

print(
    f"Duplicate rows: "
    f"{df.duplicated().sum()}"
)

print(
    f"Missing cities: "
    f"{df['city'].isna().sum()}"
)

print(
    f"Missing customer types: "
    f"{df['customer_type'].isna().sum()}"
)

print(
    f"Invalid credit limits: "
    f"{(df['credit_limit'] <= 0).sum()}"
)

print(
    f"Invalid dates: "
    f"{df['created_at'].isna().sum()}"
)


# -----------------------------------
# 9. Save cleaned dataset
# -----------------------------------

df.to_csv(
    "data/processed/customers_clean.csv",
    index=False
)

print("\nClean dataset saved to:")
print("data/processed/customers_clean.csv")