import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score , confusion_matrix, roc_curve, auc
import plotly.figure_factory as ff


def render_stock_visualizations(results):
    """Render stock prediction visualizations with focus on trading decisions"""
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
            'actual': '#00FF00',
            'predicted': '#FF0000',
            'up': '#00FF00',
            'down': '#FF0000',
            'accuracy_high': '#00FF00',
            'accuracy_med': '#FFA500',
            'accuracy_low': '#FF0000'
        }

        # 1. Prediction Summary Cards
        st.subheader("Trading Recommendation")
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
            rec = "BUY" if direction == "UP" else "SELL"
            color = color_scheme['up'] if direction == "UP" else color_scheme['down']
            st.metric("Recommendation", rec, delta_color="off")
        # 2. Actual vs Predicted Comparison
        st.subheader("Model Performance: Actual vs Predicted")
        try:
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

            fig2.add_trace(go.Scatter(
                x=eval_data['regression']['actual'].index,
                y=eval_data['regression']['actual'],
                name='Actual Price',
                line=dict(color=color_scheme['actual'], width=2),
                mode='lines+markers'
            ))

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

        # 3. Volatility & Price Change Trend
        st.subheader("Volatility & Price Change Trend")
        try:
            # Convert numpy array to pandas Series if needed
            if isinstance(eval_data['regression']['actual'], np.ndarray):
                actual_prices = pd.Series(
                    eval_data['regression']['actual'],
                    index=pd.to_datetime(dates['test_dates'])
                )
            else:
                actual_prices = eval_data['regression']['actual']

            # Now calculate returns and volatility
            returns = actual_prices.pct_change().dropna() * 100
            volatility = returns.rolling(window=5).std()

            fig_vol = go.Figure()

            fig_vol.add_trace(go.Scatter(
                x=returns.index,
                y=returns,
                name='Daily Return (%)',
                line=dict(color='orange', width=2),
                mode='lines+markers',
                yaxis='y1'
            ))

            fig_vol.add_trace(go.Scatter(
                x=volatility.index,
                y=volatility,
                name='Rolling Volatility (5D)',
                line=dict(color='purple', width=2, dash='dot'),
                mode='lines',
                yaxis='y2'
            ))

            fig_vol.update_layout(
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title='Date',
                yaxis=dict(title='Daily Return (%)', side='left', showgrid=False),
                yaxis2=dict(title='Volatility', overlaying='y', side='right', showgrid=False),
                hovermode='x unified',
                legend=dict(x=0, y=1.15, orientation='h')
            )

            st.plotly_chart(fig_vol, use_container_width=True)

        except Exception as e:
            st.error(f"Error in Volatility Plot: {str(e)}")

        # 4. Moving Average Crossover
        st.subheader("Moving Average Crossover")
        try:
            if isinstance(hist_data, pd.DataFrame):
                if ('MA_5', '') in hist_data.columns and ('MA_20', '') in hist_data.columns:
                    ma_short = hist_data[('MA_5', '')]
                    ma_long = hist_data[('MA_20', '')]
                    prices = hist_data[('Close', 'GOOGL')] if ('Close', 'GOOGL') in hist_data.columns else hist_data.iloc[:, 0]
                    
                    fig_ma = go.Figure()
                    
                    # Price line
                    fig_ma.add_trace(go.Scatter(
                        x=prices.index,
                        y=prices,
                        name='Price',
                        line=dict(color='#1f77b4', width=1),
                        mode='lines'
                    ))
                    
                    # Short MA
                    fig_ma.add_trace(go.Scatter(
                        x=ma_short.index,
                        y=ma_short,
                        name='5-Day MA',
                        line=dict(color=color_scheme['up'], width=2),
                        mode='lines'
                    ))
                    
                    # Long MA
                    fig_ma.add_trace(go.Scatter(
                        x=ma_long.index,
                        y=ma_long,
                        name='20-Day MA',
                        line=dict(color=color_scheme['down'], width=2),
                        mode='lines'
                    ))
                    
                    # Highlight crossover points
                    crossover_up = (ma_short > ma_long) & (ma_short.shift(1) <= ma_long.shift(1))
                    crossover_down = (ma_short < ma_long) & (ma_short.shift(1) >= ma_long.shift(1))
                    
                    fig_ma.add_trace(go.Scatter(
                        x=prices.index[crossover_up],
                        y=prices[crossover_up],
                        name='Buy Signal',
                        mode='markers',
                        marker=dict(
                            color=color_scheme['up'],
                            size=10,
                            symbol='triangle-up')
                    ))
                    
                    fig_ma.add_trace(go.Scatter(
                        x=prices.index[crossover_down],
                        y=prices[crossover_down],
                        name='Sell Signal',
                        mode='markers',
                        marker=dict(
                            color=color_scheme['down'],
                            size=10,
                            symbol='triangle-down')
                    ))
                    
                    fig_ma.update_layout(
                        height=500,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        xaxis_title='Date',
                        yaxis_title='Price ($)',
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig_ma, use_container_width=True)
                    
        except Exception as e:
            st.error(f"Error in Moving Average Plot: {str(e)}")

        # 5. RSI Indicator with Overbought/Oversold Levels
        st.subheader("RSI Indicator")
        try:
            if isinstance(hist_data, pd.DataFrame) and ('RSI', '') in hist_data.columns:
                rsi = hist_data[('RSI', '')]
                
                fig_rsi = go.Figure()
                
                # RSI line
                fig_rsi.add_trace(go.Scatter(
                    x=rsi.index,
                    y=rsi,
                    name='RSI',
                    line=dict(color='#FFA500', width=2),
                    mode='lines'
                ))
                
                # Overbought level
                fig_rsi.add_hline(y=70, line_dash="dash", 
                                line_color=color_scheme['down'],
                                annotation_text="Overbought",
                                annotation_position="top right")
                
                # Oversold level
                fig_rsi.add_hline(y=30, line_dash="dash",
                                line_color=color_scheme['up'],
                                annotation_text="Oversold", 
                                annotation_position="bottom right")
                
                # Current RSI marker
                last_rsi = rsi.iloc[-1]
                fig_rsi.add_trace(go.Scatter(
                    x=[rsi.index[-1]],
                    y=[last_rsi],
                    name='Current',
                    mode='markers',
                    marker=dict(
                        color='yellow',
                        size=10,
                        line=dict(width=1, color='black')
                )))
                
                fig_rsi.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis_title='Date',
                    yaxis_title='RSI',
                    yaxis_range=[0, 100],
                    hovermode='x unified'
                )
                st.plotly_chart(fig_rsi, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error in RSI Plot: {str(e)}")

        st.subheader("Prediction Accuracy (%)")
        try:
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

        # 5. Model Performance Metrics
        st.subheader("Model Performance Metrics")
        try:
            mae = eval_data['regression'].get('mae', np.nan)
            y_true = eval_data['classification']['actual']
            y_pred = eval_data['classification']['predicted']

            cls_metrics = {
                'Accuracy': accuracy_score(y_true, y_pred),
                'Precision': precision_score(y_true, y_pred),
                'Recall': recall_score(y_true, y_pred),
                'F1 Score': f1_score(y_true, y_pred)
            }

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

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Regression Metrics")

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
        # Add Confusion Matrix and ROC Curve
        st.subheader("Confusion Matrix & ROC Curve")
        try:
            y_true = eval_data['classification']['actual']
            y_pred = eval_data['classification']['predicted']

            if isinstance(y_true, pd.Series) and isinstance(y_pred, (np.ndarray, list)):
                # Ensure both are aligned by index
                y_true = y_true.reset_index(drop=True)
                y_pred = pd.Series(y_pred).reset_index(drop=True)

                # Confusion Matrix
                cm = confusion_matrix(y_true, y_pred)
                cm_labels = ["Down (0)", "Up (1)"]
                z = cm.tolist()

                fig_cm = ff.create_annotated_heatmap(
                    z=z,
                    x=cm_labels,
                    y=cm_labels,
                    colorscale='Blues',
                    showscale=True,
                    hoverinfo="z"
                )
                fig_cm.update_layout(
                    title_text="Confusion Matrix",
                    font=dict(color='white'),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_cm, use_container_width=True)

                # ROC Curve
                if 'proba' in eval_data['classification']:  # Only if probability scores available
                    y_proba = eval_data['classification']['proba']
                    fpr, tpr, _ = roc_curve(y_true, y_proba)
                    roc_auc = auc(fpr, tpr)

                    fig_roc = go.Figure()
                    fig_roc.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', name='ROC Curve'))
                    fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Random', line=dict(dash='dash')))

                    fig_roc.update_layout(
                        title=f"ROC Curve (AUC = {roc_auc:.2f})",
                        xaxis_title='False Positive Rate',
                        yaxis_title='True Positive Rate',
                        font=dict(color='white'),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig_roc, use_container_width=True)
        except Exception as e:
            
            st.error(f"Error displaying confusion matrix or ROC curve: {str(e)}")
            
        st.markdown("---")
        st.subheader("Project Team")
        st.markdown("""
        <style>
        .team-container {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-top: 1rem;
        }
        .team-member {
            flex: 1;
            min-width: 200px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 0.5rem;
            padding: 1rem;
            background-color: rgba(0, 0, 0, 0.2);
        }
        .member-name {
            font-weight: bold;
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
            color: #4FC3F7;
        }
        .member-role {
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.8);
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="team-container">
            <div class="team-member">
                <div class="member-name">Vignesh S</div>
                <div class="member-role">Model Building & Training</div>
            </div>
            <div class="team-member">
                <div class="member-name">Umar Farooq V H</div>
                <div class="member-role">Front-End Design & Exploratory Data Analysis</div>
            </div>
            <div class="team-member">
                <div class="member-name">Vikram M</div>
                <div class="member-role">Data Cleaning & Feature Engineering</div>
            </div>
            <div class="team-member">
                <div class="member-name">Sheshathri M</div>
                <div class="member-role">Documentation & Reporting</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.warning(""" 
        **Disclaimer:**  
        This is a non-commercial academic project. Predictions are for educational purposes only and may involve financial risks if used for trading.  
        Please consult a financial advisor before making any investment decisions.
        """)
        
    except Exception as e:
        st.error(f"Visualization error: {str(e)}")
