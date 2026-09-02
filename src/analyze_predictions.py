import pandas as pd

# Read prediction history
log_file = "data/prediction_logs.csv"
data = pd.read_csv(log_file)

# Count predictions
total = len(data)
normal = (data["prediction"] == "NORMAL").sum()
suspicious = (data["prediction"] == "SUSPICIOUS").sum()

# Calculate threat percentage
if total > 0:
    threat_percentage = (suspicious / total) * 100
else:
    threat_percentage = 0

# Display summary
print("\nCybersecurity Prediction Summary")
print("--------------------------------")
print("Total Predictions:", total)
print("Normal Traffic:", normal)
print("Suspicious Traffic:", suspicious)
print("Threat Percentage:", round(threat_percentage, 2), "%")