import joblib
import pandas as pd

# Load the trained model
model = joblib.load("models/decision_tree_model.pkl")

print("Trained model loaded successfully!")

# New network traffic
new_data = pd.DataFrame({
    "packets": [500],
    "bytes": [9000],
    "failed_logins": [5]
})

# Make prediction
prediction = model.predict(new_data)[0]

# Convert numeric label to readable result
if prediction == 1:
    result = "SUSPICIOUS"
else:
    result = "NORMAL"

print("\nPrediction:", result)