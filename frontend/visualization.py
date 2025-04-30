import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render_stock_visualizations(results):
    """Render all stock prediction visualizations with proper line visibility"""
    try:
        # Validate input structure
        required_keys = ['ticker', 'historical_data', 'prediction', 'evaluation', 'dates']
        if not all(k in results for k in required_keys):
            st.error(f"Missing required data in results. Expected keys: {required_keys}")
            return

        ticker = results['ticker']
        hist_data = results['historical_data']
        pred = results['prediction']
        eval_data = results['evaluation']
        dates = results['dates']

        # Debug: Check data structure
        st.write("Debug - Historical data columns:", hist_data.columns.tolist())
        st.write("Debug - Evaluation data keys:", eval_data.keys())

        # Ensure data is properly formatted
        if not isinstance(hist_data, pd.DataFrame):
            st.error("Historical data is not a DataFrame")
            return

        # Create a color scheme that works in dark mode
        color_scheme = {
            'price': '#00FFFF',  # Bright cyan
            'ma5': '#FF00FF',    # Magenta
            'ma20': '#FFFF00',   # Yellow
            'actual': '#00FF00', # Green
            'predicted': '#FF0000', # Red
            'rsi': '#FFA500',    # Orange
            'signal_up': '#00FF00',
            'signal_down': '#FF0000',
            'prediction': '#FFFFFF'  # White
        }

        # 1. Main Price Chart with Moving Averages
        st.subheader("Price Trend with Indicators")
        try:
            fig1 = go.Figure()
            
            # Add price line
            fig1.add_trace(go.Scatter(
                x=hist_data.index,
                y=hist_data['Close'],
                name='Price',
                line=dict(color=color_scheme['price'], width=2),
                mode='lines'
            ))
            
            # Add moving averages
            fig1.add_trace(go.Scatter(
                x=hist_data.index,
                y=hist_data['MA_5'],
                name='5-Day MA',
                line=dict(color=color_scheme['ma5'], width=1),
                mode='lines'
            ))
            
            fig1.add_trace(go.Scatter(
                x=hist_data.index,
                y=hist_data['MA_20'],
                name='20-Day MA',
                line=dict(color=color_scheme['ma20'], width=1),
                mode='lines'
            ))

            # Update layout
            fig1.update_layout(
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
                hovermode='x unified'
            )
            st.plotly_chart(fig1, use_container_width=True)
        except Exception as e:
            st.error(f"Error in Price Trend: {str(e)}")

        # 2. Actual vs Predicted Prices
        st.subheader("Actual vs Predicted Prices")
        try:
            fig2 = go.Figure()
            
            # Convert evaluation data if needed
            if isinstance(eval_data['regression']['actual'], np.ndarray):
                eval_data['regression']['actual'] = pd.Series(
                    eval_data['regression']['actual'],
                    index=pd.to_datetime(dates['test_dates'])
                )
            
            if isinstance(eval_data['regression']['predicted'], np.ndarray):
                eval_data['regression']['predicted'] = pd.Series(
                    eval_data['regression']['predicted'],
                    index=pd.to_datetime(dates['test_dates'])
                )

            # Add actual prices
            fig2.add_trace(go.Scatter(
                x=eval_data['regression']['actual'].index,
                y=eval_data['regression']['actual'],
                name='Actual',
                line=dict(color=color_scheme['actual'], width=2),
                mode='lines'
            ))
            
            # Add predicted prices
            fig2.add_trace(go.Scatter(
                x=eval_data['regression']['predicted'].index,
                y=eval_data['regression']['predicted'],
                name='Predicted',
                line=dict(color=color_scheme['predicted'], width=2, dash='dash'),
                mode='lines'
            ))

            fig2.update_layout(
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig2, use_container_width=True)
        except Exception as e:
            st.error(f"Error in Actual vs Predicted: {str(e)}")

        # 3. RSI Indicator - Fixed subplot implementation
        st.subheader("RSI Indicator")
        try:
            # Create figure with secondary y-axis
            fig3 = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                               vertical_spacing=0.05, row_heights=[0.7, 0.3])
            
            # Price plot (top)
            fig3.add_trace(
                go.Scatter(
                    x=hist_data.index,
                    y=hist_data['Close'],
                    name='Price',
                    line=dict(color=color_scheme['price'], width=1)
                ),
                row=1, col=1
            )
            
            # RSI plot (bottom)
            fig3.add_trace(
                go.Scatter(
                    x=hist_data.index,
                    y=hist_data['RSI'],
                    name='RSI',
                    line=dict(color=color_scheme['rsi'], width=1)
                ),
                row=2, col=1
            )
            
            # Add RSI reference lines
            fig3.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
            fig3.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
            
            # Update layout
            fig3.update_layout(
                height=600,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=False
            )
            
            # Update y-axes
            fig3.update_yaxes(title_text="Price ($)", row=1, col=1)
            fig3.update_yaxes(title_text="RSI", range=[0,100], row=2, col=1)
            
            st.plotly_chart(fig3, use_container_width=True)
        except Exception as e:
            st.error(f"Error in RSI Indicator: {str(e)}")

    except Exception as e:
        st.error(f"Visualization error: {str(e)}")
        st.write("Debug info:", {
            'historical_data_type': type(hist_data),
            'historical_data_cols': hist_data.columns.tolist() if isinstance(hist_data, pd.DataFrame) else None,
            'evaluation_data': list(eval_data.keys()) if isinstance(eval_data, dict) else type(eval_data)
        })