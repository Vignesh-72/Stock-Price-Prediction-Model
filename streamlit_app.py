import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

import appdirs as ad
ad.user_cache_dir = lambda *args: "/tmp"

import yfinance as yf

# Function to fetch stock data
def get_stock_data(stock_symbol, start_date, end_date):
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    return stock_data['Close']  

# Function to calculate simple moving averages (SMAs)
def calculate_sma(stock_data, short_window=20, long_window=200):
    short_sma = stock_data.rolling(window=short_window).mean()
    long_sma = stock_data.rolling(window=long_window).mean()
    return short_sma, long_sma

# Function to create an interactive graph with SMAs
def create_stock_graph(stock_data, short_sma, long_sma, title):
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True, subplot_titles=[title])

    #Add Range Slider and Selectors
    fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=False
        ),
        type="date"
    ))

    trace_stock = go.Scatter(x=stock_data.index, y=stock_data.values, mode='lines', name=title)
    trace_short_sma = go.Scatter(x=short_sma.index, y=short_sma.values, mode='lines', name='20-day SMA', line=dict(color="#20fc03"))
    trace_long_sma = go.Scatter(x=long_sma.index, y=long_sma.values, mode='lines', name='200-day SMA', line=dict(color="#fc0303"))

    fig.add_trace(trace_stock, row=1, col=1)
    fig.add_trace(trace_short_sma, row=1, col=1)
    fig.add_trace(trace_long_sma, row=1, col=1)
    
    fig.update_layout(title_text=title)
    fig.update_xaxes(title_text='Date', row=1, col=1)
    fig.update_yaxes(title_text='Price', row=1, col=1)

    return fig

# Main Streamlit app
def main():
    st.title("Stocks Dashboard")

    # List of stock symbols
    stock_symbols = ["AAPL", "GOOG", "MSFT", "AMZN", "TSLA", "NVDA", "META", "CRM", "JPM", "XOM"]

    # Date range for stock data (default to present date)
    end_date = pd.to_datetime("today")
    start_date = end_date - pd.DateOffset(years=3)  # 3 years ago
    
    #Display Most Recent Date
    st.text('Last Update Date: ' + str(end_date))
    
    # Fetch and display graphs for each stock
    for symbol in stock_symbols:
        st.subheader(f"Stock: {symbol}")
        stock_data = get_stock_data(symbol, start_date, end_date)
        
        # Calculate Simple Moving Averages (SMAs)
        short_sma, long_sma = calculate_sma(stock_data)
        
        # Display only the last year of data
        stock_data_last_year = stock_data.tail(504)  # Assuming 252 trading days in a year
        short_sma_last_year, long_sma_last_year = short_sma.tail(504), long_sma.tail(504)
        
        st.plotly_chart(create_stock_graph(stock_data_last_year, short_sma_last_year, long_sma_last_year, title=symbol))

if __name__ == "__main__":
    main()
