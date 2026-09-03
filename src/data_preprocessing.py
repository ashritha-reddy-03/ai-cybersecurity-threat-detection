import pandas as pd

file_path = "data/sample_traffic.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print(df)
print("\nColumn names:")
print(df.columns)

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())
df["label"] = ((df["failed_logins"] > 5) | (df["packets"] > 1000)).astype(int)

print("\nDataset with labels:")
print(df)
features = ["packets", "bytes", "failed_logins"]

X = df[features]
y = df["label"]

print("\nFeatures (X):")
print(X)

print("\nTarget (y):")
print(y)
ml_data = X.copy()
ml_data["label"] = y

ml_data.to_csv("data/ml_ready_data.csv", index=False)

print("\nML-ready dataset saved successfully!")
print("File: data/ml_ready_data.csv")python 