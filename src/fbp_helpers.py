from fbprophet import Prophet
from fbprophet.diagnostics import performance_metrics, cross_validation
import sqlalchemy as sa
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.special import inv_boxcox
import pickle

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
        self.item_list = None
        self.positive_trend = []
        self.negative_trend = []
        self.profit = pd.DataFrame()

    def sql_call(self):
        self.df = pd.read_sql(self.query, self.engine)
        self.df = self.df.sort_values(by='when')

    def prophet_fit(self, periods=31):
        mask = self.df['name_enus'] == self.item
        self.data = self.df[mask][['when', 'priceavg']].rename(columns={'when': 'ds', 'priceavg': 'y'})
        self.data['ds'] = pd.to_datetime(self.data['ds'])
        # remove outliers
        std = self.data['y'].std() * 1.5
        mean = self.data['y'].mean()
        self.data = self.data[(self.data['y'] < mean + std) & (self.data['y'] > mean - std)]
        # box-cox transformation
        # yt, self.lmbda = stats.boxcox(self.data['y'])
        # self.data['y'] = yt
        # fit
        self.m = Prophet(n_changepoints=20)
        self.m.add_seasonality(period=30.4, fourier_order=5, name='monthly')
        self.m.fit(self.data)
        future = self.m.make_future_dataframe(periods)
        self.forecast = self.m.predict(future)
        # create moving average colunmn
        # self.forecast['yhat'] = inv_boxcox(self.forecast['yhat'], self.lmbda)
        # self.data['y'] = inv_boxcox(self.data['y'], self.lmbda)
        self.ma = pd.concat([self.data['y'].reset_index(drop=True), self.forecast[['ds', 'yhat', 'trend']]], axis=1)
        self.ma['7day'] = self.ma['trend'].rolling(7).mean()
        self.ma.loc[(self.ma['trend'] > self.ma['7day']), 'trend_pos'] = 1
        self.ma.loc[(self.ma['trend'] < self.ma['7day']), 'trend_pos'] = -1



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

    def make_lists(self, buy_date):
        self.sql_call()
        self.item_list = self.df.groupby('name_enus').mean().sort_values('quantityavg')[::-1]
        for item in self.item_list.index:
            self.item = item
            if self.profit.shape[1] < 10:
                self.prophet_fit()
                if self.ma['trend_pos'].iloc[-31:-39:-1].sum() > 1:
                    buy = self.data[self.data['ds'] == buy_date]['y'].values[0]
                    profit_temp = self.forecast[self.forecast['ds'] > buy_date][['ds', 'yhat']].reset_index(drop=True)
                    profit_temp['buy'] = buy
                    profit_temp[item] = profit_temp['yhat'] - profit_temp['buy']
                    self.profit = pd.concat([self.profit, profit_temp[item]], axis=1)
                elif self.ma['trend_pos'].iloc[-31:-39:-1].sum() < -1:
                    self.negative_trend.append(self.item)
            else:
                pickle.dump(self.profit,open('../data/profit_df.pkl','wb'))
                break



    def cross_val(self):
        df_cv = cross_validation(self.m, initial='62 days', period='1 days',horizon='7 days')
        # for col in ['yhat', 'yhat_lower', 'yhat_upper', 'y']:
        #     df_cv[col] = inv_boxcox(df_cv[col], lmbda)
        print(df_cv.sort_values('ds').tail())
        df_p = performance_metrics(df_cv)
        print(df_p)