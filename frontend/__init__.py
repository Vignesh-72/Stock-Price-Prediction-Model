
from .visualization import render_stock_visualizations

__all__ = ['render_stock_visualizations']
__version__ = '1.0.0'

# Initialize Streamlit config when module is imported
import streamlit as st
st.set_page_config(
    page_title="Stock Prediction Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)