import streamlit as st
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="SentimentEdge™",
    page_icon="🎯",
    layout="wide"
)

# Header
st.markdown("# 🎯 SentimentEdge™")
st.markdown("### AI Trading Platform")

# Key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Portfolio Value", "$100,247", "+$247")

with col2:
    st.metric("Win Rate", "67%", "2 of 3")

with col3:
    st.metric("Active Positions", "3", "AAPL, TSLA, MSFT")

with col4:
    st.metric("Daily P&L", "+0.25%", "+$247.50")

# Simple data
st.markdown("## 📊 Current Positions")
positions = pd.DataFrame({
    'Symbol': ['AAPL', 'TSLA', 'MSFT'],
    'Shares': [25, 10, 15],
    'Value': ['$4,737', '$2,420', '$4,200'],
    'P&L': ['+2.1%', '-0.8%', '+1.5%']
})
st.dataframe(positions, use_container_width=True)

# Trading signals
st.markdown("## 🎯 AI Signals")
col1, col2, col3 = st.columns(3)

with col1:
    st.success("AAPL: BUY (85%)")

with col2:
    st.warning("TSLA: HOLD (72%)")

with col3:
    st.success("MSFT: BUY (78%)")

st.success("🚀 SentimentEdge™ AI Trading Platform - Live!")