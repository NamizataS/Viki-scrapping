from database import Database
import pandas as pd
import plotly.graph_objects as go

database = Database()
text_colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


def dash_countries():
    cur = database.get_countries()
    res = pd.DataFrame(list(cur))
    res = res.rename(columns={'_id': 'Pays', 'number_of_shows': 'Nombre de programmes'})
    x = res['Pays']
    y = res['Nombre de programmes']
    colors = ['#35193e', '#701f57', '#ad1759', '#f37651', '#f6b48f']
    fig = go.Figure(data=go.Bar(x=x, y=y, marker_color=colors))
    fig.update_layout(title="Le nombre de programmes en fonction du pays",
                      yaxis=dict(title='Nombre de programmes', titlefont_size=16, tickfont_size=14),
                      plot_bgcolor=text_colors['background'],
                      paper_bgcolor=text_colors['background'],
                      font_color=text_colors['text'])
    return fig


def dash_types():
    cur = database.get_types()
    res = pd.DataFrame(list(cur))
    type_shows = res['TypeShows']
    labels = res['_id']
    colors = ['#701f57', '#c2c2f0']
    fig = go.Figure(data=[go.Pie(labels=labels, values=type_shows, marker_colors=colors, pull=[0.05, 0.05])])
    fig.update_layout(title_text='La répartition des différents types de programmes de Viki',
                      plot_bgcolor=text_colors['background'],
                      paper_bgcolor=text_colors['background'],
                      font_color=text_colors['text'])
    return fig


def dash_best_tv_shows():
    cur = database.get_best_tv_shows()
    df_res = pd.DataFrame(list(cur))
    colors = ['#f7a889', '#be7c89']
    df_res['numbers_of_shows'] = 1
    df_res = df_res.groupby('Pays', as_index=False).sum()
    labels = df_res['Pays']
    values = df_res['numbers_of_shows']
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker_colors=colors, pull=[0.05, 0.05])])
    fig.update_layout(title_text="Répartion des pays des 5 meilleures séries", plot_bgcolor=text_colors['background'],
                      paper_bgcolor=text_colors['background'],
                      font_color=text_colors['text'])
    return fig
