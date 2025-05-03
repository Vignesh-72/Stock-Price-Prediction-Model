import yfinance as yf
from datetime import datetime, timedelta

# Fetch Google stock data (1 year history)
ticker = "GOOG"
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

try:
    print(f"Downloading {ticker} stock data...")
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    
    if not data.empty:
        # Save to CSV
        filename = f"{ticker}_stock_data.csv"
        data.to_csv(filename)
        print(f"Success! Data saved to {filename}")
    else:
        print("No data received from Yahoo Finance")
        
except Exception as e:
    print(f"Error occurred: {e}")