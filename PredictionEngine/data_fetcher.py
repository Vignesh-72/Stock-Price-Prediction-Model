import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker: str, period: str = '1y') -> pd.DataFrame:
    """
    Fetch stock data from Yahoo Finance
    """
    data = yf.download(ticker, period=period, auto_adjust=True)
    
    if data.empty:
        raise ValueError(f"No data returned for ticker '{ticker}'. Check the symbol or try again later.")

    return data
