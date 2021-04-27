import plotly.graph_objects as go
from flask import Flask, render_template, request, redirect, url_for
from database import Database
from pymongo import MongoClient
import dash
import dash_core_components as dcc
import dash_html_components as html
import dashboard

database = Database()
text_colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
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
best_tv_shows = database.get_best_tv_shows()

output = []
for i in best_tv_shows:
    output.append(html.Div(className='card', style={'width': '15rem'},
                           children=[html.Img(src=i['image'], className='card-img-top'), html.Div(className='card-body', children=[
                               html.P(className='card-text',children=i['Nom']),html.P(className='card-text',children=i['Pays']),
                               html.P(className='card-text', children=i['Note'])
                           ])]))

dash_app0.layout = html.Div(style={'font-family': 'Raleway'},
                            children=[html.Section(className='page-section', children=[
                                html.Div(className='container', children=[
                                    html.Div(className='product-item', children=[
                                        dcc.Graph(
                                            id='dash_types',
                                            figure=dash_types
                                        )
                                    ])
                                ])
                            ]), html.Section(className='page-section', children=[
                                html.Div(className='container', children=[
                                    html.Div(className='product-item', children=[
                                        html.Label('Countries'),
                                        dcc.Dropdown(id='countries-dropdown',
                                                     options=[
                                                         {'label': 'All', 'value': 'All'},
                                                         {'label': 'Corée du Sud', 'value': 'Corée'},
                                                         {'label': 'Chine Continentale', 'value': 'Chine Continentale'},
                                                         {'label': 'Taïwan', 'value': 'Taïwan'},
                                                         {'label': 'Japon', 'value': 'Japon'},
                                                         {'label': 'La Thaïlande', 'value': 'La Thaïlande'}
                                                     ],
                                                     value='All'),
                                        dcc.Graph(
                                            id='dash_countries',
                                            figure=dash_countries
                                        )
                                    ])
                                ])
                            ]),
                                      html.Section(className='page-section',
                                                   children=[
                                                       html.Div(className='container', children=[
                                                           html.Div(className='product-item', children=[
                                                               dcc.Graph(
                                                                   id='dash_best_tv_shows',
                                                                   figure=dash_best_tv_shows
                                                               )
                                                           ]),
                                                           html.Div(className='row justify-content-center', children=[
                                                               html.Div(className='row', children=output)
                                                           ])
                                                       ])
                                                   ])
                                      ])


@dash_app0.callback(
    dash.dependencies.Output(component_id='dash_countries', component_property='figure'),
    [dash.dependencies.Input(component_id='countries-dropdown', component_property='value')]
)
def update_figure(input_value):
    if input_value == 'All':
        return dash_countries
    else:
        labels, values = database.get_repart_by_countries(input_value)
    colors = ['#f7a889', '#be7c89']
    fig = go.Figure(data=go.Pie(labels=labels, values=values, marker_colors=colors, hole=.3))
    fig.update_layout(title_text="Répartition des types de programmes", plot_bgcolor=text_colors['background'],
                      paper_bgcolor=text_colors['background'],
                      font_color=text_colors['text'])
    return fig


def check_database():
    client = MongoClient()
    db_names = client.list_database_names()
    if 'viki' in db_names:
        return True
    return False


def start_program():
    if check_database():
        app.run(port=5000)
    else:
        print("Veuillez lancer le fichier scraping.py tout d'abord")


def get_series():
    types = []
    cur = database.get_types()
    for elt in cur:
        types.append(elt['_id'])
    return types


def get_countries_names():
    countries = []
    cur = database.get_countries()
    for elt in cur:
        countries.append(elt['_id'])
    return countries


def get_options():
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
    start_program()
