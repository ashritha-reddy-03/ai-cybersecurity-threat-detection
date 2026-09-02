import pandas as pd

# Read prediction history
data = pd.read_csv("data/prediction_logs.csv")

# Overall statistics
total = len(data)
normal = (data["prediction"] == "NORMAL").sum()
suspicious = (data["prediction"] == "SUSPICIOUS").sum()

if total > 0:
    threat_percentage = (suspicious / total) * 100
else:
    threat_percentage = 0

# Get latest prediction
latest = data.iloc[-1]

# Display dashboard
print("\n====================================")
print("     AI CYBERSECURITY DASHBOARD")
print("====================================")

print(f"Total Traffic       : {total}")
print(f"Normal Traffic      : {normal}")
print(f"Suspicious Traffic  : {suspicious}")
print(f"Threat Percentage   : {threat_percentage:.2f}%")

print("\nLatest Activity")
print("------------------------------------")
print(f"Packets             : {latest['packets']}")
print(f"Bytes               : {latest['bytes']}")
print(f"Failed Logins       : {latest['failed_logins']}")
print(f"Status              : {latest['prediction']}")

print("====================================")