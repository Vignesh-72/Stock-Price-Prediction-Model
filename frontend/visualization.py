import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

def render_stock_visualizations(results):
    """Render all stock prediction visualizations using Streamlit"""
    ticker = results['ticker']
    data = results['historical_data']
    pred = results['prediction']
    eval_data = results['evaluation']
    
    st.title(f"{ticker} Stock Analysis")
    
    # 1. Main Prediction Card
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Predicted Closing Price", 
                 f"${pred['price']:.2f}",
                 f"{(pred['price'] - pred['last_close']):.2f} from previous close")
    with col2:
        direction_color = "green" if pred['direction'] == "UP" else "red"
        st.metric("Predicted Direction", 
                 pred['direction'],
                 delta_color="off",
                 help="Predicted movement for next trading day")
    
    # 2. Actual vs Predicted Prices (Plotly)
    st.subheader("Actual vs Predicted Prices")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=eval_data['regression']['actual'].index,
        y=eval_data['regression']['actual'],
        name='Actual Price',
        line=dict(color='blue')))
    fig1.add_trace(go.Scatter(
        x=eval_data['regression']['predicted'].index,
        y=eval_data['regression']['predicted'],
        name='Predicted Price',
        line=dict(color='orange', dash='dash')))
    fig1.update_layout(
        xaxis_title='Date',
        yaxis_title='Price ($)',
        hovermode='x unified',
        showlegend=True,
        height=500)
    st.plotly_chart(fig1, use_container_width=True)
    
    # 3. Historical Trend with Tomorrow's Prediction
    st.subheader("Price Trend with Forecast")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        name='Historical Prices',
        line=dict(color='gray')))
    # Add tomorrow's prediction
    future_date = data.index[-1] + pd.Timedelta(days=1)
    fig2.add_trace(go.Scatter(
        x=[future_date],
        y=[pred['price']],
        name='Tomorrow Prediction',
        mode='markers',
        marker=dict(color='red', size=12)))
    fig2.update_layout(
        height=400,
        showlegend=True)
    st.plotly_chart(fig2, use_container_width=True)
    
    # 4. Moving Average Crossover Strategy
    st.subheader("Moving Average Crossover Signals")
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        name='Price',
        line=dict(color='black', width=1)))
    fig3.add_trace(go.Scatter(
        x=data.index,
        y=data['MA_5'],
        name='5-Day MA',
        line=dict(color='blue', width=2)))
    fig3.add_trace(go.Scatter(
        x=data.index,
        y=data['MA_20'],
        name='20-Day MA',
        line=dict(color='orange', width=2)))
    
    # Add buy/sell signals
    cross_above = (data['MA_5'] > data['MA_20']) & (data['MA_5'].shift(1) <= data['MA_20'].shift(1))
    cross_below = (data['MA_5'] < data['MA_20']) & (data['MA_5'].shift(1) >= data['MA_20'].shift(1))
    
    fig3.add_trace(go.Scatter(
        x=data[cross_above].index,
        y=data[cross_above]['Close'],
        mode='markers',
        name='Buy Signal',
        marker=dict(color='green', size=10, symbol='triangle-up')))
    fig3.add_trace(go.Scatter(
        x=data[cross_below].index,
        y=data[cross_below]['Close'],
        mode='markers',
        name='Sell Signal',
        marker=dict(color='red', size=10, symbol='triangle-down')))
    
    fig3.update_layout(
        height=500,
        hovermode='x unified')
    st.plotly_chart(fig3, use_container_width=True)
    
    # 5. Prediction Accuracy
    st.subheader("Model Prediction Accuracy")
    error = eval_data['regression']['actual'] - eval_data['regression']['predicted']
    error_percent = (error / eval_data['regression']['actual']) * 100
    accuracy = 100 - np.abs(error_percent)
    
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        x=accuracy.index,
        y=accuracy,
        marker_color=np.where(accuracy >= 95, 'green',
                            np.where(accuracy >= 90, 'orange', 'red')),
        name='Accuracy %'))
    fig4.add_hline(y=95, line_dash="dot",
                  annotation_text="Excellent (95%+)", 
                  annotation_position="bottom right")
    fig4.add_hline(y=90, line_dash="dot",
                  annotation_text="Good (90-95%)", 
                  annotation_position="bottom right")
    fig4.update_layout(
        yaxis_title='Accuracy (%)',
        yaxis_range=[80,100],
        height=400)
    st.plotly_chart(fig4, use_container_width=True)
    
    # 6. Additional Metrics
    st.subheader("Model Performance Metrics")
    metrics_col1, metrics_col2 = st.columns(2)
    with metrics_col1:
        st.metric("Regression MAE", 
                 f"${eval_data['regression']['mae']:.2f}",
                 help="Mean Absolute Error")
    with metrics_col2:
        st.metric("Classification Accuracy", 
                 f"{eval_data['classification']['accuracy']*100:.1f}%",
                 help="Direction prediction accuracy")