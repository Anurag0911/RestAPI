import json
from unicodedata import category

from flask import jsonify, Flask
from flask_restful import Resource, Api

f = open("prize.json")
data = json.load(f)
prizes = data["prizes"]
f.close()

app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome to the application"

@app.route("/prizes")
def prizes():
    return data

@app.route("/prizes/name&<string:given_name>", methods=["GET"])
def name(given_name):
    name_list =[]
    for prize in data["prizes"]:
        for name in prize["laureates"]:
            if given_name in name["firstname"] + " " + name["surname"]:
                name_dict = {
                    "firstname" : name["firstname"],
                    "surname" : name["surname"],
                    "year" : prize["year"],
                    "category" : prize["category"]
                }
                name_list.append(name_dict)

    return jsonify(name_list)

@app.route("/prizes/year&<string:year>", methods=["GET"])
def year(year):
    yearlist = []
    for prize in data['prizes']:
            if year in prize['year']:
                for name in prize['laureates']:
                    yearDict = {
                        "firstname": name['firstname'],
                        "surname":name['surname'],
                        "year":prize['year'],
                        "category":prize['category']}
                    yearlist.append(yearDict)
    return jsonify(yearlist)

@app.route("/prizes/year&<string:year>/category&<string:category>", methods=["GET"])
def year_category(year,category):
    year_category_list = []
    for prize in data['prizes']:
        if year in prize['year'] and category in prize['category']:
            for name in prize['laureates']:
                year_category_dict = {
                    "firstname": name['firstname'],
                    "surname": name['surname'],
                    "year": prize['year'],
                    "category": prize['category']
                }
                year_category_list.append(year_category_dict)
    return jsonify(year_category_list)


@app.route("/sortedprizes")
def sortedprizes():
    sorted_list = []
    names, year, category= [], [], []
    for prize in data['prizes']:
        for name in prize['laureates']:
            names.append(name['firstname'] + ' ' +name['surname'])
            year.append(prize['year'])
            category.append(prize['category'])

        final_deatils = [{"name": n,"year": y, "category":c} for n, y, c in zip(names, year, category)]
        final_data = sorted(final_deatils, key=lambda k: k["name"])
        for details in final_data:
            year_category_dict = {
                details['name']:"name" ,
                "year":details['year'] ,
                "category":details['category']
            }
            sorted_list.append(year_category_dict)
    return jsonify(sorted_list)





if __name__ == "__main__":
    app.run(debug=True)
