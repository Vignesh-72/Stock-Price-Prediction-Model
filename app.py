# app.py
import streamlit as st
from PredictionEngine import analyze_stock
from frontend.visualization import render_stock_visualizations

ticker = st.text_input("Enter stock ticker:", "GOOGL")
if st.button("Analyze"):
    results = analyze_stock(ticker)
    render_stock_visualizations(results)