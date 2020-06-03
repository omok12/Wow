import sqlalchemy as sa
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.special import inv_boxcox
from src.fbp_helpers import *

engine_local = sa.create_engine('postgres://o:password@localhost/wow')

query = ('''
        SELECT area52_daily.when, area52_daily.priceavg, area52_daily.quantityavg, name_enus
        FROM area52_daily
        INNER JOIN item_name on area52_daily.item=item_name.id
        ''')

df = sql_call(engine_local, query)
mask = df['name_enus'] == 'Deep Sea Satin'
data = df[mask][['when', 'priceavg']].rename(columns={'when': 'ds', 'priceavg': 'y'})
std = data['y'].std() * 1.5
mean = data['y'].mean()
data = data[(data['y'] < mean + std) & (data['y'] > mean - std)]
# fig, ax = plt.subplots(1,2)
# ax[0].plot(data.ds, data.y)

yt, lmbda = stats.boxcox(data.y)
data.y = yt

m = Prophet(n_changepoints=20)
m.add_seasonality(period=30.4, fourier_order=5, name='monthly')
m.fit(data)
future = m.make_future_dataframe(periods=31)
forecast = m.predict(future)
print(forecast.columns)
# fig1 = m.plot(forecast)
# fig2 = m.plot_components(forecast)
# plt.show()
#
# df_cv = cross_validation(m, initial='62 days', period='1 days', horizon='7 days')
# print(df_cv.sort_values('ds').tail())
# df_cv['yhat'] = inv_boxcox(df_cv['yhat'], lmbda)
# df_cv['y'] = inv_boxcox(df_cv['y'], lmbda)
# print(df_cv.sort_values('ds').tail())
# df_p = performance_metrics(df_cv)
# print(df_p.head())




# ax[1].plot(data.ds, yt)
# plt.show()