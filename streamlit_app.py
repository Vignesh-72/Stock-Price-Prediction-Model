# app.py
import streamlit as st
from PredictionEngine import analyze_stock
from frontend.visualization import render_stock_visualizations

def main():
    # Add this at the very beginning of your code, before any other content
    st.markdown("""
    <style>
    .centered-title {
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
        color: #4FC3F7;
        margin-bottom: 0.5em;
    }
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: pointer;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 250px;
        background-color: rgba(0, 0, 0, 0.8);
        color: white;
        text-align: center;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -125px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 14px;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="centered-title">Stock Prediction Dashboard</h1>', unsafe_allow_html=True)
    
    # Create columns to align the input and tooltip icon
    col1, col2 = st.columns([10, 1])
    
    with col1:
        ticker = st.text_input("Enter stock ticker:", "GOOGL")
    
    with col2:
        st.markdown("""
        <div class="tooltip" style="margin-top: 28px;">ℹ️
            <span class="tooltiptext">
                <b>Enter a Stock Ticker</b><br><br>
                Examples:<br>
                     Here Are Some Stock Ticker Examples<br>
                • US: AAPL, MSFT<br>
                • India: TCS.NS, RELIANCE.NS<br>
                • Crypto: BTC-USD, ETH-USD<br><br>
                For more tickers, visit:<br>
                <a href="https://finance.yahoo.com" target="_blank">Yahoo Finance</a>
            </span>
        </div>

        """, unsafe_allow_html=True)
    
    if st.button("Analyze"):
        try:
            results = analyze_stock(ticker)
            # Debug: Print the results structure
            # st.write("Raw results data:", results)
            
            # Ensure required keys exist
            required_keys = ['historical_data', 'prediction', 'evaluation']
            if all(key in results for key in required_keys):
                render_stock_visualizations(results)
            else:
                st.error("Invalid data structure received from prediction engine")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()