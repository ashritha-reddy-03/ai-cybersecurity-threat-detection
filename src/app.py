from flask import Flask, render_template, request, redirect
import pandas as pd
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates")
)

model = joblib.load(
    os.path.join(BASE_DIR, "models", "decision_tree_model.pkl")
)


@app.route("/", methods=["GET", "POST"])
def home():

    log_file = os.path.join(
        BASE_DIR,
        "data",
        "prediction_logs.csv"
    )

    message = ""

    if request.method == "POST":

        packets = int(request.form["packets"])
        bytes_sent = int(request.form["bytes"])
        failed_logins = int(request.form["failed_logins"])

        new_data = pd.DataFrame({
            "packets": [packets],
            "bytes": [bytes_sent],
            "failed_logins": [failed_logins]
        })

        prediction = model.predict(new_data)[0]

        if prediction == 1:
            result = "SUSPICIOUS"
        else:
            result = "NORMAL"

        log_data = pd.DataFrame({
            "packets": [packets],
            "bytes": [bytes_sent],
            "failed_logins": [failed_logins],
            "prediction": [result]
        })

        if os.path.exists(log_file):
            log_data.to_csv(
                log_file,
                mode="a",
                header=False,
                index=False
            )
        else:
            log_data.to_csv(
                log_file,
                index=False
            )

        message = f"Prediction: {result}"
        return redirect("/")

    data = pd.read_csv(log_file)

    total = len(data)
    normal = (data["prediction"] == "NORMAL").sum()
    suspicious = (data["prediction"] == "SUSPICIOUS").sum()
    threat_percentage = (
        (suspicious / total) * 100
        if total > 0 else 0
    )

    if threat_percentage < 30:
        threat_level = "LOW"
    elif threat_percentage <= 60:
        threat_level = "MEDIUM"
    else:
        threat_level = "HIGH"

    latest = data.iloc[-1]

    return render_template(
        "index.html",
        total=total,
        normal=normal,
        suspicious=suspicious,
        threat_percentage=round(threat_percentage, 2),
        threat_level=threat_level,
        latest=latest,
        message=message,
        history=data.to_dict("records")
    )


if __name__ == "__main__":
    app.run(debug=True)