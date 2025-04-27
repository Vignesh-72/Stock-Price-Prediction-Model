import pandas as pd

def add_technical_features(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add technical indicators to stock data
    Args:
        data: Raw stock data DataFrame
    Returns:
        pd.DataFrame: Data with engineered features
    """
    # Lag features
    data['Lag_1'] = data['Close'].shift(1)
    data['Lag_2'] = data['Close'].shift(2)
    
    # Moving averages
    data['MA_5'] = data['Close'].rolling(window=5).mean()
    data['MA_20'] = data['Close'].rolling(window=20).mean()
    
    # RSI calculation
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # Targets
    data['Target_Price'] = data['Close'].shift(-1)
    data['Target_UpDown'] = (data['Close'].shift(-1) > data['Close']).astype(int)
    
    return data.dropna()