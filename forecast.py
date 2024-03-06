#import libraries
import pandas as pd
import yfinance as yf

import datetime
from datetime import date, timedelta
today = date.today()

#user input
security = input("Which security? ")

#confirmation
print(f"Selected {security}")

d1 = today.strftime("%Y-%m-%d")
end_date = d1

#price history of last x amount of days
d2 = date.today() - timedelta(days=90)
d2 = d2.strftime("%Y-%m-%d")
start_date = d2

#downloading historical data of the security
data = yf.download({security},
                      start=start_date,
                      end=end_date,
                      progress=False)
data["Date"] = data.index
data = data[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]
data.reset_index(drop=True, inplace=True)
print(data)

#checking the shape of the data
data.shape

import plotly.graph_objects as go
figure = go.Figure(data=[go.Candlestick(x=data["Date"],
                                        open=data["Open"],
                                        high=data["High"],
                                        low=data["Low"],
                                        close=data["Close"])])
figure.update_layout(title = "Price Action Overview",
                     xaxis_rangeslider_visible=False)
figure.show()

correlation = data.corr(numeric_only=True)
print(correlation["Close"].sort_values(ascending=False))

#import AutoTs for time series analysis. !pip install autots if on Colab
from autots import AutoTS

model = AutoTS(forecast_length=14, frequency='infer', ensemble='simple')
model = model.fit(data, date_col='Date', value_col='Close', id_col=None)
prediction = model.predict()
forecast = prediction.forecast
print(forecast)
print("Are the results for:", security)