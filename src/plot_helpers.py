import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_recipe(df, dict, to_sell, all=False, proc=1.5):
    sell_mask = df['name_enus']==to_sell
    total_cost = pd.Series(np.zeros(df[sell_mask].shape[0]))
    for ing in list(dict.keys()):
        mask = df['name_enus']==ing
        cost = df[mask].priceavg*dict[ing]
        if ing != to_sell:
            total_cost = total_cost.add(cost.reset_index(drop=True))
        if all is True:
            plt.plot(df[mask].when, cost, label=ing)
    plt.plot(df[sell_mask].when, total_cost, label='Cost')
    profit = df[sell_mask].priceavg.reset_index(drop=True).multiply(proc).add(-total_cost)
    plt.plot(df[sell_mask].when, profit, label='Profit')
    plt.legend()
    plt.show()