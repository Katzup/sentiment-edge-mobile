import streamlit as st
import pandas as pd

# Simple header
st.title("🎯 SentimentEdge™")
st.write("AI Trading Platform")

# Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Portfolio", "$100,247")
with col2:
    st.metric("Win Rate", "67%")
with col3:
    st.metric("Positions", "3")

# Table
data = {
    'Symbol': ['AAPL', 'TSLA', 'MSFT'],
    'P&L': ['+2.1%', '-0.8%', '+1.5%']
}
st.dataframe(pd.DataFrame(data))

st.success("Live Trading Active")