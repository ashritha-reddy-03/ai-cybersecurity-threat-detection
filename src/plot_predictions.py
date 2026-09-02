import pandas as pd
import matplotlib.pyplot as plt

# Read prediction history
data = pd.read_csv("data/prediction_logs.csv")

# Count both categories
normal_count = (data["prediction"] == "NORMAL").sum()
suspicious_count = (data["prediction"] == "SUSPICIOUS").sum()

# Create values for graph
labels = ["NORMAL", "SUSPICIOUS"]
counts = [normal_count, suspicious_count]

# Create bar graph
plt.bar(labels, counts)

plt.title("Cybersecurity Threat Detection")
plt.xlabel("Prediction")
plt.ylabel("Number of Predictions")

plt.tight_layout()
plt.show()