import pandas as pd


# -----------------------------
# Load dirty dataset
# -----------------------------

df = pd.read_csv("data/raw/customers_dirty.csv")


print("=" * 50)
print("BUSINESS MEMORY - DATA QUALITY REPORT")
print("=" * 50)


# -----------------------------
# 1. Dataset size
# -----------------------------

print("\n1. DATASET SIZE")
print("-" * 30)

print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")


# -----------------------------
# 2. Missing values
# -----------------------------

print("\n2. MISSING VALUES")
print("-" * 30)

missing = df.isnull().sum()

print(missing[missing > 0])


# -----------------------------
# 3. Duplicate rows
# -----------------------------

print("\n3. DUPLICATE ROWS")
print("-" * 30)

duplicates = df.duplicated().sum()

print(f"Duplicate rows: {duplicates}")


# -----------------------------
# 4. Invalid credit limits
# -----------------------------

print("\n4. INVALID CREDIT LIMITS")
print("-" * 30)

invalid_credit = df[df["credit_limit"] <= 0]

print(f"Invalid records: {len(invalid_credit)}")


# -----------------------------
# 5. Invalid dates
# -----------------------------

print("\n5. INVALID DATES")
print("-" * 30)

parsed_dates = pd.to_datetime(
    df["created_at"],
    errors="coerce"
)

invalid_dates = parsed_dates.isna().sum()

print(f"Invalid dates: {invalid_dates}")


# -----------------------------
# 6. Whitespace problems
# -----------------------------

print("\n6. WHITESPACE ISSUES")
print("-" * 30)

whitespace_issues = (
    df["customer_name"] !=
    df["customer_name"].str.strip()
).sum()

print(f"Names with extra whitespace: {whitespace_issues}")


# -----------------------------
# 7. Uppercase inconsistencies
# -----------------------------

print("\n7. NAME FORMAT ISSUES")
print("-" * 30)

uppercase_issues = (
    df["customer_name"] !=
    df["customer_name"].str.title()
).sum()

print(f"Names not in standard format: {uppercase_issues}")


# -----------------------------
# Final summary
# -----------------------------

print("\n" + "=" * 50)
print("DATA QUALITY CHECK COMPLETE")
print("=" * 50)