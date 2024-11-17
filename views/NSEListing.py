import streamlit as st, pandas as pd, numpy as np, yfinance as yf

import streamlit as st, pandas as pd
import requests
from bs4 import BeautifulSoup



def fetch_ind_stock_data(ticker, exchange):
    url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    ticker_heading_class ="zzDege"
    price_class = "YMlKec fxKbKc"
    previous_close_class = "P6K39c"
    revenue_class ="QXDnM"
    recent_news_class ='Yfwt5'
    about_company_class = 'bLLb2d'
    market_cap_class ="P6K39c"

    yoy_revenue_change_class ="JwB6zf Ez2Ioe CnzlGc"
    ope_exp_class ="slpEwd"

    price = float(soup.find(class_=price_class).text.strip()[1:].replace(",", ""))
    previous_close_price = float(soup.find(class_=previous_close_class).text.strip()[1:].replace(",", ""))
    revenue_data = soup.find(class_=revenue_class).text
    recent_news = soup.find(class_=recent_news_class).text
    about_company = soup.find(class_=about_company_class).text
    market_cap = soup.find(class_=market_cap_class).text


    company_name = soup.find(class_=ticker_heading_class).text
    yoy_revenue_change = soup.find(class_=yoy_revenue_change_class).text



    ope_expense_table = soup.find('table', attrs={'class':ope_exp_class})

    data = []
    for row in ope_expense_table.find_all('tr'):
        row_data = []
        for cell in row.find_all('td'):
            row_data.append(cell.text)
        data.append(row_data)
    df = pd.DataFrame(data)
    df.columns= ["About", "Value","Change"]





    return price, previous_close_price, revenue_data, recent_news, about_company, market_cap, yoy_revenue_change, df, company_name

st.title("Indian Stock Data")
ind_ticker = st.sidebar.text_input("Indian Ticker", value="INFY").upper()
# ind_exchange = st.sidebar.text_input("Indian Exchange", value="NSE").upper()

try:
    price, previous_close_price, revenue_data, recent_news, about_company, market_cap, yoy_revenue_change, df, company_name = fetch_ind_stock_data(ind_ticker, 'NSE')
    st.subheader(company_name)

    st.write("Current Price : ", price)
    st.write("Previous Day Close :", previous_close_price)
    st.write("Revenue :", revenue_data)
    st.write("Market Cap : ", market_cap)
    st.write("Recent News :", recent_news)
    st.write("About Company : ", about_company)
    st.write("YOY Revenue Change : ", yoy_revenue_change)


    st.write("Figures : ", df[1:])
except Exception:
    st.write("Only Indian Stockes listed in NSE allowed! Enter a correct ticker")