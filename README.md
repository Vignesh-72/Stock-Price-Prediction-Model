# Stock-Price-Prediction-Model

![Stock Prediction Visualization](https://img.shields.io/badge/Python-3.8%2B-blue) ![Framework](https://img.shields.io/badge/Framework-Streamlit-red)

A machine learning application that predicts next-day stock prices and movement direction using technical indicators.

## Key Features
- 📈 Predicts next day's closing price (Regression)
- 🔮 Forecasts price movement direction (Up/Down Classification)
- 📊 Interactive visualizations of trends and predictions
- 🎛️ Customizable technical indicators (RSI, Moving Averages)
- 🚀 Real-time predictions using Yahoo Finance data

## How It Works
1. **Data Collection**: Fetches stock data using `yfinance` API
2. **Feature Engineering**: Calculates technical indicators:
   - Lag features (previous day prices)
   - Moving Averages (5-day, 20-day)
   - Relative Strength Index (RSI)
3. **Machine Learning**:
   - Regression: Random Forest for price prediction
   - Classification: Logistic Regression for direction prediction
4. **Visualization**: Streamlit dashboard displays:
   - Actual vs Predicted prices
   - Buy/Sell signals
   - Accuracy metrics

