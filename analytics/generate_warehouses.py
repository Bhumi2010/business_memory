import pandas as pd


warehouses = [
    {
        "warehouse_id": "W001",
        "warehouse_name": "Sharma Main Warehouse",
        "city": "Meerut",
        "state": "Uttar Pradesh",
        "capacity_units": 50000
    },
    {
        "warehouse_id": "W002",
        "warehouse_name": "Sharma Delhi Warehouse",
        "city": "Delhi",
        "state": "Delhi",
        "capacity_units": 35000
    }
]


warehouses_df = pd.DataFrame(warehouses)


warehouses_df.to_csv(
    "data/raw/warehouses.csv",
    index=False
)


print("Warehouse dataset created successfully!")
print(f"Number of warehouses: {len(warehouses_df)}")

print("\nSaved to:")
print("data/raw/warehouses.csv")