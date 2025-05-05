from pathlib import Path
from datetime import datetime, timedelta
import time
import pandas as pd
import yfinance as yf
import appdirs as ad
import os

#External dependencies for smarter requests
import requests_cache
from requests_ratelimiter import LimiterSession
from pyrate_limiter import Duration, RequestRate, Limiter

#Set Streamlit-safe cache directory
CACHE_DIR = "/tmp/yf-cache"
ad.user_cache_dir = lambda *args: CACHE_DIR
Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)

#Set up request caching + rate limiting
# Cache expires after 5 minutes
cached_session = requests_cache.CachedSession(
    cache_name=os.path.join(CACHE_DIR, "yfinance.cache"),
    backend="sqlite",
    expire_after=300  # seconds
)
cached_session.headers["User-agent"] = "Mozilla/5.0 (yfinance-app)"

# Limit: max 2 requests every 5 seconds
limiter = Limiter(RequestRate(2, Duration.SECOND * 5))
session = LimiterSession(limiter=limiter)
session._session = cached_session  # Combine limiter and cache

#Function to fetch stock data using yf.download
def fetch_stock_data(ticker: str) -> pd.DataFrame:
    """
    Fetches 1 year of historical stock data for the given ticker using yfinance.download().
    Implements caching, retries, and rate limiting.
    """
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)
    max_retries = 3

    for attempt in range(max_retries):
        try:
            df = yf.download(
                ticker,
                start=start_date.strftime("%Y-%m-%d"),
                end=end_date.strftime("%Y-%m-%d"),
                auto_adjust=True,
                progress=False,
                session=session  # 💡 Use the smarter session
            )
            if not df.empty:
                return df
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {ticker}: {e}")
        time.sleep(2)  # Wait before retrying

    raise ValueError(f"No data returned for ticker '{ticker}' after {max_retries} attempts.")


'''
from pathlib import Path
from datetime import datetime, timedelta
import time
import pandas as pd
import yfinance as yf
import appdirs as ad
import os

# Use Streamlit-compatible cache directory
CACHE_DIR = "/tmp/yf-cache"
ad.user_cache_dir = lambda *args: CACHE_DIR
Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)

#  Optional: disable yfinance caching (uncomment if you want to force fresh fetches)
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

    raise ValueError(f"No data returned for ticker '{ticker}' after {max_retries} attempts.")'''
