from fbprophet import Prophet
from fbprophet.diagnostics import performance_metrics, cross_validation
import sqlalchemy as sa
import pandas as pd
import matplotlib.pyplot as plt
from src.fbp_helpers import *


engine_local = sa.create_engine('postgres://o:password@localhost/wow')

query = ('''
        SELECT area52_daily.when, area52_daily.priceavg, area52_daily.quantityavg, name_enus
        FROM area52_daily
        INNER JOIN item_name on area52_daily.item=item_name.id
        ''')
item = 'Coarse Leather'
p = ProphetProfit(engine_local, query, item)
p.plot()
# p.make_profit('2020-05-24')
p.cross_val()
#
# positive_trend = []
# negative_trend = []
#
# for item in item_list(df):
#     print(item)
#     m, forecast, ma = prophet_fit(df, item)
#     positive_trend, negative_trend = make_lists(ma, item, positive_trend, negative_trend)
#     if len(positive_trend) > 10:
#         break
# print(positive_trend)
# print(negative_trend)

# m, forecast, ma, lmbda = prophet_fit(df, 'Monelite Ore')
# print(forecast.columns)
# buy_date = '2020-05-20'
# buy_price =

# fig1 = m.plot(forecast)
# fig2 = m.plot_components(forecast)
# plt.show()
# cross_val(m, lmbda)
