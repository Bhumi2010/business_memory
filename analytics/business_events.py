import pandas as pd
from pathlib import Path


# -----------------------------
# Paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "raw"

SALES_FILE = RAW_DATA / "sales.csv"
SALE_ITEMS_FILE = RAW_DATA / "sale_items.csv"


# -----------------------------
# Load data
# -----------------------------

sales = pd.read_csv(SALES_FILE)
sale_items = pd.read_csv(SALE_ITEMS_FILE)


# -----------------------------
# Prepare dates
# -----------------------------

sales["sale_date"] = pd.to_datetime(sales["sale_date"])


# -----------------------------
# Attach sale dates to items
# -----------------------------

sale_items_with_dates = sale_items.merge(
    sales[["sale_id", "sale_date"]],
    on="sale_id",
    how="left"
)


# -----------------------------
# Create month column
# -----------------------------

sale_items_with_dates["month"] = (
    sale_items_with_dates["sale_date"]
    .dt.to_period("M")
)


# -----------------------------
# Calculate monthly revenue
# -----------------------------

monthly_revenue = (
    sale_items_with_dates
    .groupby("month")["line_total"]
    .sum()
    .sort_index()
)


# -----------------------------
# Find latest transaction date
# -----------------------------

latest_date = sales["sale_date"].max()

latest_month = latest_date.to_period("M")


# -----------------------------
# Calculate MoM change
# -----------------------------

monthly_change = monthly_revenue.pct_change() * 100


# -----------------------------
# Generate business events
# -----------------------------

events = []


for month, change in monthly_change.items():

    if pd.isna(change):
        continue

    # ---------------------------------
    # Ignore incomplete latest month
    # ---------------------------------

    if month == latest_month:

        print()
        print(f"Skipping {month}: incomplete month")
        print(f"Data available through: {latest_date.date()}")

        continue


    # ---------------------------------
    # Ignore small changes
    # ---------------------------------

    if abs(change) < 5:
        continue


    # ---------------------------------
    # Determine event type
    # ---------------------------------

    if change >= 10:
        event_type = "Revenue Increase"
        severity = "High"

    elif change > 0:
        event_type = "Revenue Increase"
        severity = "Medium"

    elif change <= -10:
        event_type = "Revenue Decrease"
        severity = "High"

    else:
        event_type = "Revenue Decrease"
        severity = "Medium"


    # ---------------------------------
    # Previous month
    # ---------------------------------

    previous_month = month - 1


    # ---------------------------------
    # Revenue values
    # ---------------------------------

    current_revenue = monthly_revenue.loc[month]
    previous_revenue = monthly_revenue.loc[previous_month]


    # ---------------------------------
    # Store event
    # ---------------------------------

    events.append({
        "period": str(month),
        "event_type": event_type,
        "severity": severity,
        "change_percent": round(change, 2),
        "previous_revenue": round(previous_revenue, 2),
        "current_revenue": round(current_revenue, 2)
    })


# -----------------------------
# Convert to DataFrame
# -----------------------------

events_df = pd.DataFrame(events)


# -----------------------------
# Display events
# -----------------------------

print()
print("BUSINESS MEMORY EVENTS")
print("======================")

if events_df.empty:

    print("No significant business events detected.")

else:

    for _, event in events_df.iterrows():

        print()
        print(f"Period     : {event['period']}")
        print(f"Event      : {event['event_type']}")
        print(f"Severity   : {event['severity']}")
        print(f"Change     : {event['change_percent']:+.2f}%")
        print(
            f"Revenue    : ₹{event['previous_revenue']:,.2f}"
            f" → ₹{event['current_revenue']:,.2f}"
        )
        print("----------------------")