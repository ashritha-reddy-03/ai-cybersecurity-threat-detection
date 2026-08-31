import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# Load the ML-ready dataset
data = pd.read_csv("data/ml_ready_data.csv")

print("Dataset loaded successfully!")
print(data)

# Separate input features and target
X = data[["packets", "bytes", "failed_logins"]]
y = data["label"]

print("\nFeatures:")
print(X)

print("\nTarget:")
print(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

print("\nTraining rows:", len(X_train))
print("Testing rows:", len(X_test))
# Create the Decision Tree model
model = DecisionTreeClassifier(random_state=42)

# Train the model
model.fit(X_train, y_train)

print("\nModel trained successfully!")
# Make predictions on the test data
y_pred = model.predict(X_test)

print("\nPredictions:")
print(y_pred)

print("\nActual labels:")
print(y_test.values)
from sklearn.metrics import accuracy_score

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("\nAccuracy:", accuracy)
from sklearn.metrics import accuracy_score
import joblib

# Save the trained model
joblib.dump(model, "models/decision_tree_model.pkl")

print("\nModel saved successfully!")