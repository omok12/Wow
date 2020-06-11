import pickle
import pandas as pd
from scipy.special import inv_boxcox
import random

df = pd.read_pickle('../data/profit_df.pkl')
df.fillna(df.mean())
print(df.sum())

# N = df.shape[0]
# d = df.shape[1]
# selected = []
# total_reward = 0
# for n in range(0, N):
#     ad = random.randrange(d)
#     selected.append(ad)
#     reward = df.values[n, ad]
#     total_reward = total_reward + reward
#
# print(pd.Series(selected).value_counts(normalize=True))
# print(total_reward)
#
import math
N = df.shape[0]
d = df.shape[1]
selected = []
numbers_of_selections = [0] * d
sums_of_reward = [0] * d
total_reward = 0

for n in range(0, N):
    ad = 0
    max_upper_bound = 0
    for i in range(0, d):
        if (numbers_of_selections[i] > 0):
            average_reward = sums_of_reward[i] / numbers_of_selections[i]
            delta_i = math.sqrt(2 * math.log(n+1) / numbers_of_selections[i])
            upper_bound = average_reward + delta_i
        else:
            upper_bound = 1e400
        if upper_bound > max_upper_bound:
            max_upper_bound = upper_bound
            ad = i
    selected.append(ad)
    numbers_of_selections[ad] += 1
    reward = df.values[n, ad]
    sums_of_reward[ad] += reward
    total_reward += reward
    print(selected)

print(pd.Series(selected).value_counts(normalize=True))
print(total_reward)

print(df.describe().max())

