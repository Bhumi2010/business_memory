import pandas as pd

from data_loader import load_sales, load_transaction_data


# -----------------------------
# Load prepared data
# -----------------------------

sales = load_sales()
transactions = load_transaction_data()


# -----------------------------
# Calculate monthly revenue
# -----------------------------

monthly_revenue = (
    transactions
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