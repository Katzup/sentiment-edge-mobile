import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page config
st.set_page_config(
    page_title="SentimentEdge™",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS for mobile
st.markdown("""
<style>
.metric-card {
    background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
    padding: 1rem;
    border-radius: 0.5rem;
    border: 1px solid #00D4FF33;
    margin: 0.5rem 0;
}
.metric-value {
    font-size: 1.5rem;
    font-weight: bold;
    color: #00D4FF;
}
.metric-label {
    color: #CCCCCC;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #00D4FF;">🎯 SentimentEdge™</h1>
    <p style="color: #888;">AI Trading Platform</p>
</div>
""", unsafe_allow_html=True)

# Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Portfolio Value</div>
        <div class="metric-value">$100,247</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Daily P&L</div>
        <div class="metric-value" style="color: #00FF88;">+$247 (+0.25%)</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Active Positions</div>
        <div class="metric-value">3</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Win Rate</div>
        <div class="metric-value">67%</div>
    </div>
    """, unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💼 Portfolio", "🎯 Signals"])

with tab1:
    st.subheader("📈 Portfolio Performance")
    
    # Sample chart
    data = pd.DataFrame({
        'Date': pd.date_range('2024-07-01', periods=14),
        'Value': [100000 + i*247 for i in range(14)]
    })
    
    fig = px.line(data, x='Date', y='Value', title="Portfolio Growth")
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("📊 Current Positions")
    
    positions = pd.DataFrame({
        'Symbol': ['AAPL', 'TSLA', 'MSFT'],
        'Quantity': [25, 10, 15],
        'Value': ['$4,737', '$2,420', '$4,200'],
        'P&L': ['+2.1%', '-0.8%', '+1.5%']
    })
    
    st.dataframe(positions, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("🎯 AI Trading Signals")
    
    signals = [
        {"Symbol": "AAPL", "Signal": "BUY", "Confidence": "85%"},
        {"Symbol": "TSLA", "Signal": "HOLD", "Confidence": "72%"},
        {"Symbol": "MSFT", "Signal": "BUY", "Confidence": "78%"}
    ]
    
    for signal in signals:
        color = "#00FF88" if signal["Signal"] == "BUY" else "#FFAA00"
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <strong>{signal['Symbol']}</strong><br>
                    <span style="color: {color};">{signal['Signal']}</span>
                </div>
                <div style="text-align: right;">
                    Confidence<br>
                    <strong>{signal['Confidence']}</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Mobile install prompt
st.markdown("---")
st.info("📱 Add to your phone's home screen for the best mobile experience!")
st.success("🚀 SentimentEdge™ AI Trading Platform - Live and Global!")