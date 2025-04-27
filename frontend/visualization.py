import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import timedelta

def render_stock_visualizations(results):
    """Render all stock prediction visualizations with array support"""
    try:
        # Validate input structure
        required_keys = ['ticker', 'historical_data', 'prediction', 'evaluation']
        if not all(k in results for k in required_keys):
            raise ValueError(f"Missing required keys in results: {required_keys}")

        ticker = results['ticker']
        data = results['historical_data']
        pred = results['prediction']
        eval_data = results['evaluation']

        # Convert numpy arrays to pandas Series if needed
        if isinstance(eval_data['regression']['actual'], np.ndarray):
            dates = data.index[-len(eval_data['regression']['actual']):]
            eval_data['regression']['actual'] = pd.Series(
                eval_data['regression']['actual'],
                index=dates
            )
            eval_data['regression']['predicted'] = pd.Series(
                eval_data['regression']['predicted'],
                index=dates
            )
            eval_data['classification']['actual'] = pd.Series(
                eval_data['classification']['actual'],
                index=dates
            )
            eval_data['classification']['predicted'] = pd.Series(
                eval_data['classification']['predicted'],
                index=dates
            )

        # Start rendering
        st.title(f"{ticker} Stock Analysis")
        
        # 1. Prediction Cards
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Predicted Price", f"${pred['price']:.2f}")
        with col2:
            st.metric("Direction", pred['direction'])

        # 2. Actual vs Predicted Plot
        st.subheader("Actual vs Predicted Prices")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=eval_data['regression']['actual'].index,
            y=eval_data['regression']['actual'],
            name='Actual',
            line=dict(color='blue')
        ))
        fig.add_trace(go.Scatter(
            x=eval_data['regression']['predicted'].index,
            y=eval_data['regression']['predicted'],
            name='Predicted',
            line=dict(color='orange', dash='dash')
        ))
        st.plotly_chart(fig, use_container_width=True)

        # 3. Historical Trend
        st.subheader("Price Trend")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            name='Close Price'
        ))
        st.plotly_chart(fig, use_container_width=True)

        # 4. Performance Metrics
        st.subheader("Model Performance")
        mae = eval_data['regression'].get('mae', 'N/A')
        accuracy = eval_data['classification'].get('accuracy', 'N/A')
        st.metric("MAE", f"${mae:.2f}" if isinstance(mae, (int, float)) else mae)
        st.metric("Accuracy", f"{accuracy*100:.1f}%" if isinstance(accuracy, (int, float)) else accuracy)

    except Exception as e:
        st.error(f"Visualization error: {str(e)}")
        st.write("Debug - results keys:", list(results.keys()))
        if 'evaluation' in results:
            st.write("Evaluation keys:", list(results['evaluation'].keys()))
            st.write("Regression data type:", type(results['evaluation']['regression']['actual']))