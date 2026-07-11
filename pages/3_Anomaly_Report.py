import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Anomaly Report",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Weekly Sales Anomaly Report")

st.markdown(
    """
This page identifies unusual sales weeks using the **Isolation Forest**
algorithm. Weeks highlighted in red represent anomalous sales patterns.
"""
)

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------
@st.cache_data
def load_data():

    df = pd.read_csv("train.csv")

    df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    dayfirst=True
)

    return df


df = load_data()

# -------------------------------------------------
# Weekly Sales
# -------------------------------------------------
weekly_sales = (
    df.groupby(
        pd.Grouper(
            key="Order Date",
            freq="W"
        )
    )["Sales"]
    .sum()
    .reset_index()
)

# -------------------------------------------------
# Isolation Forest
# -------------------------------------------------
model = IsolationForest(
    contamination=0.05,
    random_state=42
)

weekly_sales["Anomaly"] = model.fit_predict(
    weekly_sales[["Sales"]]
)

weekly_sales["Anomaly"] = weekly_sales["Anomaly"].map(
    {
        1: "Normal",
        -1: "Anomaly"
    }
)

anomalies = weekly_sales[
    weekly_sales["Anomaly"] == "Anomaly"
]

# -------------------------------------------------
# KPI
# -------------------------------------------------
c1, c2 = st.columns(2)

c1.metric(
    "Total Weeks",
    len(weekly_sales)
)

c2.metric(
    "Anomalies Detected",
    len(anomalies)
)

st.divider()

# -------------------------------------------------
# Plot
# -------------------------------------------------
fig = go.Figure()

# Weekly Sales Line
fig.add_trace(

    go.Scatter(

        x=weekly_sales["Order Date"],

        y=weekly_sales["Sales"],

        mode="lines",

        name="Weekly Sales",

        line=dict(width=2)

    )

)

# Anomaly Points
fig.add_trace(

    go.Scatter(

        x=anomalies["Order Date"],

        y=anomalies["Sales"],

        mode="markers",

        marker=dict(
            size=10,
            color="red",
            symbol="diamond"
        ),

        name="Anomalies"

    )

)

fig.update_layout(

    title="Weekly Sales with Detected Anomalies",

    xaxis_title="Week",

    yaxis_title="Sales",

    template="plotly_white"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------
# Table
# -------------------------------------------------
st.subheader("Detected Anomalies")

table = anomalies[
    ["Order Date", "Sales"]
].copy()

table.columns = [
    "Anomaly Date",
    "Weekly Sales"
]

st.dataframe(
    table,
    use_container_width=True
)

# -------------------------------------------------
# Download Button
# -------------------------------------------------
csv = table.to_csv(index=False)

st.download_button(
    label="⬇ Download Anomaly Report",
    data=csv,
    file_name="anomaly_report.csv",
    mime="text/csv"
)