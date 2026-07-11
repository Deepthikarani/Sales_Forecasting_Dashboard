import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Sales Overview",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Overview Dashboard")
st.markdown("Analyze yearly, monthly, regional and category-wise sales.")

# -------------------------------------------------
# Load Data
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
# KPI Cards
# -------------------------------------------------
total_sales = df["Sales"].sum()
total_orders = df["Order ID"].nunique()
avg_order_value = df.groupby("Order ID")["Sales"].sum().mean()

c1, c2, c3 = st.columns(3)

c1.metric("💰 Total Sales", f"${total_sales:,.0f}")
c2.metric("🛒 Total Orders", f"{total_orders:,}")
c3.metric("📦 Avg Order Value", f"${avg_order_value:,.2f}")

st.divider()

# =================================================
# 1. Total Sales by Year
# =================================================
st.subheader("📈 Total Sales by Year")

yearly_sales = (
    df.groupby(df["Order Date"].dt.year)["Sales"]
      .sum()
      .reset_index()
)

yearly_sales.columns = ["Year", "Sales"]

fig = px.bar(
    yearly_sales,
    x="Year",
    y="Sales",
    text_auto=".2s",
    color="Sales",
    title="Yearly Sales"
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Year",
    yaxis_title="Sales"
)

st.plotly_chart(fig, use_container_width=True)

# =================================================
# 2. Monthly Sales Trend
# =================================================
st.subheader("📅 Monthly Sales Trend")

monthly_sales = (
    df.groupby(pd.Grouper(key="Order Date", freq="ME"))["Sales"]
      .sum()
      .reset_index()
)

fig = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Month",
    yaxis_title="Sales"
)

st.plotly_chart(fig, use_container_width=True)

# =================================================
# 3. Interactive Filters
# =================================================
st.subheader("🎯 Sales by Region and Category")

col1, col2 = st.columns(2)

with col1:
    selected_region = st.selectbox(
        "Select Region",
        ["All"] + sorted(df["Region"].unique())
    )

with col2:
    selected_category = st.selectbox(
        "Select Category",
        ["All"] + sorted(df["Category"].unique())
    )

filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

# =================================================
# 4. Sales by Region
# =================================================
col1, col2 = st.columns(2)

with col1:

    region_sales = (
        filtered_df.groupby("Region")["Sales"]
                   .sum()
                   .reset_index()
    )

    fig = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        color="Region",
        title="Sales by Region"
    )

    fig.update_layout(template="plotly_white")

    st.plotly_chart(fig, use_container_width=True)

# =================================================
# 5. Sales by Category
# =================================================
with col2:

    category_sales = (
        filtered_df.groupby("Category")["Sales"]
                   .sum()
                   .reset_index()
    )

    fig = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        hole=0.45,
        title="Sales by Category"
    )

    st.plotly_chart(fig, use_container_width=True)

# =================================================
# 6. Filtered Dataset
# =================================================
st.subheader("📄 Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)