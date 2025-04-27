import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker: str, period: str = '1y') -> pd.DataFrame:
    """
    Fetch stock data from Yahoo Finance
    Args:
        ticker: Stock symbol (e.g., 'GOOGL')
        period: Time period to fetch (default: '1y')
    Returns:
        pd.DataFrame: Raw stock data
    """
    data = yf.download(ticker, period=period, auto_adjust=True)
    return data