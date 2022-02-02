import json
from unicodedata import category

f = open("prize.json")
data = json.load(f)
prizes = data["prizes"]
f.close()


from flask import jsonify, Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Welcome to the application"


@app.route("/prizes")
def prizes():
    return data


@app.route("prizes/name/<string:given_name>", methods=["GET"])
def name(given_name):
    for prize in data["prizes"]:
        for name in prize["laureates"]:
            if given_name in name["firstname"] + " " + name["surname"]:
                string = name["firstname"] + " " + name["surname"]+prize["year"] + prize["category"]
    return jsonify(string)


if __name__ == "__main__":
    app.run(debug=True)
