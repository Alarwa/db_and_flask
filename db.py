import flask
from flask import Flask, request
from json import loads
app = Flask("New")
from flask_cors import CORS, cross_origin
cors = CORS(app)


@app.route("/")
def home():
    return "Done"


@cross_origin()
@app.route("/prior", methods=["POST"])
def prior():
    with open("prior.csv", "a") as f:
        answers = request.data
        answers = loads(answers)["body"]
        f.writelines(",".join(list(loads(answers).values()))+"\n")

        return "Done"


@cross_origin()
@app.route("/questions", methods=["POST"])
def questions():
    with open("questions.csv", "a") as f:
        answers = request.data
        answers = loads(answers)["body"]
        f.writelines(",".join(list(loads(answers).values()))+"\n")

        return "Done"


@cross_origin()
@app.route("/feedback", methods=["POST"])
def feedback():
    with open("feedback.csv", "a") as f:
        answers = request.data
        answers = loads(answers)["body"]
        f.writelines(",".join(list(loads(answers).values()))+"\n")

        return "Done"


app.run(port=5001, debug=True)
