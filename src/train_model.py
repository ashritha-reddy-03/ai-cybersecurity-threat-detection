import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)
import joblib


# ==========================================
# 1. LOAD DATASET
# ==========================================

data = pd.read_csv("data/cybersecurity_dataset.csv")

print("Dataset loaded successfully!")
print(data)


# ==========================================
# 2. SEPARATE FEATURES AND TARGET
# ==========================================

X = data[
    [
        "packets",
        "bytes",
        "failed_logins"
    ]
]

y = data["label"]


print("\nFeatures:")
print(X)

print("\nTarget:")
print(y)


# ==========================================
# 3. SPLIT DATA
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42
)

print("\nTraining rows:", len(X_train))
print("Testing rows:", len(X_test))


# ==========================================
# 4. CREATE DECISION TREE
# ==========================================

model = DecisionTreeClassifier(
    random_state=42,
    max_depth=4,
    min_samples_leaf=5
)


# ==========================================
# 5. TRAIN MODEL
# ==========================================

model.fit(
    X_train,
    y_train
)

print("\nModel trained successfully!")


# ==========================================
# 6. MAKE PREDICTIONS
# ==========================================

y_pred = model.predict(X_test)

print("\nPredictions:")
print(y_pred)

print("\nActual labels:")
print(y_test.values)


# ==========================================
# 7. MODEL EVALUATION
# ==========================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

cm = confusion_matrix(
    y_test,
    y_pred
)


# ==========================================
# 8. DISPLAY RESULTS
# ==========================================

print("\n==============================")
print("       MODEL EVALUATION")
print("==============================")

print("Accuracy :", accuracy)
print("Precision:", precision)
print("Recall   :", recall)
print("F1-Score :", f1)

print("\nConfusion Matrix:")
print(cm)


# ==========================================
# 9. FEATURE IMPORTANCE
# ==========================================

feature_importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
})


print("\n==============================")
print("      FEATURE IMPORTANCE")
print("==============================")

print(feature_importance)


# ==========================================
# 10. SAVE FEATURE IMPORTANCE
# ==========================================

feature_importance.to_csv(
    "data/feature_importance.csv",
    index=False
)

print("\nFeature importance saved successfully!")


# ==========================================
# 11. SAVE MODEL EVALUATION
# ==========================================

evaluation_results = {
    "accuracy": accuracy,
    "precision": precision,
    "recall": recall,
    "f1_score": f1
}

evaluation_df = pd.DataFrame([
    evaluation_results
])

evaluation_df.to_csv(
    "data/model_evaluation.csv",
    index=False
)

print("Evaluation results saved successfully!")


# ==========================================
# 12. SAVE TRAINED MODEL
# ==========================================

joblib.dump(
    model,
    "models/decision_tree_model.pkl"
)

print("Model saved successfully!")