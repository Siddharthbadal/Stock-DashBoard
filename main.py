from datetime import date, timedelta

import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px


yesterday = date.today() - timedelta(30)
today = date.today()

# title
st.title("Stock DashBoard")

#  sidebar
ticker = st.sidebar.text_input("Ticker", value="MSFT").upper()
start_date = st.sidebar.date_input("Start date", value=yesterday)
end_date = st.sidebar.date_input("End date", value=today)

data = yf.download(ticker, start=start_date, end=end_date)
data_for_chart = data['Adj Close']

fig = px.line(data_for_chart, x=data.index,
              y= data_for_chart[ticker], title= ticker.upper())
st.plotly_chart(fig)

pricing_data, fundamental_data, news_data = st.tabs([ "Pricing", "Fundamentals", "News"])


with pricing_data:
    st.write("Daily Changes")
    data_with_changes = data
    data_with_changes["% Change"] = data["Adj Close"] / data["Adj Close"].shift(1) - 1
    data_with_changes.dropna(inplace=True)
    st.write(data_with_changes)

    annual_return = round(data_with_changes["% Change"].mean()*252*100, 2)
    st.write("Annual Returns (%): ", annual_return)

    stddev = round(np.std(data_with_changes['% Change']) * np.sqrt(252), 4)
    st.write("Standard Deviation: ", stddev, " *Standard deviation measures the dispersion of a dataset relative to its mean.")

    st.write("Risk Adjusted Return: ", round(annual_return / ( stddev * 100 ), 2))

with fundamental_data:
    st.write("Fundamentals")

with news_data:
    st.write("news")










