import streamlit as st

st.set_page_config(
    page_title="Retail Sales Dashboard",
    layout="wide"
)

st.title("📈 Retail Sales Forecasting Dashboard")

st.write("""
Welcome!

Use the sidebar to navigate.

Pages:

• Sales Overview

• Forecast Explorer

• Anomaly Report

• Product Demand Segments
""")