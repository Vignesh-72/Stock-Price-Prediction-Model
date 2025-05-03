from pathlib import Path
from datetime import datetime, timedelta
import time
import pandas as pd
import yfinance as yf
import appdirs as ad
import os

# ✅ Use Streamlit-compatible cache directory
CACHE_DIR = "/tmp/yf-cache"
ad.user_cache_dir = lambda *args: CACHE_DIR
Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)

# ✅ Optional: disable yfinance caching (uncomment if you want to force fresh fetches)
# os.environ["YFINANCE_NO_CACHE"] = "1"

def fetch_stock_data(ticker: str) -> pd.DataFrame:
    """
    Fetches 1 year of historical stock data for the given ticker using yfinance.
    Implements retries and uses explicit start/end dates to avoid yfinance issues.
    """
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
        time.sleep(2)  # Wait before retrying

    raise ValueError(f"No data returned for ticker '{ticker}' after {max_retries} attempts.")