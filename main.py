from datetime import date, timedelta
from alpha_vantage.fundamentaldata import FundamentalData
from stocknews import StockNews
import streamlit as st, pandas as pd, numpy as np, yfinance as yf

import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

yesterday = date.today() - timedelta(30)
today = date.today()


st.set_page_config(
    page_title="Stock Dashboard",
    page_icon="🎯"
)


# title
st.title("Stock Dashboard")

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
    api_key= os.getenv("API_KEY")
    fdata = FundamentalData(api_key, output_format= 'pandas')
    st.subheader("Balance Sheet")
    try:
        balance_sheet = fdata.get_balance_sheet_annual(ticker)[0]
        bsheet = balance_sheet.T[2:]
        bsheet.columns = list(balance_sheet.T.iloc[0])
        st.write(bsheet)
        st.subheader("Income Statement")
        income_statement = fdata.get_income_statement_annual(ticker)[0]
        istat = income_statement.T[2:]
        istat.columns = list(income_statement.T.iloc[0])
        st.write(istat)
        st.subheader("Cash Flow")
        cash_flow_statement = fdata.get_cash_flow_annual(ticker)[0]
        cash_flow = cash_flow_statement.T[2:]
        cash_flow.columns = list(cash_flow_statement.T.iloc[0])
        st.write(cash_flow)
    except Exception:
        st.markdown("### Incorrect Ticker or API limit reached. Try Again.")



with news_data:
    try:
        st.header(f"{ticker} in News")
        snews = StockNews(ticker, save_news=False)
        print(snews)
        df_news = snews.read_rss()
        for n in range(5):
            st.subheader(f"News {n+1}")
            st.write(f"Published at : {df_news['published'][n]}")
            st.markdown("#### News title")
            st.write(df_news['title'][n])
            st.markdown("##### News Details")
            st.write(df_news['summary'][n])
    except Exception:
        st.markdown("### Incorrect Ticker or API limit reached. Try Again.")









