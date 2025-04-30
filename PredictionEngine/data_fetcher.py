
from pathlib import Path

import appdirs as ad

CACHE_DIR = ".cache"

# Force appdirs to say that the cache dir is .cache
ad.user_cache_dir = lambda *args: CACHE_DIR

# Create the cache dir if it doesn't exist
Path(CACHE_DIR).mkdir(exist_ok=True)

import yfinance as yf

from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import time


def fetch_stock_data(ticker: str) -> pd.DataFrame:
    """
    Fetch stock data using explicit start/end dates to avoid yfinance period bug in cloud.
    """
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)  # 1 year back
    max_retries = 3

    for attempt in range(max_retries):
        df = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"), auto_adjust=True)
        if not df.empty:
            return df
        time.sleep(2)

    raise ValueError(f"No data returned for ticker '{ticker}' after {max_retries} attempts.")