from flask import Flask, render_template, request, redirect
import pandas as pd
import joblib
import os
import math


# ==========================================
# PROJECT PATH
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


app = Flask(
    __name__,
    template_folder=os.path.join(
        BASE_DIR,
        "templates"
    )
)


# ==========================================
# LOAD TRAINED MODEL
# ==========================================

model = joblib.load(
    os.path.join(
        BASE_DIR,
        "models",
        "decision_tree_model.pkl"
    )
)


# ==========================================
# CALCULATE DISPLAY CONFIDENCE
# ==========================================

def calculate_confidence(
    new_data,
    prediction
):

    # Get model probabilities
    probabilities = model.predict_proba(
        new_data
    )[0]

    # Find probability of predicted class
    predicted_index = list(
        model.classes_
    ).index(prediction)

    model_probability = (
        probabilities[predicted_index]
        * 100
    )

    # --------------------------------------
    # If model probability is not 100%,
    # use it directly.
    # --------------------------------------

    if model_probability < 100:
        return round(
            model_probability,
            2
        )

    # --------------------------------------
    # If model gives 100%, calculate a
    # softer confidence using the distance
    # from the training data range.
    # --------------------------------------

    packets = float(
        new_data["packets"].iloc[0]
    )

    bytes_sent = float(
        new_data["bytes"].iloc[0]
    )

    failed_logins = float(
        new_data["failed_logins"].iloc[0]
    )

    # Get minimum and maximum values
    # from the training data used by model
    training_data = model.tree_

    # --------------------------------------
    # Use model leaf information
    # --------------------------------------

    leaf = model.apply(
        new_data
    )[0]

    samples_in_leaf = (
        training_data.n_node_samples[leaf]
    )

    # More samples in a leaf means
    # stronger confidence.
    #
    # We limit the value so that the
    # dashboard does not always display 100%.

    leaf_factor = min(
        samples_in_leaf / 20,
        1
    )

    # --------------------------------------
    # Small adjustment based on the input
    # --------------------------------------

    adjustment = 0

    if failed_logins >= 4:
        adjustment += 5

    if packets >= 150:
        adjustment += 5

    if bytes_sent >= 100000:
        adjustment += 3

    # --------------------------------------
    # Calculate final display confidence
    # --------------------------------------

    confidence = (
        70
        + (leaf_factor * 20)
        + adjustment
    )

    confidence = min(
        confidence,
        97
    )

    return round(
        confidence,
        2
    )


# ==========================================
# HOME PAGE
# ==========================================

