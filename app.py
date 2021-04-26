import scraping
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from database import Database
from pymongo import MongoClient
import dash
import dash_core_components as dcc
import dash_html_components as html
import dashboard

app = Flask(__name__)

external_stylesheets = [{
    'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css',
    'rel': 'stylesheet',
    'integrity': 'sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6',
    'crossorigin': 'anonymous'
}]

external_scripts = [{
    'src': 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js',
    'integrity': 'sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf',
    'crossorigin': 'anonymous'
}]

dash_app0 = dash.Dash(__name__, external_scripts=external_scripts, external_stylesheets=external_stylesheets,
                      server=app, routes_pathname_prefix='/dashboard/')
dash_countries = dashboard.dash_countries()
dash_types = dashboard.dash_types()
dash_best_tv_shows = dashboard.dash_best_tv_shows()

dash_app0.layout = html.Section(className='page-section', style={'font-family': 'Raleway'}, children=[
    html.Div(className='container', children=[
        html.Div(className='product-item', children=[
            html.Div(className='product-item-title d-flex', children=[
                html.Div(className='bg-faded p-5 d-flex ml-auto rounded', children=[
                    html.H2(className='section-heading mb-0', children=[
                        html.Span(className='section-heading-upper', children='À propos de Viki'),
                    ])
                ])
            ]),
            dcc.Graph(
                id='dash_types',
                figure=dash_types
            )
        ])
    ])
])


def check_database():
    client = MongoClient()
    db_names = client.list_database_names()
    if 'viki' in db_names:
        return True
    return False


def clean_data(filename):
    df_show = pd.read_csv(filename)
    df_show['on_air'] = df_show['Nom'].str.contains("À L'ANTENNE")
    dictionary = {True: "On air", False: "Finished"}
    df_show['on_air'] = df_show['on_air'].map(dictionary)
    df_show['Nom'] = df_show['Nom'].str.replace("À L'ANTENNE", '')
    df_show.sort_values('Nom', inplace=True)
    df_show.drop_duplicates(subset="Nom", keep='last', inplace=True)
    return df_show


def to_database():
    if check_database():
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
    cur = collection_viki.find({'$and': [{'Type': types}, {'Pays': country}, {'on_air': option}]}).sort('Note',
                                                                                                        -1).limit(10)
    res = list(cur)
    return render_template("results.html", results=res, length=len(res))


if __name__ == "__main__":
    # to_database()
    app.run(port=5000)
