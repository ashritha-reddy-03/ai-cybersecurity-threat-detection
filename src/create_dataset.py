import pandas as pd
import random

data = []

for i in range(180):

    # Generate normal traffic
    if random.random() < 0.45:

        packets = random.randint(10, 150)
        bytes_sent = random.randint(500, 200000)
        failed_logins = random.randint(0, 3)

        label = 0

    # Generate suspicious traffic
    else:

        packets = random.randint(80, 3000)
        bytes_sent = random.randint(5000, 1000000)
        failed_logins = random.randint(2, 15)

        label = 1

    data.append([
        packets,
        bytes_sent,
        failed_logins,
        label
    ])


# ==========================================
# ADD SOME BORDERLINE NORMAL RECORDS
# ==========================================

for i in range(10):

    packets = random.randint(100, 250)
    bytes_sent = random.randint(100000, 300000)
    failed_logins = random.randint(2, 4)

    label = 0

    data.append([
        packets,
        bytes_sent,
        failed_logins,
        label
    ])


# ==========================================
# ADD SOME BORDERLINE SUSPICIOUS RECORDS
# ==========================================

for i in range(10):

    packets = random.randint(100, 250)
    bytes_sent = random.randint(50000, 200000)
    failed_logins = random.randint(4, 8)

    label = 1

    data.append([
        packets,
        bytes_sent,
        failed_logins,
        label
    ])


# ==========================================
# CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(
    data,
    columns=[
        "packets",
        "bytes",
        "failed_logins",
        "label"
    ]
)


# ==========================================
# SAVE DATASET
# ==========================================

df.to_csv(
    "data/cybersecurity_dataset.csv",
    index=False
)


# ==========================================
# DISPLAY INFORMATION
# ==========================================

print("Dataset created successfully!")

print("Number of records:", len(df))

print("\nFirst 10 records:")
print(df.head(10))

print("\nLabel distribution:")
print(df["label"].value_counts())

print("\nAverage values by label:")

print(
    df.groupby("label")[
        ["packets", "bytes", "failed_logins"]
    ].mean()
)