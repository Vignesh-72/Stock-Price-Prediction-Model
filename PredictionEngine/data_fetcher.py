from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import time
import appdirs as ad

# Fix yfinance cache path
ad.user_cache_dir = lambda *args: "/tmp"

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