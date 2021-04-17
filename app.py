import scraping
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from os import path
from database import Database
from pymongo import MongoClient

app = Flask(__name__)


def clean_data(filename):
    df_shows = pd.read_csv(filename)
    df_shows['on_air'] = "À L'ANTENNE" in df_shows['Nom']
    dictionary = {True: "On air", False: "Finished"}
    df_shows['on_air'] = df_shows['on_air'].map(dictionary)
    df_shows['Nom'] = df_shows['Nom'].str.replace("À L'ANTENNE", '')
    df_shows.sort_values('Nom', inplace=True)
    df_shows.drop_duplicates(subset="Nom", keep=False, inplace=True)
    return df_shows


def to_database():
    if path.exists('viki_shows.csv'):
        scraping.to_csv(scraping.scrape_infos())
        database = Database(clean_data('viki_shows.csv'))
        database.update()
    else:
        scraping.to_csv(scraping.scrape_infos())
        database = Database(clean_data('viki_shows.csv'))
        database.insert()


def get_series():
    database = Database(clean_data('viki_shows.csv'))
    types = []
    cur = database.get_types()
    for elt in cur:
        types.append(elt['_id'])
    return types


def get_countries_names():
    database = Database(clean_data('viki_shows.csv'))
    countries = []
    cur = database.get_countries()
    for elt in cur:
        countries.append(elt['_id'])
    return countries


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search_program", methods=["POST", "GET"])
def search_program():
    if request.method == "POST":
        types = request.form["types"]
        countries = request.form["countries"]

        return redirect(url_for("display_results", types=types, country=countries))
    else:
        return render_template("search_program.html", types=get_series(), countries=get_countries_names())


@app.route("/display_results<types>&<country>")
def display_results(types, country):
    client = MongoClient()
    db_viki = client.viki
    collection_viki = db_viki['shows']
    cur = collection_viki.find({'$and': [{'Type': types}, {'Pays': country}]}).sort('Note', -1).limit(10)
    res = list(cur)
    return render_template("results.html", results=res)


@app.route("/dashboard")
def show_dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    #to_database()
    app.run()
