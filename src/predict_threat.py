import joblib
import pandas as pd
import os

# Load the trained model
model = joblib.load("models/decision_tree_model.pkl")

print("AI Cybersecurity Threat Detection System")
print("-----------------------------------------")

# Get user input
packets = int(input("Enter number of packets: "))
bytes_sent = int(input("Enter number of bytes: "))
failed_logins = int(input("Enter number of failed logins: "))

# Create input data
new_data = pd.DataFrame({
    "packets": [packets],
    "bytes": [bytes_sent],
    "failed_logins": [failed_logins]
})

# Predict
prediction = model.predict(new_data)[0]

if prediction == 1:
    result = "SUSPICIOUS"
else:
    result = "NORMAL"

print("\nPrediction:", result)

# Save prediction to CSV
log_file = "data/prediction_logs.csv"

log_data = pd.DataFrame({
    "packets": [packets],
    "bytes": [bytes_sent],
    "failed_logins": [failed_logins],
    "prediction": [result]
})

# Create file if it doesn't exist, otherwise add a new row
if os.path.exists(log_file):
    log_data.to_csv(log_file, mode="a", header=False, index=False)
else:
    log_data.to_csv(log_file, index=False)

print("Prediction saved successfully!")