# AI Cybersecurity Threat Detection System

## 1. Project Overview

The **AI Cybersecurity Threat Detection System** is a machine learning based web application designed to identify potentially suspicious network traffic.

The system analyzes network-related features such as:

- Number of packets
- Number of bytes
- Failed login attempts

A Decision Tree machine learning model is trained using these features and classifies network traffic as either:

- **NORMAL**
- **SUSPICIOUS**

The prediction results are displayed through a simple Flask web dashboard.

---

## 2. Problem Statement

Cybersecurity systems need to identify suspicious network activity quickly and accurately.

Traditional monitoring methods may require manual analysis of large amounts of network data. This can make it difficult to identify potentially harmful activity efficiently.

This project uses machine learning to automatically analyze network traffic features and classify them as normal or suspicious.

---

## 3. Objectives

The main objectives of this project are:

1. To create a dataset containing normal and suspicious network traffic.
2. To identify important features related to suspicious activity.
3. To train a machine learning model for threat detection.
4. To evaluate the model using accuracy, precision, recall and F1-score.
5. To develop a web-based interface for making predictions.
6. To maintain a history of previous predictions.
7. To display a confidence score for each prediction.
8. To provide a simple and understandable cybersecurity monitoring dashboard.

---

## 4. Technologies Used

### Programming Language

- Python

### Machine Learning

- Scikit-learn
- Decision Tree Classifier

### Data Processing

- Pandas

### Model Saving

- Joblib

### Web Framework

- Flask

### Frontend

- HTML
- CSS
- JavaScript

### Version Control

- Git
- GitHub

---

## 5. System Features

The system provides the following features:

### Threat Prediction

The user enters:

- Packets
- Bytes
- Failed Login Attempts

The trained model predicts whether the traffic is **NORMAL** or **SUSPICIOUS**.

### Confidence Score

The dashboard displays a confidence score along with the prediction.

### Prediction History

Previous predictions are stored in:

`data/prediction_logs.csv`

### Threat Statistics

The dashboard displays:

- Total predictions
- Normal predictions
- Suspicious predictions
- Threat percentage
- Threat level

### Model Performance

The dashboard provides model evaluation results including:

- Accuracy
- Precision
- Recall
- F1-score

### Feature Importance

The system displays the importance of the features used by the Decision Tree model.

---

## 6. Dataset

The project uses a generated cybersecurity dataset containing **200 records**.

The dataset contains the following columns:

| Feature | Description |
|---|---|
| packets | Number of packets |
| bytes | Number of bytes transferred |
| failed_logins | Number of failed login attempts |
| label | Target class |

The label represents:

- `0` = NORMAL
- `1` = SUSPICIOUS

The dataset is stored in:

`data/cybersecurity_dataset.csv`

---

## 7. Machine Learning Model

The project uses a **Decision Tree Classifier**.

The model is trained using:

- Packets
- Bytes
- Failed Login Attempts

The dataset is divided into:

- **75% training data**
- **25% testing data**

The model uses:

- `max_depth = 4`
- `min_samples_leaf = 5`
- `random_state = 42`

The trained model is saved as:

`models/decision_tree_model.pkl`

---

## 8. Model Performance

The trained Decision Tree model achieved the following results on the test dataset:

| Metric | Result |
|---|---:|
| Accuracy | 98% |
| Precision | 100% |
| Recall | 96.55% |
| F1-Score | 98.25% |

### Confusion Matrix

The confusion matrix was:

```text
[[21  0]
 [ 1 28]]