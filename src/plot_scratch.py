import sqlalchemy as sa
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

engine_local = sa.create_engine('postgres://o:password@localhost/wow')

query = ('''
        SELECT area52_daily.when, area52_daily.priceavg, name_enus
        FROM area52_daily
        INNER JOIN item_name on area52_daily.item=item_name.id

        ''')

df = pd.read_sql(query, engine_local)
df = df.sort_values(by='when')

recipe = {'Zin\'anthid':25,
          'Anchor Weed':10,
          'Sea Stalk':8,
          'Greater Flask of the Currents':1
          }
print(list(recipe.keys()))


def plot_recipe(df, dict, to_sell):
    temp = pd.Series(np.zeros(93))
    for ing in list(dict.keys()):
        mask = df['name_enus']==ing
        cost = df[mask].priceavg*dict[ing]
        if ing != to_sell:
            temp = temp.add(cost.reset_index(drop=True))
        plt.plot(df[mask].when, cost, label=ing)
    sell_mask = df['name_enus']==to_sell
    plt.plot(df[sell_mask].when, temp, label='Cost')
    profit = df[sell_mask].priceavg.reset_index(drop=True).multiply(dict[to_sell]).add(-temp)
    plt.plot(df[sell_mask].when, profit, label='Profit')
    plt.plot()

to_sell = 'Greater Flask of the Currents'
plot_recipe(df, recipe, to_sell)
plt.legend()
plt.show()

