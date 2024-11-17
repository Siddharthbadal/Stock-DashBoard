import requests
from bs4 import BeautifulSoup
import streamlit as st, pandas as pd, numpy as np, yfinance as yf

st.title("Stock in INR")

def get_currency_rate(currency):
    if currency == "GBX":
        currency = 'GBP'
        url = f"https://www.google.com/finance/quote/{currency}-INR"
    else:
        url = f"https://www.google.com/finance/quote/{currency}-INR"
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    inr_div = soup.find("div", attrs={'data-last-price':True})
    inr_rate = float(inr_div['data-last-price'])
    return inr_rate



def get_stock_price(ticker, exchange):
    url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    price_div = soup.find("div", attrs={'data-last-price':True})
    price = float(price_div['data-last-price'])
    currency = price_div['data-currency-code']
    
    inr_price = price
    if currency != 'INR':
        rate = get_currency_rate(currency)
        inr_price = round(price * rate, 2)


    result= {
        'Ticker': ticker,
        'Exchange': exchange,
        'Price_USD': price,
        'Currency': currency,
        'Price_INR': inr_price
    }

    # df = pd.DataFrame(result.items(), columns=['Date', 'Exchange', 'Price_USD', 'Currency', 'Price_INR'])
    # df = pd.DataFrame.from_dict(result, orient="index").reset_index()
    df = pd.DataFrame(result, index=['Details',])
    return df

ticker = st.sidebar.text_input("Ticker", value="MSFT").upper()
exchange = st.sidebar.text_input("Exchange", value="NASDAQ").upper()

try:
    st.write(get_stock_price(ticker, exchange))
    
except Exception:
    st.warning(f"{ticker} is not listed in {exchange}")
    st.write("""
                    Example -
                        AAPL : NASDAQ |
                        SHOP, TSE  |
                        BP, LON |
             """)

