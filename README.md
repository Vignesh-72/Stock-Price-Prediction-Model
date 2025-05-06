## 📈 Project Overview
Due to rapid and unpredictable price changes, stock market prediction is a complex task.  
This project uses machine learning models to predict:
- **The next day's closing stock price** (Regression)
- **The direction of price movement (Up/Down)** (Classification)  

It aims to assist financial analysts and investors by uncovering hidden patterns using historical data and technical indicators.

---

## 🎯 Objectives
- **Simplify Stock Movement Predictions**  
Predict stock price trends using past data and technical indicators.
- **Predict Future Prices**  
Build a regression model to forecast the next day’s closing price.
- **Classification Model**  
Predict if the stock price will move up or down.
- **Interactive Frontend Dashboard**  
Allow users to input stock tickers and view real-time predictions.
- **Collaborative Development**  
Use GitHub and GitHub Actions for version control and CI/CD automation.

---

## 🛠 Features
- **Lag Values**: Previous day's closing prices (e.g., lag-1, lag-2)
- **Moving Averages**: 5-day and 20-day moving averages
- **RSI**: Relative Strength Index for momentum analysis
- **Bollinger Bands**: Volatility indicators

---

## 📌 Project Scope
- **Data Source**:  
  - Historical stock data collected using `yfinance` (Yahoo Finance).
  - Open, high, low, close prices, and volume data.
- **Limitations**:
  - Does not consider news or external factors.
  - Focused on a limited set of stocks.
  - Predictions are for short term only.
- **Constraints**:
  - Models limited to Linear Regression, Random Forest, and Logistic Regression.
  - Only public APIs used.

---

## 🧩 High-Level Methodology

![workflow](https://github.com/user-attachments/assets/302a0eac-bef0-48ce-9aa7-e298c797c52a)

1. **Data Collection**: Using `yfinance` API.
2. **Data Cleaning**: Handling missing values, removing duplicates.
3. **Exploratory Data Analysis (EDA)**:  
   Visualize trends with plots, moving averages, and heatmaps.
4. **Feature Engineering**:  
   Create lag values, moving averages, RSI, and Bollinger Bands.
5. **Model Building**:  
   - **Regression Models**: Linear Regression, Random Forest
   - **Classification Model**: Logistic Regression
6. **Model Evaluation**:
   - Regression: MAE (Mean Absolute Error)
   - Classification: Accuracy, Precision, Recall, F1-Score
7. **Deployment**:  
   An interactive **Streamlit** web app where users can input stock tickers and get predictions.

---

## ⚙️ Tools and Technologies
- **Programming Language**: Python
- **Notebook/IDE**:
  - Jupyter Notebook
  - Visual Studio Code (VS Code)
  - Axel DICE
  - Google Colab (for training models)
- **Libraries**:
  - `pandas`, `numpy` (Data processing)
  - `matplotlib`, `seaborn`, `plotly` (Visualization)
  - `scikit-learn` (Machine Learning)
- **Deployment**:
  - Streamlit (Web App)
  - GitHub (Version Control)
  - GitHub Actions (CI/CD Automation)

---

## 🚀 How to Run the Project

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Vignesh-72/Stock-Price-Prediction-Model.git
   cd Stock-Price-Prediction-Model
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit App**
   ```bash
   streamlit run app.py
   ```

4. **Usage**
   - Enter the stock ticker symbol (e.g., `AAPL`, `GOOGL`) in the Streamlit dashboard.
   - View predictions for price direction and next day's closing price.

---
