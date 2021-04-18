import scraping
import pandas as pd
import dashboard
from flask import Flask, render_template, request, redirect, url_for
from os import path
from database import Database
from pymongo import MongoClient

app = Flask(__name__)


def clean_data(filename):
    df_show = pd.read_csv(filename)
    print(len(df_show))
    df_show['on_air'] = df_show['Nom'].str.contains("À L'ANTENNE")
    dictionary = {True: "On air", False: "Finished"}
    df_show['on_air'] = df_show['on_air'].map(dictionary)
    df_show['Nom'] = df_show['Nom'].str.replace("À L'ANTENNE", '')
    df_show.sort_values('Nom', inplace=True)
    df_show.drop_duplicates(subset="Nom", keep='last', inplace=True)
    return df_show


def to_database():
    if path.exists('viki_shows.csv'):
        scraping.to_csv(scraping.scrape_infos())
        database = Database()
        database.update(clean_data('viki_shows.csv'))
    else:
        scraping.to_csv(scraping.scrape_infos())
        database = Database()
        database.insert(clean_data('viki_shows.csv'))


def get_series():
    database = Database()
    types = []
    cur = database.get_types()
    for elt in cur:
        types.append(elt['_id'])
    return types


def get_countries_names():
    database = Database()
    countries = []
    cur = database.get_countries()
    for elt in cur:
        countries.append(elt['_id'])
    return countries


def get_options():
    database = Database()
    options = []
    cur = database.get_on_air()
    for elt in cur:
        options.append(elt['_id'])
    return options


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search_program", methods=["POST", "GET"])
def search_program():
    if request.method == "POST":
        types = request.form["types"]
        countries = request.form["countries"]
        options = request.form['options']
        return redirect(url_for("display_results", types=types, country=countries, option=options))
    else:
        return render_template("search_program.html", types=get_series(), countries=get_countries_names(),
                               options=get_options())


@app.route("/display_results<types>&<country>&<option>")
def display_results(types, country, option):
    client = MongoClient()
    db_viki = client.viki
    collection_viki = db_viki['shows']
    cur = collection_viki.find({'$and': [{'Type': types}, {'Pays': country}, {'on_air':option}]}).sort('Note', -1).limit(10)
    res = list(cur)
    return render_template("results.html", results=res, length=len(res))


@app.route("/dashboard")
def show_dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    to_database()
    app.run()
