from datetime import datetime, timedelta
import time
import pandas as pd
import os
import yfinance as yf

import appdirs
appdirs.user_cache_dir = lambda *args: "/tmp"

def fetch_stock_data(ticker: str) -> pd.DataFrame:
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)
    max_retries = 3

    for attempt in range(max_retries):
        df = yf.download(
            ticker,
            start=start_date.strftime("%Y-%m-%d"),
            end=end_date.strftime("%Y-%m-%d"),
            auto_adjust=True,
            progress=False
        )
        if not df.empty:
            return df
        time.sleep(2)

    raise ValueError(f"No data returned for ticker '{ticker}' after {max_retries} attempts.")