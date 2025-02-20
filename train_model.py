import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

def train_and_evaluate(df_2024, df_2025):
    #Train Random Forest model on 2024 data and evaluate on 2025 data."

    # Define features and target variable
    features = ["OrderedQty", "DeliveredQty", "Prev_ReturnRate", "Rolling_ReturnRate", "ShelfLife", "WeekNumber"]
    target = "ReturnRate"

    # Ensure features are numeric
    df_2024[features] = df_2024[features].apply(pd.to_numeric, errors="coerce").fillna(0)
    df_2025[features] = df_2025[features].apply(pd.to_numeric, errors="coerce").fillna(0)

    X_train = df_2024[features]
    y_train = df_2024[target]

    X_test = df_2025[features]
    y_test = df_2025[target]

    #Train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions on 2025 data
    y_pred = model.predict(X_test)

    # Evaluate performance
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    #print(f" Model trained and evaluated!")
    print(f" Mean Absolute Error (MAE): {mae:.4f}")
    print(f" R² Score: {r2:.4f}")

    return model, y_test, y_pred

# Run script directly for testing
if __name__ == "__main__":
    df_24 = pd.read_csv("Featured2024.csv", parse_dates=["TranDate"])
    df_25 = pd.read_csv("Featured2025.csv", parse_dates=["TranDate"])

    model, y_test, y_pred = train_and_evaluate(df_24, df_25)

    # Save actual vs predicted results
    results = pd.DataFrame({"Actual": y_test, "Predicted": y_pred})
    results.to_csv("Evaluation_Results_2025.csv", index=False)

    print("Model evaluation results saved to 'Evaluation_Results_2025.csv'")
