"""
Stock Price Prediction Engine

Primary Interface:
    analyze_stock(ticker: str) -> dict: Main prediction pipeline

Example Usage:
    from PredictionEngine import analyze_stock
    results = analyze_stock("AAPL")
    print(results['prediction']['price'])
"""

from .stock_predictor import analyze_stock

# Only expose the main interface function
__all__ = ['analyze_stock']

__version__ = '0.1.0'