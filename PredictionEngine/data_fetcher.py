import yfinance as yf
import pandas as pd
import time

def fetch_stock_data(ticker: str, period: str = '1y') -> pd.DataFrame:
    max_retries = 3
    for attempt in range(max_retries):
        data = yf.download(ticker, period=period, auto_adjust=True)
        if not data.empty:
            return data
        time.sleep(2)
    raise ValueError(f"No data returned for ticker '{ticker}' after {max_retries} attempts.")