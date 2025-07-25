import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import r2_score, mean_absolute_error
import joblib


df = pd.read_csv("../data/train_set.csv")

# Feature Engineering
df["checkin"] = pd.to_datetime(df["checkin"])
df["checkout"] = pd.to_datetime(df["checkout"])
df["trip_length"] = (df["checkout"] - df["checkin"]).dt.days
df["checkin_month"] = df["checkin"].dt.month
df["is_cross_border"] = df["booker_country"] != df["hotel_country"]

# Aggregation
agg_features = df.groupby("utrip_id").agg({
    "trip_length": "sum",
    "checkin_month": "first",
    "city_id": pd.Series.nunique,
    "device_class": lambda x: x.iloc[0],  # Assuming the
    "is_cross_border": "max"
}).rename(columns={"city_id": "num_cities"})

# One-Hot Encode
encoder = OneHotEncoder(sparse_output=False)
encoded = encoder.fit_transform(agg_features[["checkin_month", "device_class"]])

# Combine
X = np.hstack([
    agg_features[["trip_length", "is_cross_border"]].astype(float).values,
    encoded
])
y = agg_features["num_cities"].values


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

rf_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
rf_model.fit(X_train, y_train)


# Evaluate
def evaluate_model(name, model, x_test, y_test):
    preds = model.predict(x_test)
    r2 = r2_score(y_test, preds)
    mae = mean_absolute_error(y_test, preds)
    print(f"\n{name} Model:")
    print(f"R² Score: {r2:.3f}")
    print(f"Mean Absolute Error: {mae:.2f} Cities")


evaluate_model("Linear Regression", linear_model, X_test, y_test)
evaluate_model("Random Forest", rf_model, X_test, y_test)


# Prediction Function
def predict_city_count(model, preferred_nights, checkin_month, device_class, is_cross_border):
    input_df = pd.DataFrame([[checkin_month, device_class]], columns=["checkin_month", "device_class"])
    encoded_input = encoder.transform(input_df)
    input_vector = np.hstack([[preferred_nights, int(is_cross_border)], encoded_input[0]])
    prediction = model.predict([input_vector])[0]
    return max(1, round(prediction))


# Example
examples = [
    {"nights": 10, "month": 8, "device": "desktop", "cross_border": True},
    {"nights": 7, "month": 1, "device": "mobile", "cross_border": False},
    {"nights": 14, "month": 6, "device": "tablet", "cross_border": True},
    {"nights": 5, "month": 11, "device": "desktop", "cross_border": False},
    {"nights": 9, "month": 3, "device": "mobile", "cross_border": True},
    {"nights": 8, "month": 4, "device": "mobile", "cross_border": False}
]

print("\n--- Sample Predictions ---")
for i, ex in enumerate(examples, 1):
    lin_pred = predict_city_count(linear_model, ex["nights"], ex["month"], ex["device"], ex["cross_border"])
    rf_pred = predict_city_count(rf_model, ex["nights"], ex["month"], ex["device"], ex["cross_border"])
    print(f"Example {i}: {ex}")
    print(f"  Linear Regression → {lin_pred} cities")
    print(f"  Random Forest     → {rf_pred} cities\n")

joblib.dump(rf_model, "../data/city_count_model.pkl")
joblib.dump(encoder, "../data/city_count_encoder.pkl")
