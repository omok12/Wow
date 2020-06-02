from fbprophet import Prophet
from fbprophet.diagnostics import performance_metrics, cross_validation
import sqlalchemy as sa
import pandas as pd
import matplotlib.pyplot as plt


def sql_call(engine, query):
    df = pd.read_sql(query, engine)
    df = df.sort_values(by='when')
    return df


def prophet_fit(df, item, periods=31):
    mask = df['name_enus'] == item
    data = df[mask][['when', 'priceavg']].rename(columns={'when': 'ds', 'priceavg': 'y'})
    std = data['y'].std() * 5
    data = data[data['y'] < std]
    m = Prophet()
    m.fit(data)
    future = m.make_future_dataframe(periods)
    forecast = m.predict(future)

    ma = pd.concat([data['y'].reset_index(drop=True), forecast[['ds', 'yhat', 'trend']]], axis=1)
    ma['7day'] = ma['trend'].rolling(7).mean()
    ma.loc[(ma['trend'] > ma['7day']), 'trend_pos'] = 1
    ma.loc[(ma['trend'] < ma['7day']), 'trend_pos'] = -1
    return forecast, ma






