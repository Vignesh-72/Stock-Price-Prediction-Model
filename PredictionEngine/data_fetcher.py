
import yfinance as yf
import pandas as pd
import time
import appdirs
from pathlib import Path

cache_dir = Path("./.cache")
cache_dir.mkdir(exist_ok=True)
appdirs.user_cache_dir = lambda *args: str(cache_dir)

def fetch_stock_data(ticker: str, period: str = '1y') -> pd.DataFrame:
    """
    Fetch stock data from Yahoo Finance with retry logic and cache fix.
    """
    max_retries = 3
    for attempt in range(max_retries):
        data = yf.download(ticker, period=period, auto_adjust=True)
        if not data.empty:
            return data
        time.sleep(2)  # brief pause before retry

    raise ValueError(f"No data returned for ticker '{ticker}' after {max_retries} attempts.")