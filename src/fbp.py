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

df = sql_call(engine_local, query)
item = 'Tidespray Linen'

forecast, ma = prophet_fit(df, item)



print(ma.tail())

# fig1 = m.plot(forecast)
# fig2 = m.plot_components(forecast)
# plt.show()

# df_cv = cross_validation(m, initial='62 days', period='1 days',horizon='7 days')
# print(df_cv.sort_values('ds').tail())
# df_p = performance_metrics(df_cv)
# print(df_p.head())