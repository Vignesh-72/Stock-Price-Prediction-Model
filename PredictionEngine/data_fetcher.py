from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time

# ✅ Set your Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = "your_api_key_here"

# ✅ Create global client once
ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas', indexing_type='date')

def fetch_stock_data(ticker: str) -> pd.DataFrame:
    """
    Fetches 1 year of historical daily stock data using Alpha Vantage.
    Falls back with retry logic.
    """
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            print(f"📈 Fetching data for {ticker}, attempt {attempt}")
            data, meta = ts.get_daily_adjusted(symbol=ticker, outputsize='full')
            if data is not None and not data.empty:
                # Filter last 1 year
                data = data.sort_index()
                data.index = pd.to_datetime(data.index)
                one_year_ago = pd.Timestamp.today() - pd.Timedelta(days=365)
                df = data[data.index >= one_year_ago]
                df = df.rename(columns={
                    '1. open': 'Open',
                    '2. high': 'High',
                    '3. low': 'Low',
                    '4. close': 'Close',
                    '5. adjusted close': 'Adj Close',
                    '6. volume': 'Volume'
                })
                return df
            else:
                print(f"⚠️ Empty data received for {ticker}, retrying...")
        except Exception as e:
            print(f"❌ Error fetching data for {ticker}: {e}")
        time.sleep(2)
    raise ValueError(f"❌ No data returned for ticker '{ticker}' after {max_retries} attempts.")


'''from pathlib import Path
from datetime import datetime, timedelta
import time
import pandas as pd
import yfinance as yf
import appdirs as ad
import os

# External modules for smarter HTTP handling
import requests_cache
from requests_ratelimiter import LimiterSession
from pyrate_limiter import Duration, RequestRate, Limiter

# ✅ Streamlit-safe cache directory
CACHE_DIR = "/tmp/yf-cache"
Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)
ad.user_cache_dir = lambda *args: CACHE_DIR  # Override yfinance internal cache path

# ✅ Setup requests cache (expires every 5 minutes)
cached_session = requests_cache.CachedSession(
    cache_name=os.path.join(CACHE_DIR, "yfinance_cache"),
    backend="sqlite",
    expire_after=300  # seconds
)
cached_session.headers.update({
    "User-Agent": "Mozilla/5.0 (stock-app)"
})

# ✅ Setup rate limiter (2 requests per 5 seconds)
rate_limiter = Limiter(RequestRate(2, Duration.SECOND * 5))
session = LimiterSession(limiter=rate_limiter)
session._session = cached_session  # Combine limiter + cache

# ✅ Main fetch function
def fetch_stock_data(ticker: str) -> pd.DataFrame:
    """
    Fetches 1 year of historical stock data for a given ticker using yfinance.Ticker.
    Includes caching, rate limiting, retries, and Streamlit-safe cache directory.
    """
    max_retries = 3

    for attempt in range(1, max_retries + 1):
        try:
            print(f"📈 Attempt {attempt} to fetch '{ticker}'")
            stock = yf.Ticker(ticker, session=session)
            df = stock.history(period="1y", auto_adjust=True)

            if df is not None and not df.empty:
                return df
            else:
                print(f"⚠️ Empty data received for '{ticker}', retrying...")
        except Exception as e:
            print(f"❌ Error fetching data for '{ticker}': {e}")
        time.sleep(2)

    raise ValueError(f"❌ No data returned for ticker '{ticker}' after {max_retries} attempts.")
'''
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
