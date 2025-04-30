import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

def render_stock_visualizations(results):
    """Render stock prediction visualizations with focus on accuracy and predictions"""
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

        # Color scheme
        color_scheme = {
            'actual': '#00FF00',  # Green
            'predicted': '#FF0000',  # Red
            'up': '#00FF00',
            'down': '#FF0000',
            'accuracy_high': '#00FF00',
            'accuracy_med': '#FFA500',
            'accuracy_low': '#FF0000'
        }

        # 1. Prediction Summary Cards
        st.subheader("Prediction Summary")
        cols = st.columns(3)
        with cols[0]:
            st.metric("Last Close Price", f"${pred.get('last_close', 'N/A'):.2f}")
        with cols[1]:
            price_diff = pred.get('price', 0) - pred.get('last_close', 0)
            st.metric("Predicted Price", 
                     f"${pred.get('price', 'N/A'):.2f}",
                     f"{price_diff:.2f} ({price_diff/pred.get('last_close', 1)*100:.2f}%)")
        with cols[2]:
            direction = pred.get('direction', 'UNKNOWN')
            color = "green" if direction == "UP" else "red"
            st.metric("Predicted Direction", direction, delta_color="off")

        # 2. Recent Price History with Prediction
        st.subheader("Recent Price Trend with Prediction")
        try:
            # Get last 10 days of data
            recent_data = hist_data.iloc[-10:]
            
            fig1 = go.Figure()
            
            # Historical prices
            fig1.add_trace(go.Scatter(
                x=recent_data.index,
                y=recent_data['Close'],
                name='Historical Price',
                line=dict(color='#1f77b4', width=3),
                mode='lines+markers'
            ))
            
            # Tomorrow's prediction
            if 'price' in pred and isinstance(hist_data.index, pd.DatetimeIndex):
                future_date = hist_data.index[-1] + pd.Timedelta(days=1)
                fig1.add_trace(go.Scatter(
                    x=[future_date],
                    y=[pred['price']],
                    name='Tomorrow Prediction',
                    mode='markers',
                    marker=dict(
                        color='gold',
                        size=15,
                        line=dict(width=1, color='black')
                )))
            
            fig1.update_layout(
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title='Date',
                yaxis_title='Price ($)',
                hovermode='x unified'
            )
            st.plotly_chart(fig1, use_container_width=True)
        except Exception as e:
            st.error(f"Error in Recent Price Trend: {str(e)}")

        # 3. Actual vs Predicted Comparison
        st.subheader("Model Performance: Actual vs Predicted")
        try:
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

            fig2 = go.Figure()
            
            # Actual prices
            fig2.add_trace(go.Scatter(
                x=eval_data['regression']['actual'].index,
                y=eval_data['regression']['actual'],
                name='Actual Price',
                line=dict(color=color_scheme['actual'], width=2),
                mode='lines+markers'
            ))
            
            # Predicted prices
            fig2.add_trace(go.Scatter(
                x=eval_data['regression']['predicted'].index,
                y=eval_data['regression']['predicted'],
                name='Predicted Price',
                line=dict(color=color_scheme['predicted'], width=2, dash='dash'),
                mode='lines+markers'
            ))

            fig2.update_layout(
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title='Date',
                yaxis_title='Price ($)',
                hovermode='x unified'
            )
            st.plotly_chart(fig2, use_container_width=True)
        except Exception as e:
            st.error(f"Error in Actual vs Predicted: {str(e)}")

        # 4. Accuracy Percentage Plot
        st.subheader("Prediction Accuracy (%)")
        try:
            # Calculate accuracy
            actual = eval_data['regression']['actual']
            predicted = eval_data['regression']['predicted']
            error = actual - predicted
            accuracy = 100 - (abs(error) / actual * 100)
            
            fig3 = go.Figure()
            
            fig3.add_trace(go.Bar(
                x=actual.index,
                y=accuracy,
                marker_color=np.where(accuracy >= 95, color_scheme['accuracy_high'],
                                 np.where(accuracy >= 90, color_scheme['accuracy_med'],
                                          color_scheme['accuracy_low'])),
                name='Accuracy'
            ))
            
            # Add reference lines
            fig3.add_hline(y=95, line_dash="dash", line_color=color_scheme['accuracy_high'])
            fig3.add_hline(y=90, line_dash="dash", line_color=color_scheme['accuracy_med'])
            
            fig3.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title='Date',
                yaxis_title='Accuracy %',
                yaxis_range=[80, 100],
                hovermode='x unified'
            )
            st.plotly_chart(fig3, use_container_width=True)
        except Exception as e:
            st.error(f"Error in Accuracy Plot: {str(e)}")

        # 5. Model Performance Metrics - IMPROVED VERSION
        st.subheader("Model Performance Metrics")
        try:
            # Calculate all metrics first
            mae = eval_data['regression'].get('mae', np.nan)
            y_true = eval_data['classification']['actual']
            y_pred = eval_data['classification']['predicted']
            
            # Calculate all classification metrics
            cls_metrics = {
                'Accuracy': accuracy_score(y_true, y_pred),
                'Precision': precision_score(y_true, y_pred),
                'Recall': recall_score(y_true, y_pred),
                'F1 Score': f1_score(y_true, y_pred)
            }
            
            # Create a more professional metrics display
            st.markdown("""
            <style>
            .metric-card {
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 0.5rem;
                padding: 1rem;
                margin-bottom: 1rem;
                background-color: rgba(0, 0, 0, 0.2);
            }
            .metric-title {
                font-size: 1rem;
                font-weight: 600;
                margin-bottom: 0.5rem;
                color: #FFFFFF;
            }
            .metric-value {
                font-size: 1.5rem;
                font-weight: 700;
                color: #FFFFFF;
            }
            .metric-help {
                font-size: 0.8rem;
                color: rgba(255, 255, 255, 0.6);
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Create two columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Regression Metrics")
                
                # MAE card
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Mean Absolute Error (MAE)</div>
                    <div class="metric-value">{f"${mae:.2f}" if isinstance(mae, (int, float)) else mae}</div>
                    <div class="metric-help">Average absolute difference between actual and predicted prices</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Calculate and show MAPE
                actual_prices = eval_data['regression']['actual']
                predicted_prices = eval_data['regression']['predicted']
                mape = np.mean(np.abs((actual_prices - predicted_prices) / actual_prices)) * 100
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Mean Absolute Percentage Error (MAPE)</div>
                    <div class="metric-value">{mape:.2f}%</div>
                    <div class="metric-help">Average percentage difference between actual and predicted</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("### Classification Metrics")
                
                # Create a grid for classification metrics
                grid_col1, grid_col2 = st.columns(2)
                
                with grid_col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Accuracy</div>
                        <div class="metric-value">{cls_metrics['Accuracy']*100:.1f}%</div>
                        <div class="metric-help">Overall prediction correctness</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Precision</div>
                        <div class="metric-value">{cls_metrics['Precision']*100:.1f}%</div>
                        <div class="metric-help">Correct UP predictions</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with grid_col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">Recall</div>
                        <div class="metric-value">{cls_metrics['Recall']*100:.1f}%</div>
                        <div class="metric-help">Actual UP movements captured</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-title">F1 Score</div>
                        <div class="metric-value">{cls_metrics['F1 Score']*100:.1f}%</div>
                        <div class="metric-help">Balance of precision and recall</div>
                    </div>
                    """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error calculating metrics: {str(e)}")

    except Exception as e:
        st.error(f"Visualization error: {str(e)}")