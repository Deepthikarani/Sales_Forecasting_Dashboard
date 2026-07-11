import streamlit as st
import pandas as pd
import plotly.express as px
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Forecast Explorer",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 Forecast Explorer")

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
# User Inputs
# -------------------------------------------------
forecast_type = st.radio(
    "Forecast By",
    ["Category", "Region"],
    horizontal=True
)

if forecast_type == "Category":
    selected = st.selectbox(
        "Select Category",
        sorted(df["Category"].unique())
    )
    filtered = df[df["Category"] == selected]

else:
    selected = st.selectbox(
        "Select Region",
        sorted(df["Region"].unique())
    )
    filtered = df[df["Region"] == selected]

months = st.slider(
    "Forecast Horizon (Months)",
    min_value=1,
    max_value=3,
    value=3
)

# -------------------------------------------------
# Prepare Monthly Sales
# -------------------------------------------------
monthly = (
    filtered.groupby(pd.Grouper(key="Order Date", freq="ME"))["Sales"]
    .sum()
    .reset_index()
)

monthly.columns = ["ds", "y"]

# -------------------------------------------------
# Train-Test Split
# -------------------------------------------------
train_size = int(len(monthly) * 0.8)

train = monthly.iloc[:train_size]
test = monthly.iloc[train_size:]

# -------------------------------------------------
# Train Prophet
# -------------------------------------------------
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=False,
    daily_seasonality=False
)

model.fit(train)

# -------------------------------------------------
# Evaluate Model
# -------------------------------------------------
future_test = model.make_future_dataframe(
    periods=len(test),
    freq="ME"
)

forecast_test = model.predict(future_test)

forecast_test = forecast_test.tail(len(test))

mae = mean_absolute_error(
    test["y"],
    forecast_test["yhat"]
)

rmse = np.sqrt(
    mean_squared_error(
        test["y"],
        forecast_test["yhat"]
    )
)

# -------------------------------------------------
# Forecast Next Months
# -------------------------------------------------
future = model.make_future_dataframe(
    periods=months,
    freq="ME"
)

forecast = model.predict(future)

forecast_output = forecast.tail(months)[
    ["ds", "yhat", "yhat_lower", "yhat_upper"]
]

# -------------------------------------------------
# Forecast Chart
# -------------------------------------------------
st.subheader(f"Forecast for {selected}")

fig = px.line(
    forecast,
    x="ds",
    y="yhat",
    markers=True
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Forecast Sales",
    template="plotly_white"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------
# Metrics
# -------------------------------------------------
c1, c2 = st.columns(2)

c1.metric(
    "MAE",
    f"{mae:,.2f}"
)

c2.metric(
    "RMSE",
    f"{rmse:,.2f}"
)

# -------------------------------------------------
# Forecast Table
# -------------------------------------------------
st.subheader("Forecast Output")

forecast_output.columns = [
    "Date",
    "Forecast Sales",
    "Lower Confidence",
    "Upper Confidence"
]

st.dataframe(
    forecast_output,
    use_container_width=True
)