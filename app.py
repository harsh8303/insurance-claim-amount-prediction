from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd


app = Flask(__name__)
with open("regmodel.pkl", "rb") as f:
    pickle_model = pickle.load(f)

model = pickle_model["model"]
preprocessor = pickle_model["preprocessor"]

@app.route("/", methods=["GET","POST"])
def index():
    prediction=None

    if request.method == "POST":
        
        
        data={
        "policy_type" : [request.form["policy_type"]],
        "accident_type" :[request.form["accident_type"]],
        "claim_severity_level" : [request.form["claim_severity_level"]],
        "vehicle_category" :[request.form["vehicle_category"]],
        "area_type" :[request.form["area_type"]],

        "vehicle_damage_score" :[float(request.form["vehicle_damage_score"])],
        "accident_impact_score" :[float(request.form["accident_impact_score"])],
        "repair_risk_index" : [float(request.form["repair_risk_index"])],
        "injury_severity_prob" :[float(request.form["injury_severity_prob"])],
        "overall_claim_risk" :[float(request.form["overall_claim_risk"])],
        "claim_description" : [request.form["claim_description"]]
        }

        input_df=pd.DataFrame(data)
        input_transformed = preprocessor.transform(input_df)
        prediction = model.predict(input_transformed)[0]

        
        


    return render_template("index.html",prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
