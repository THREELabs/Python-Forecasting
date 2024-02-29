#collecting the latest price data from Yahoo Finance, using the yfinance API.
import pandas as pd
import yfinance as yf


import datetime
from datetime import date, timedelta
today = date.today()

d1 = today.strftime("%Y-%m-%d")
end_date = d1

#price history of last 100 days
d2 = date.today() - timedelta(days=100)
d2 = d2.strftime("%Y-%m-%d")
start_date = d2

#downloading historical data of object
data = yf.download('GM',
                      start=start_date,
                      end=end_date,
                      progress=False)
data["Date"] = data.index
data = data[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]
data.reset_index(drop=True, inplace=True)
print(data)

#cheching the shape of the data
data.shape

import plotly.graph_objects as go
figure = go.Figure(data=[go.Candlestick(x=data["Date"],
                                        open=data["Open"],
                                        high=data["High"],
                                        low=data["Low"],
                                        close=data["Close"])])
figure.update_layout(title = "btc-usd",
                     xaxis_rangeslider_visible=False)
figure.show()

correlation = data.corr()
print(correlation["Close"].sort_values(ascending=False))

#!pip install autots

#importing AutoTs for time series analysis
from autots import AutoTS

model = AutoTS(forecast_length=14, frequency='infer', ensemble='simple')
model = model.fit(data, date_col='Date', value_col='Close', id_col=None)
prediction = model.predict()
forecast = prediction.forecast
print(forecast)
