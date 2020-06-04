from fbprophet import Prophet
from fbprophet.diagnostics import performance_metrics, cross_validation
import sqlalchemy as sa
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.special import inv_boxcox

class ProphetProfit:

    def __init__(self, engine, query, item):
        self.engine = engine
        self.query = query
        self.item = item
        self.df = None
        self.data = None
        self.m = None
        self.lmbda = None
        self.forecast = None
        self.ma = None

    def sql_call(self):
        self.df = pd.read_sql(self.query, self.engine)
        self.df = self.df.sort_values(by='when')

    def item_list(self, df):
        temp = df.groupby('name_enus').sum().sort_values('quantityavg')[::-1]
        return temp.index

    def prophet_fit(self, periods=31):
        mask = self.df['name_enus'] == self.item
        self.data = self.df[mask][['when', 'priceavg']].rename(columns={'when': 'ds', 'priceavg': 'y'})
        self.data['ds'] = pd.to_datetime(self.data['ds'])
        # remove outliers
        std = self.data['y'].std() * 1.5
        mean = self.data['y'].mean()
        self.data = self.data[(self.data['y'] < mean + std) & (self.data['y'] > mean - std)]
        # box-cox transformation
        yt, self.lmbda = stats.boxcox(self.data.y)
        self.data['y'] = yt
        # fit
        self.m = Prophet(n_changepoints=20)
        self.m.add_seasonality(period=30.4, fourier_order=5, name='monthly')
        self.m.fit(self.data)
        future = self.m.make_future_dataframe(periods)
        self.forecast = self.m.predict(future)
        # create moving average colunmn
        # self.forecast['yhat'] = inv_boxcox(self.forecast['yhat'], self.lmbda)
        self.ma = pd.concat([self.data['y'].reset_index(drop=True), self.forecast[['ds', 'yhat', 'trend']]], axis=1)
        self.ma['7day'] = self.ma['trend'].rolling(7).mean()
        self.ma.loc[(self.ma['trend'] > self.ma['7day']), 'trend_pos'] = 1
        self.ma.loc[(self.ma['trend'] < self.ma['7day']), 'trend_pos'] = -1
        # self.data['y'] = inv_boxcox(self.data['y'], self.lmbda)


    def plot(self):
        self.sql_call()
        self.prophet_fit()
        fig1 = self.m.plot(self.forecast)
        fig2 = self.m.plot_components(self.forecast)
        plt.show()

    def make_profit(self, buy_date):
        self.sql_call()
        self.prophet_fit()
        buy = self.data[self.data['ds']==buy_date]['y'].values[0]
        profit = self.forecast[self.forecast['ds'] > buy_date][['ds','yhat']].reset_index(drop=True)
        profit['buy'] = buy
        profit['profit'] = profit['yhat'] - profit['buy']
        max = profit['profit'].max()
        print(profit[profit['profit'] == max])











    def make_lists(self, ma, item, positive_trend, negative_trend):
        if ma['trend_pos'].iloc[-31:-39:-1].sum() > 1:
            positive_trend.append(item)
        elif ma['trend_pos'].iloc[-31:-39:-1].sum() < -1:
            negative_trend.append(item)
        else:
            print(f'error with {item}')
        return positive_trend, negative_trend


    def cross_val(self):
        df_cv = cross_validation(self.m, initial='62 days', period='1 days',horizon='7 days')
        # for col in ['yhat', 'yhat_lower', 'yhat_upper', 'y']:
        #     df_cv[col] = inv_boxcox(df_cv[col], lmbda)
        print(df_cv.sort_values('ds').tail())
        df_p = performance_metrics(df_cv)
        print(df_p)