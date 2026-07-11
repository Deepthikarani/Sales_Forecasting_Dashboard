import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# --------------------------------------------------------
# Page Config
# --------------------------------------------------------
st.set_page_config(
    page_title="Product Demand Segments",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Product Demand Segmentation")

st.markdown("""
This page segments product sub-categories into demand groups using
**K-Means Clustering** based on:

- Total Sales
- Sales Growth
- Sales Volatility
- Average Order Value
""")

# --------------------------------------------------------
# Load Dataset
# --------------------------------------------------------
@st.cache_data
def load_data():

    df = pd.read_csv("train.csv")

    df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    dayfirst=True
)
    return df

df = load_data()

# --------------------------------------------------------
# Feature Engineering
# --------------------------------------------------------

df["Year"] = df["Order Date"].dt.year

# Total Sales
total_sales = (
    df.groupby("Sub-Category")["Sales"]
      .sum()
      .rename("Total Sales")
)

# Average Order Value
average_order = (
    df.groupby("Sub-Category")["Sales"]
      .mean()
      .rename("Average Order Value")
)

# Monthly Sales
monthly_sales = (
    df.groupby(
        [
            "Sub-Category",
            pd.Grouper(
                key="Order Date",
                freq="ME"
            )
        ]
    )["Sales"]
    .sum()
    .reset_index()
)

# Sales Volatility
volatility = (
    monthly_sales.groupby("Sub-Category")["Sales"]
    .std()
    .fillna(0)
    .rename("Sales Volatility")
)

# Yearly Sales
yearly_sales = (
    df.groupby(
        [
            "Sub-Category",
            "Year"
        ]
    )["Sales"]
    .sum()
    .reset_index()
)

yearly_sales["Growth"] = (
    yearly_sales
    .groupby("Sub-Category")["Sales"]
    .pct_change()
)

growth = (
    yearly_sales.groupby("Sub-Category")["Growth"]
    .mean()
    .fillna(0)
    .rename("Sales Growth")
)

# --------------------------------------------------------
# Final Feature Table
# --------------------------------------------------------

cluster_df = pd.concat(
    [
        total_sales,
        growth,
        volatility,
        average_order
    ],
    axis=1
)

cluster_df = cluster_df.fillna(0)

# --------------------------------------------------------
# Scaling
# --------------------------------------------------------

scaler = StandardScaler()

scaled = scaler.fit_transform(cluster_df)

# --------------------------------------------------------
# KMeans
# --------------------------------------------------------

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

cluster_df["Cluster"] = kmeans.fit_predict(scaled)

# --------------------------------------------------------
# Rename Clusters
# --------------------------------------------------------

summary = (
    cluster_df.groupby("Cluster")["Total Sales"]
    .mean()
    .sort_values()
)

mapping = {}

mapping[summary.index[0]] = "Low Demand"
mapping[summary.index[1]] = "Medium Demand"
mapping[summary.index[2]] = "High Demand"

cluster_df["Demand Group"] = (
    cluster_df["Cluster"]
    .map(mapping)
)

# --------------------------------------------------------
# PCA
# --------------------------------------------------------

pca = PCA(n_components=2)

components = pca.fit_transform(scaled)

pca_df = pd.DataFrame(

    components,

    columns=["PC1", "PC2"],

    index=cluster_df.index

)

pca_df["Demand Group"] = cluster_df["Demand Group"]

# --------------------------------------------------------
# KPI Cards
# --------------------------------------------------------

c1, c2, c3 = st.columns(3)

c1.metric(
    "High Demand",
    (cluster_df["Demand Group"]=="High Demand").sum()
)

c2.metric(
    "Medium Demand",
    (cluster_df["Demand Group"]=="Medium Demand").sum()
)

c3.metric(
    "Low Demand",
    (cluster_df["Demand Group"]=="Low Demand").sum()
)

st.divider()

# --------------------------------------------------------
# Cluster Chart
# --------------------------------------------------------

st.subheader("Demand Cluster Visualization")

fig = px.scatter(

    pca_df,

    x="PC1",

    y="PC2",

    color="Demand Group",

    text=pca_df.index,

    title="K-Means Product Segmentation"

)

fig.update_traces(textposition="top center")

fig.update_layout(
    template="plotly_white"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------------
# Cluster Table
# --------------------------------------------------------

st.subheader("Product Demand Segments")

table = cluster_df.copy()

table = table.reset_index()

table = table[
    [
        "Sub-Category",
        "Total Sales",
        "Average Order Value",
        "Sales Growth",
        "Sales Volatility",
        "Demand Group"
    ]
]

st.dataframe(
    table,
    use_container_width=True
)

# --------------------------------------------------------
# Download
# --------------------------------------------------------

csv = table.to_csv(index=False)

st.download_button(

    label="⬇ Download Cluster Report",

    data=csv,

    file_name="product_segments.csv",

    mime="text/csv"

)