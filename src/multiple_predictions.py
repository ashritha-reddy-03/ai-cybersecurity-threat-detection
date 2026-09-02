import joblib
import pandas as pd
import os

# Load the trained model
model = joblib.load("models/decision_tree_model.pkl")

print("AI Cybersecurity Threat Detection System")
print("-----------------------------------------")

# Ask how many records to test
number = int(input("How many traffic records do you want to test? "))

for i in range(number):

    print(f"\nTraffic {i + 1}")

    packets = int(input("Enter number of packets: "))
    bytes_sent = int(input("Enter number of bytes: "))
    failed_logins = int(input("Enter number of failed logins: "))

    # Create input data
    new_data = pd.DataFrame({
        "packets": [packets],
        "bytes": [bytes_sent],
        "failed_logins": [failed_logins]
    })

    # Make prediction
    prediction = model.predict(new_data)[0]

    if prediction == 1:
        result = "SUSPICIOUS"
    else:
        result = "NORMAL"

    print("Prediction:", result)

    # Save prediction
    log_file = "data/prediction_logs.csv"

    log_data = pd.DataFrame({
        "packets": [packets],
        "bytes": [bytes_sent],
        "failed_logins": [failed_logins],
        "prediction": [result]
    })

    if os.path.exists(log_file):
        log_data.to_csv(log_file, mode="a", header=False, index=False)
    else:
        log_data.to_csv(log_file, index=False)

print("\nAll predictions saved successfully!")