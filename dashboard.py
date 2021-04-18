from database import Database
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

database = Database()


def dash_countries():
    cur = database.get_countries()
    res = pd.DataFrame(list(cur))
    plt.figure(figsize=(8, 8))
    plt.title('Le nombre de programme en fonction des pays')
    sns.barplot(x='showsNumber', y='_id', data=res, palette='rocket')
    plt.show()


def dash_types():
    cur = database.get_types()
    res = pd.DataFrame(list(cur))
    explode = (0.05, 0.05)
    colors = ['#701f57', '#c2c2f0']

    fig1, ax1 = plt.subplots()
    type_shows = res['TypeShows']
    labels = res['_id']
    ax1.pie(type_shows, explode=explode, labels=labels, pctdistance=0.85, autopct='%1.1f%%', shadow=True, colors=colors,
            startangle=90)
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    ax1.axis('equal')
    ax1.set_title('Répartition des différents types de programmes')
    plt.tight_layout()
    plt.savefig('static/img/dash_types.png')



