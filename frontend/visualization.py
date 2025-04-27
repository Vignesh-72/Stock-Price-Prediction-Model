import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import timedelta

def render_stock_visualizations(results):
    """Render all stock prediction visualizations with robust type handling"""
    try:
        # Validate input structure
        required_keys = ['ticker', 'historical_data', 'prediction', 'evaluation', 'dates']
        if not all(k in results for k in required_keys):
            st.error(f"Missing required data in results. Expected keys: {required_keys}")
            st.write("Actual keys received:", list(results.keys()))
            return

        ticker = results['ticker']
        hist_data = results['historical_data']
        pred = results['prediction']
        eval_data = results['evaluation']
        dates = results['dates']

        # Prepare evaluation data - convert arrays to Series if needed
        if isinstance(eval_data['regression']['actual'], np.ndarray):
            test_dates = dates['test_dates']
            eval_data['regression']['actual'] = pd.Series(
                eval_data['regression']['actual'],
                index=test_dates
            )
            eval_data['regression']['predicted'] = pd.Series(
                eval_data['regression']['predicted'],
                index=test_dates
            )
            eval_data['classification']['actual'] = pd.Series(
                eval_data['classification']['actual'],
                index=test_dates
            )
            eval_data['classification']['predicted'] = pd.Series(
                eval_data['classification']['predicted'],
                index=test_dates
            )

        # Start rendering
        st.title(f"{ticker} Stock Analysis")
        
        # 1. Prediction Cards
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Predicted Closing Price", 
                     f"${pred['price']:.2f}",
                     f"{(pred['price'] - pred['last_close']):.2f} from previous close")
        with col2:
            direction_color = "green" if pred['direction'] == "UP" else "red"
            st.metric("Predicted Direction", 
                     pred['direction'],
                     delta_color="off")

        # 2. Actual vs Predicted Plot
        st.subheader("Actual vs Predicted Prices")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=eval_data['regression']['actual'].index,
            y=eval_data['regression']['actual'],
            name='Actual Price',
            line=dict(color='blue')
        ))
        fig.add_trace(go.Scatter(
            x=eval_data['regression']['predicted'].index,
            y=eval_data['regression']['predicted'],
            name='Predicted Price',
            line=dict(color='orange', dash='dash')
        ))
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Price ($)',
            hovermode='x unified',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

        # 3. Historical Trend with Forecast
        st.subheader("Price Trend with Forecast")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist_data.index,
            y=hist_data['Close'],
            name='Historical Prices',
            line=dict(color='gray')
        ))
        try:
            future_date = hist_data.index[-1] + timedelta(days=1)
            fig.add_trace(go.Scatter(
                x=[future_date],
                y=[pred['price']],
                name='Tomorrow Prediction',
                mode='markers',
                marker=dict(color='red', size=12)
            ))
        except Exception as e:
            st.warning(f"Couldn't render forecast: {str(e)}")
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

        # 4. Model Performance Metrics
        st.subheader("Model Performance")
        cols = st.columns(2)
        with cols[0]:
            if 'mae' in eval_data['regression']:
                st.metric("Regression MAE", 
                         f"${eval_data['regression']['mae']:.2f}",
                         help="Mean Absolute Error")
            else:
                st.warning("MAE data not available")
        
        with cols[1]:
            if 'accuracy' in eval_data['classification']:
                st.metric("Classification Accuracy", 
                         f"{eval_data['classification']['accuracy']*100:.1f}%",
                         help="Direction prediction accuracy")
            else:
                st.warning("Accuracy data not available")

    except Exception as e:
        st.error(f"Failed to render visualizations: {str(e)}")
    
    # Simpler debug output
        debug_info = {}
        debug_info['ticker'] = type(results.get('ticker'))
        debug_info['historical_data'] = type(results.get('historical_data'))
    
        pred = results.get('prediction', {})
        debug_info['prediction'] = pred.keys() if isinstance(pred, dict) else type(pred)
    
        eval_data = results.get('evaluation', {})
        debug_info['evaluation_keys'] = list(eval_data.keys()) if isinstance(eval_data, dict) else type(eval_data)
    
        dates = results.get('dates', {})
        debug_info['dates_keys'] = list(dates.keys()) if isinstance(dates, dict) else type(dates)
    
        st.write("Debug Info - Results Structure:", debug_info)