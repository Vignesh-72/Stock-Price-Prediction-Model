from pathlib import Path
from datetime import datetime, timedelta
import time
import pandas as pd
import yfinance as yf
import os
import streamlit as st

def is_running_in_streamlit():
    """Check if the code is running in Streamlit"""
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        return get_script_run_ctx() is not None
    except:
        return False

def fetch_stock_data(ticker: str) -> pd.DataFrame:
    """
    Fetches 1 year of historical stock data for the given ticker.
    Uses yfinance Ticker when run locally, CSV when run in Streamlit.
    """
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)
    max_retries = 3

    if is_running_in_streamlit():
        # Streamlit mode - try to load from CSV first
        csv_file = f"{ticker}_stock_data.csv"
        if os.path.exists(csv_file):
            try:
                df = pd.read_csv(csv_file, index_col=0, parse_dates=True)
                if not df.empty:
                    return df
            except Exception as e:
                st.warning(f"Error reading CSV file: {e}")

    # Either not in Streamlit or CSV load failed - fetch fresh data
    for attempt in range(max_retries):
        try:
            if is_running_in_streamlit():
                # In Streamlit, use download for better reliability
                df = yf.download(
                    ticker,
                    start=start_date,
                    end=end_date,
                    auto_adjust=True,
                    progress=False
                )
            else:
                # Local execution - use Ticker interface
                stock = yf.Ticker(ticker)
                df = stock.history(
                    start=start_date,
                    end=end_date,
                    auto_adjust=True
                )

            if not df.empty:
                if not is_running_in_streamlit():
                    # Save to CSV when running locally
                    csv_file = f"{ticker}_stock_data.csv"
                    df.to_csv(csv_file)
                    print(f"Success! Data saved to {csv_file}")
                return df

        except Exception as e:
            error_msg = f"Attempt {attempt + 1} failed: {str(e)}"
            if is_running_in_streamlit():
                st.warning(error_msg)
            else:
                print(error_msg)
        
        time.sleep(2)  # Wait before retrying

    raise ValueError(f"No data returned for ticker '{ticker}' after {max_retries} attempts")

# Example usage
if __name__ == "__main__":
    # When run locally
    try:
        google_data = fetch_stock_data("GOOG")
        print("Data fetched successfully:")
        print(google_data.head())
    except Exception as e:
        print(f"Error: {e}")

if is_running_in_streamlit():
    # When run in Streamlit
    st.title("Stock Data Fetcher")
    ticker = st.text_input("Enter stock ticker", "GOOG")
    
    if st.button("Fetch Data"):
        try:
            data = fetch_stock_data(ticker)
            st.success(f"Successfully fetched {len(data)} records")
            st.dataframe(data.head())
            
            # Provide download button
            csv = data.to_csv().encode('utf-8')
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name=f"{ticker}_stock_data.csv",
                mime='text/csv',
            )
        except Exception as e:
            st.error(f"Error fetching data: {e}")