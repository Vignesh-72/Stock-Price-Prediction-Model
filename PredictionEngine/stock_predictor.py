from .data_fetcher import fetch_stock_data
from .feature_engineer import add_technical_features
from .model_predictor import StockPredictor
import pandas as pd

def analyze_stock(ticker: str) -> dict:
    """
    Main function to run full analysis pipeline
    Args:
        ticker: Stock symbol to analyze
    Returns:
        dict: Contains all prediction results and evaluation metrics
    """
    # Data pipeline
    raw_data = fetch_stock_data(ticker)
    processed_data = add_technical_features(raw_data)
    
    # Model pipeline
    predictor = StockPredictor()
    X_train, X_test, y_train_reg, y_test_reg, y_train_clf, y_test_clf = \
        predictor.prepare_data(processed_data)
    
    predictor.train_models(X_train, y_train_reg, y_train_clf)
    
    # Get latest data point for tomorrow's prediction
    latest_features = processed_data[predictor.features].iloc[[-1]]
    
    return {
        'ticker': ticker,
        'historical_data': processed_data,
        'prediction': predictor.predict(latest_features),
        'evaluation': {
            **predictor.evaluate(X_test, y_test_reg, y_test_clf),
            'regression': {
                'actual': y_test_reg.values,
                'predicted': predictor.reg_model.predict(X_test)
            }
        },
        'dates': {
            'train_dates': X_train.index,
            'test_dates': X_test.index
        },
        'y_test_reg': y_test_reg,
        'reg_preds ': predictor.reg_model.predict(X_test)
    }
