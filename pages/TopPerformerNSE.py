import streamlit as st, pandas as pd, numpy as np, yfinance as yf

import streamlit as st, pandas as pd
import requests
from bs4 import BeautifulSoup
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

url = "https://ticker.finology.in/market/index/nse/nifty"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
table = soup.find(class_='tab-content').text
st.write(table)

