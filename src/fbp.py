from fbprophet import Prophet
from fbprophet.diagnostics import performance_metrics, cross_validation
import sqlalchemy as sa
import pandas as pd
import matplotlib.pyplot as plt

engine_local = sa.create_engine('postgres://o:password@localhost/wow')

query = ('''
        SELECT area52_daily.when, area52_daily.priceavg, name_enus
        FROM area52_daily
        INNER JOIN item_name on area52_daily.item=item_name.id
        ''')

df = pd.read_sql(query, engine_local)
df = df.sort_values(by='when')

mask = df['name_enus']=='Greater Flask of the Currents'
data = df[mask][['when','priceavg']].rename(columns={'when':'ds','priceavg':'y'})

m = Prophet()
m.fit(data)
# future = m.make_future_dataframe(periods=31)
# forecast = m.predict(future)
# fig1 = m.plot(forecast)
# fig2 = m.plot_components(forecast)
# plt.show()

df_cv = cross_validation(m, initial='21 days', period='7 days', horizon='14 days')
print(df_cv.head())
df_p = performance_metrics(df_cv)
print(df_p.head())