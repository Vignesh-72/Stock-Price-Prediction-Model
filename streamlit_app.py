# app.py
import streamlit as st
from PredictionEngine import analyze_stock
from frontend.visualization import render_stock_visualizations

def main():
    st.title("Stock Prediction Dashboard")
    
    ticker = st.text_input("Enter stock ticker:", "GOOGL")
    
    if st.button("Analyze"):
        try:
            results = analyze_stock(ticker)
            # Debug: Print the results structure
            st.write("Raw results data:", results)
            
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
