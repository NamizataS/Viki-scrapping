from database import Database
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
database = Database()


def dash_countries():
    cur = database.get_countries()
    res = pd.DataFrame(list(cur))
    plt.figure(figsize=(8, 8))
    plt.title('Le nombre de programmes en fonction des pays')
    sns.barplot(x='showsNumber', y='_id', data=res, palette='dark:salmon_r')
    plt.show()