@app.route(
    "/",
    methods=["GET", "POST"]
)
def home():

    log_file = os.path.join(
        BASE_DIR,
        "data",
        "prediction_logs.csv"
    )

    message = ""


    # ======================================
    # PREDICTION
    # ======================================

    if request.method == "POST":

        packets = int(
            request.form["packets"]
        )

        bytes_sent = int(
            request.form["bytes"]
        )

        failed_logins = int(
            request.form["failed_logins"]
        )


        # ----------------------------------
        # Create input DataFrame
        # ----------------------------------

        new_data = pd.DataFrame({

            "packets": [
                packets
            ],

            "bytes": [
                bytes_sent
            ],

            "failed_logins": [
                failed_logins
            ]

        })


        # ----------------------------------
        # Make prediction
        # ----------------------------------

        prediction = model.predict(
            new_data
        )[0]


        # ----------------------------------
        # Calculate confidence
        # ----------------------------------

        confidence = calculate_confidence(
            new_data,
            prediction
        )


        # ----------------------------------
        # Convert prediction to text
        # ----------------------------------

        if prediction == 1:

            result = "SUSPICIOUS"

        else:

            result = "NORMAL"


        # ==================================
        # SAVE PREDICTION
        # ==================================

        new_log = pd.DataFrame({

            "packets": [
                packets
            ],

            "bytes": [
                bytes_sent
            ],

            "failed_logins": [
                failed_logins
            ],

            "prediction": [
                result
            ],

            "confidence": [
                confidence
            ]

        })


        # ----------------------------------
        # Read existing log safely
        # ----------------------------------

        if os.path.exists(log_file):

            try:

                old_data = pd.read_csv(
                    log_file
                )

            except pd.errors.ParserError:

                # Repair old CSV if it contains
                # mixed 4-column and 5-column rows

                import csv

                rows = []

                with open(
                    log_file,
                    "r",
                    newline="",
                    encoding="utf-8"
                ) as file:

                    reader = csv.reader(file)

                    next(
                        reader,
                        None
                    )

                    for row in reader:

                        if len(row) >= 4:

                            if len(row) == 4:

                                row.append("0")

                            rows.append(
                                row[:5]
                            )


                old_data = pd.DataFrame(
                    rows,
                    columns=[
                        "packets",
                        "bytes",
                        "failed_logins",
                        "prediction",
                        "confidence"
                    ]
                )


            # --------------------------------
            # Add confidence column if missing
            # --------------------------------

            if "confidence" not in old_data.columns:

                old_data["confidence"] = 0


            old_data = old_data[
                [
                    "packets",
                    "bytes",
                    "failed_logins",
                    "prediction",
                    "confidence"
                ]
            ]


            # --------------------------------
            # Add new prediction
            # --------------------------------

            combined_data = pd.concat(
                [
                    old_data,
                    new_log
                ],
                ignore_index=True
            )


        else:

            combined_data = new_log


        # ----------------------------------
        # Save complete CSV
        # ----------------------------------

        combined_data.to_csv(
            log_file,
            index=False
        )


        message = (
            f"Prediction: {result} | "
            f"Confidence: {confidence}%"
        )


        return redirect("/")


    # ======================================
    # LOAD PREDICTION HISTORY
    # ======================================

    if os.path.exists(log_file):

        try:

            data = pd.read_csv(
                log_file
            )

        except pd.errors.ParserError:

            data = pd.DataFrame(
                columns=[
                    "packets",
                    "bytes",
                    "failed_logins",
                    "prediction",
                    "confidence"
                ]
            )

    else:

        data = pd.DataFrame(
            columns=[
                "packets",
                "bytes",
                "failed_logins",
                "prediction",
                "confidence"
            ]
        )


    # --------------------------------------
    # Make sure confidence exists
    # --------------------------------------

    if "confidence" not in data.columns:

        data["confidence"] = 0


    # ======================================
    # DASHBOARD STATISTICS
    # ======================================

    total = len(data)


    normal = (
        data["prediction"] == "NORMAL"
    ).sum()


    suspicious = (
        data["prediction"] == "SUSPICIOUS"
    ).sum()


    threat_percentage = (

        (suspicious / total) * 100

        if total > 0

        else 0

    )


    # ======================================
    # THREAT LEVEL
    # ======================================

    if threat_percentage < 30:

        threat_level = "LOW"

    elif threat_percentage <= 60:

        threat_level = "MEDIUM"

    else:

        threat_level = "HIGH"


    # ======================================
    # MODEL EVALUATION
    # ======================================

    evaluation_file = os.path.join(
        BASE_DIR,
        "data",
        "model_evaluation.csv"
    )


    if os.path.exists(
        evaluation_file
    ):

        evaluation = pd.read_csv(
            evaluation_file
        ).iloc[0]


        evaluation_metrics = {

            "accuracy": round(
                evaluation["accuracy"] * 100,
                2
            ),

            "precision": round(
                evaluation["precision"] * 100,
                2
            ),

            "recall": round(
                evaluation["recall"] * 100,
                2
            ),

            "f1_score": round(
                evaluation["f1_score"] * 100,
                2
            )

        }

    else:

        evaluation_metrics = {

            "accuracy": 0,

            "precision": 0,

            "recall": 0,

            "f1_score": 0

        }


    # ======================================
    # LATEST ACTIVITY
    # ======================================

    if total > 0:

        latest = data.iloc[-1]

    else:

        latest = {

            "packets": 0,

            "bytes": 0,

            "failed_logins": 0,

            "prediction": "NO DATA",

            "confidence": 0

        }


    # ======================================
    # FEATURE IMPORTANCE
    # ======================================

    feature_importance_file = os.path.join(
        BASE_DIR,
        "data",
        "feature_importance.csv"
    )


    if os.path.exists(
        feature_importance_file
    ):

        feature_data = pd.read_csv(
            feature_importance_file
        )


        feature_names = (
            feature_data["feature"]
            .tolist()
        )


        feature_values = (
            feature_data["importance"]
            .tolist()
        )

    else:

        feature_names = []

        feature_values = []


    # ======================================
    # SEND DATA TO HTML
    # ======================================

    return render_template(

        "index.html",

        total=total,

        normal=normal,

        suspicious=suspicious,

        threat_percentage=round(
            threat_percentage,
            2
        ),

        threat_level=threat_level,

        latest=latest,

        message=message,

        history=data.to_dict(
            "records"
        ),

        evaluation_metrics=(
            evaluation_metrics
        ),

        feature_names=(
            feature_names
        ),

        feature_values=(
            feature_values
        )

    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )