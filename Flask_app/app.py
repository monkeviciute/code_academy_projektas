import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

PATH = r"finalized_model.pickle"

with open(f'{PATH}', 'rb') as handle:
    model = pickle.load(handle)

# Create flask app
flask_app = Flask(__name__)

@flask_app.route("/")
def Home():
    return render_template("index.html")

@flask_app.route("/predict", methods = ["POST"])
def predict():
    float_features = [float(x) for x in request.form.values()]
    features = [np.array(float_features)]
    prediction = model.predict(features).tolist()[0]
    zodynas = {0: "gerą reitingą turinčių žurnalų grupei", 1: "mažiausiai prestižinių žurnalų grupei",
               2: "vidutinės svarbos žurnalų grupei", 3: "labiausiai cituojamų žurnalų grupei",
               4 : "prestižiškiausių žurnalų grupei"}

    #return {"results": prediction}
    return render_template("index.html", prediction_text = "Žurnalas priskiriamas {}".format(zodynas[prediction]))

@flask_app.route("/test")
def test_ok():
    return {"result": "ok"}

if __name__ == "__main__":
    flask_app.run(debug=True)