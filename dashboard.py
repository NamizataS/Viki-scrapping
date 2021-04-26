from database import Database
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from matplotlib.patches import ConnectionPatch

database = Database()


def dash_countries():
    cur = database.get_countries()
    res = pd.DataFrame(list(cur))
    fig = px.bar(res, x='_id', y='number_of_shows', color='_id', title='Le nombre de programme en fonction des pays')
    return fig


def dash_types():
    cur = database.get_types()
    res = pd.DataFrame(list(cur))
    type_shows = res['TypeShows']
    labels = res['_id']
    colors = ['#701f57', '#c2c2f0']
    fig = go.Figure(data=[go.Pie(labels=labels, values=type_shows, marker_colors=colors, pull=[0.05, 0.05])])
    return fig


def get_df():
    cur_total = database.get_countries()
    res_total = pd.DataFrame(list(cur_total))
    cur_repart = database.get_countries_types()
    res_repart = pd.DataFrame(list(cur_repart))
    res_repart = pd.concat([res_repart.drop(['_id'], axis=1), res_repart['_id'].apply(pd.Series)], axis=1)
    res_repart.sort_values('pays', inplace=True)
    return res_total, res_repart


def dash_countries_type():
    res_total, res_repart = get_df()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 5))
    fig.subplots_adjust(wspace=0)

    labels_total = res_total['_id']
    sum_res = res_total.sum(axis=0, skipna=True)
    ratios = res_total['showsNumber'] / sum_res['showsNumber']
    explode_total = (0.1, 0, 0.2, 0.2, 0.2)
    angle = -180 * ratios[0]
    colors_total = ['#f7a889', '#feda7e', '#bad6eb', '#a03704', '#be7c89']
    ax1.pie(ratios, autopct='%1.1f%%', startangle=angle, labels=labels_total, colors=colors_total,
            explode=explode_total, normalize=False)

    xpos = 0
    bottom = 0
    ratios = [.93, .08]
    width = .2
    colors_repart = ['#701f57', '#c2c2f0']

    for j in range(len(ratios)):
        height = ratios[j]
        ax2.bar(xpos, height, width, bottom=bottom, color=colors_repart[j])
        ypos = bottom + ax2.patches[j].get_height() / 2
        bottom += height
        ax2.text(xpos, ypos, "%d%%" % (ax2.patches[j].get_height() * 100), ha='center')

    ax2.set_title('Type')
    ax2.legend(('Série', 'Film'))
    ax2.axis('off')
    ax2.set_xlim(- 2.5 * width, 2.5 * width)

    theta1, theta2 = ax1.patches[0].theta1, ax1.patches[0].theta2
    center, r = ax1.patches[0].center, ax1.patches[0].r
    bar_height = sum([item.get_height() for item in ax2.patches])

    # draw top connecting line
    x = r * np.cos(np.pi / 180 * theta2) + center[0]
    y = r * np.sin(np.pi / 180 * theta2) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, bar_height), coordsA=ax2.transData, xyB=(x, y), coordsB=ax1.transData)
    con.set_color([0, 0, 0])
    con.set_linewidth(2)
    ax2.add_artist(con)

    # draw bottom connecting line
    x = r * np.cos(np.pi / 180 * theta1) + center[0]
    y = r * np.sin(np.pi / 180 * theta1) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData, xyB=(x, y), coordsB=ax1.transData)
    con.set_color([0, 0, 0])
    ax2.add_artist(con)
    con.set_linewidth(2)
    return fig


def dash_best_tv_shows():
    cur = database.get_best_tv_shows()
    df_res = pd.DataFrame(list(cur))
    explode = [.1, 0]
    colors = ['#f7a889', '#be7c89']
    df_res['numbers_of_shows'] = 1
    df_res = df_res.groupby('Pays', as_index=False).sum()
    #fig = df_res.pivot_table('_id', index='Pays', aggfunc='count').plot(kind='pie', subplots=True, colors=colors,
                                                                 # explode=explode, autopct='%1.1f%%', shadow=True,
                                                                  #figsize=(8, 8), startangle=90)
    labels = df_res['Pays']
    values = df_res['numbers_of_shows']
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0.05,0.05])])
    return fig
