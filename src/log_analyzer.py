import csv

file_path = "data/sample_traffic.csv"

total_records = 0
suspicious_records = 0

with open(file_path, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        total_records += 1

        failed_logins = int(row["failed_logins"])
        packets = int(row["packets"])

        if failed_logins > 5:
            suspicious_records += 1
            print("⚠️ Suspicious Activity Detected")
            print("Source IP:", row["source_ip"])
            print("Reason: Multiple failed login attempts")
            print()

        elif packets > 1000:
            suspicious_records += 1
            print("⚠️ Suspicious Activity Detected")
            print("Source IP:", row["source_ip"])
            print("Reason: Unusually high packet volume")
            print()

normal_records = total_records - suspicious_records

print("========== Analysis Summary ==========")
print("Total records analyzed:", total_records)
print("Suspicious records:", suspicious_records)
print("Normal records:", normal_records)