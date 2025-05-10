from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, accuracy_score
import pandas as pd

class StockPredictor:
    def __init__(self):
        self.reg_model = RandomForestRegressor(random_state=42)
        self.clf_model = LogisticRegression(max_iter=1000, random_state=42)
        self.features = ['Lag_1', 'Lag_2', 'MA_5', 'MA_20', 'RSI']
    
    def prepare_data(self, data: pd.DataFrame) -> tuple:
        """Split data into features and targets"""
        X = data[self.features]
        y_reg = data['Target_Price']
        y_clf = data['Target_UpDown']
        
        # Split without shuffling to preserve time order
        X_train, X_test, y_train_reg, y_test_reg = train_test_split(
            X, y_reg, test_size=0.2, shuffle=False)
        _, _, y_train_clf, y_test_clf = train_test_split(
            X, y_clf, test_size=0.2, shuffle=False)
            
        return X_train, X_test, y_train_reg, y_test_reg, y_train_clf, y_test_clf
    
    def train_models(self, X_train, y_train_reg, y_train_clf):
        """Train both regression and classification models"""
        self.reg_model.fit(X_train, y_train_reg)
        self.clf_model.fit(X_train, y_train_clf)
    
    def predict(self, X) -> dict:
        """Make predictions for latest data"""
        price_pred = self.reg_model.predict(X)[0]
        direction_pred = self.clf_model.predict(X)[0]
        return {
            'price': price_pred,
            'direction': 'UP' if direction_pred == 1 else 'DOWN',
            'last_close': X['Lag_1'].iloc[0]  # Previous close price
        }
    
    def evaluate(self, X_test, y_test_reg, y_test_clf) -> dict:

        reg_preds = self.reg_model.predict(X_test)
        clf_preds = self.clf_model.predict(X_test)
        clf_proba = self.clf_model.predict_proba(X_test)[:, 1]  # Probability for class 1 (UP)
    
        return {
            'regression': {
                'mae': mean_absolute_error(y_test_reg, reg_preds),
                'actual': y_test_reg,
                'predicted': reg_preds
            },
            'classification': {
                'accuracy': accuracy_score(y_test_clf, clf_preds),
                'actual': y_test_clf,
                'predicted': clf_preds,
                'proba': clf_proba  
            }
        }
