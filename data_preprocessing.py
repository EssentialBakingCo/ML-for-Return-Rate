import pandas as pd

# File locations
file_location_2024 = "ReturnData.csv"
file_location_2025 = "ReturnData25.csv"

def load_clean_data(file_2024, file_2025):
    """Load datasets, clean them, convert column types, and compute ReturnRate correctly."""

    # Load datasets
    df_24 = pd.read_csv(file_2024)
    df_25 = pd.read_csv(file_2025)

    # Convert date columns to datetime format
    date_cols = ["TranDate", "DeliveryDate", "ReturnDate"]
    for col in date_cols:
        df_24[col] = pd.to_datetime(df_24[col], errors="coerce",utc=True)
        df_25[col] = pd.to_datetime(df_25[col], errors="coerce",utc=True)

    # Convert numeric columns
    int_cols = ["InventoryCD", "AcctCD", "ShelfLife", "Year", "Month", "Day", "WeekNumber"]
    float_cols = ["OrderedQty", "DeliveredQty", "ReturnedQty"]

    for col in int_cols:
        df_24[col] = pd.to_numeric(df_24[col], errors="coerce").fillna(0).astype("int64")
        df_25[col] = pd.to_numeric(df_25[col], errors="coerce").fillna(0).astype("int64")

    for col in float_cols:
        df_24[col] = pd.to_numeric(df_24[col], errors="coerce").fillna(0).astype("float64")
        df_25[col] = pd.to_numeric(df_25[col], errors="coerce").fillna(0).astype("float64")

    # ✅ Fix ReturnRate Calculation (by InventoryCD + AcctName)
    def calculate_return_rate(row):
        if row["DeliveredQty"] > 0:
            return (row["ReturnedQty"] / row["DeliveredQty"]) * 100  # Standard Return Rate
        elif row["DeliveredQty"] == 0 and row["ReturnedQty"] > 0:
            return row["ReturnedQty"]   # Custom Logic
        else:
            return 0.0

    df_24["ReturnRate"] = df_24.apply(calculate_return_rate, axis=1)
    df_25["ReturnRate"] = df_25.apply(calculate_return_rate, axis=1)

    # Debugging: Check unique values in ReturnRate
    print("\n🔍 Unique ReturnRate values (after fixing):", df_24["ReturnRate"].unique())

    # Ensure correct date range
    df_24_filtered = df_24[(df_24["TranDate"] >= "2024-01-01") & (df_24["TranDate"] <= "2024-12-31")]
    df_25_filtered = df_25[(df_25["TranDate"] >= "2025-01-01") & (df_25["TranDate"] <= "2025-02-19")]

    # Save the filtered datasets
    df_24_filtered.to_csv("Filtered2024.csv", index=False)
    df_25_filtered.to_csv("Filtered2025.csv", index=False)

    print("✅ Filtered datasets saved as 'Filtered2024.csv' and 'Filtered2025.csv'")
    return df_24_filtered, df_25_filtered

# Run script
if __name__ == "__main__":
    df_24, df_25 = load_clean_data(file_location_2024, file_location_2025)

    # Debugging: Print data types after conversion
    print("\n🔍 Data Types After Cleaning:")
    print(df_24.dtypes)
