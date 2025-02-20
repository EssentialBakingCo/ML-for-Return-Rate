import pandas as pd

def create_features(df):
    """Generate new features for better model performance."""

    # Ensure TranDate is datetime
    df["TranDate"] = pd.to_datetime(df["TranDate"], errors="coerce")

    # Extract date-related features
    df["Weekday"] = df["TranDate"].dt.day_name()

    # Sort before creating lag features
    df.sort_values(["AcctName", "InventoryCD", "TranDate"], inplace=True)

    # Create a lag feature (previous month's return rate)
    df["Prev_ReturnRate"] = df.groupby(["AcctName", "InventoryCD"])["ReturnRate"].shift(1)

    # Fill missing values (handle missing past data)
    df["Prev_ReturnRate"] = df["Prev_ReturnRate"].fillna(method="bfill").fillna(0)

    # Fix rolling mean calculation (allow at least 1 period)
    df["Rolling_ReturnRate"] = (
        df.groupby(["AcctName", "InventoryCD"])["ReturnRate"]
        .rolling(3, min_periods=1)  # Ensures even if there's only 1 month, it calculates
        .mean()
        .reset_index(level=[0, 1], drop=True)
    )

    # Fill missing values
    df.fillna(0, inplace=True)

    print("✅ Features created successfully!")
    return df

# Run script directly for testing
if __name__ == "__main__":
    df_24 = pd.read_csv("Filtered2024.csv", parse_dates=["TranDate"])
    df_25 = pd.read_csv("Filtered2025.csv", parse_dates=["TranDate"])

    df_24 = create_features(df_24)
    df_25 = create_features(df_25)

    # Save the feature-engineered data
    df_24.to_csv("Featured2024.csv", index=False)
    df_25.to_csv("Featured2025.csv", index=False)

    print("✅ Feature-engineered files saved as 'Featured2024.csv' and 'Featured2025.csv'")
