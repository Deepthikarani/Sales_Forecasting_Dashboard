# 📈 Retail Sales Forecasting & Demand Analytics Dashboard

A complete **Data Science and Machine Learning project** that analyzes historical retail sales data, forecasts future sales, detects anomalies, segments products based on demand, and presents all insights through an interactive **Streamlit dashboard**.

---

## 📌 Project Overview

This project was developed to help retail businesses make **data-driven inventory and supply chain decisions**. It combines data preprocessing, exploratory data analysis (EDA), time series forecasting, anomaly detection, clustering, and dashboard deployment.

The solution provides:

- Historical sales analysis
- Sales forecasting for the next 3 months
- Weekly anomaly detection
- Product demand segmentation
- Interactive business dashboard

---

## 🚀 Features

### 📊 Sales Overview Dashboard

- Total Sales by Year
- Monthly Sales Trend
- Sales by Region
- Sales by Category
- Interactive Region & Category Filters
- KPI Cards

---

### 🔮 Forecast Explorer

- Forecast by Category or Region
- Select Forecast Horizon (1–3 Months)
- Prophet Forecast Visualization
- Forecast Confidence Interval
- MAE & RMSE Display

---

### 🚨 Anomaly Report

- Weekly Sales Trend
- Isolation Forest Anomaly Detection
- Highlighted Anomalous Weeks
- Downloadable Anomaly Report

---

### 📦 Product Demand Segmentation

- K-Means Clustering
- PCA Visualization
- Demand Group Classification
- Downloadable Cluster Report

---

# 📂 Project Structure

```
SalesForecasting/
│
├── Home.py
├── train.csv
├── requirements.txt
├── README.md
│
├── pages/
│   ├── 1_Sales_Overview.py
│   ├── 2_Forecast_Explorer.py
│   ├── 3_Anomaly_Report.py
│   └── 4_Product_Demand_Segments.py
│
└── charts/
│   ├── Average_Shipping_Time_by_Region.png
│   ├── Comparison_of_3-Month_Sales_Forecasts_Across_Categories.png
│   ├── Monthly_Sales_Across_Years.png
│   ├── Monthly_Sales_Heatmap.png
│   ├── Monthly_Sales_Trend.png
│   ├── Overall_Monthly_Sales_Trend_(2015-2018).png
│   ├── Plot_Trend_&_Seasonality_Componenets.png
│   ├── SARIMA_Forecast_(3 Months).png
│   ├── Time_Series_Decomposition_of_Monthly_Sales.png
│   ├── Total_Revenue_by_Product_Category.png
│   ├── Weekly_Sales_Anomaly_Detection_using_Rolling_Z-Score.png
│   ├── Weekly_Sales_Isolation_Forest_Anomalies.png
│   ├── Yearly_Sales_by_Region.png
```

---

# 📊 Dataset

Dataset used:

**Retail Superstore Sales Dataset**

Main attributes include:

- Order Date
- Ship Date
- Sales
- Category
- Sub-Category
- Region
- Product Name
- Customer Information

---

# 🛠️ Technologies Used

### Programming Language

- Python

### Libraries

- Pandas
- NumPy
- Matplotlib
- Plotly
- Scikit-learn
- Prophet
- Statsmodels
- XGBoost
- Joblib
- Streamlit

---

# 📈 Exploratory Data Analysis (EDA)

Performed:

- Missing Value Analysis
- Duplicate Detection
- Feature Engineering
- Monthly & Weekly Aggregation
- Sales Trend Analysis
- Category-wise Sales
- Region-wise Sales
- Seasonality Analysis

---

# 🤖 Machine Learning Models

## Time Series Forecasting

### SARIMA

Used for classical time series forecasting.

### Prophet (Best Model)

Used for:

- Trend Analysis
- Seasonality
- Future Forecasting

Forecast Horizon:

- 1 Month
- 2 Months
- 3 Months

### XGBoost Regressor

Converted time series into supervised learning using:

- Lag Features
- Rolling Mean
- Month
- Quarter
- Season

---

# 📉 Model Performance

| Model | MAE | RMSE | MAPE (%) |
|--------|------:|------:|------:|
| SARIMA | 20581.00 | 22191.27 | 21.94 |
| **Prophet** | **20250.79** | **22318.41** | **21.86** |
| XGBoost | 20607.15 | 22407.23 | 21.28 |

**Selected Model:** Prophet

---

# 🚨 Anomaly Detection

Methods Used:

- Isolation Forest
- Rolling Z-Score

Outputs:

- Weekly Sales Anomalies
- Interactive Visualization
- Downloadable Report

---

# 📦 Product Demand Segmentation

Technique Used:

- K-Means Clustering

Features:

- Total Sales
- Sales Growth
- Sales Volatility
- Average Order Value

Visualization:

- PCA Scatter Plot

Clusters:

- High Demand
- Medium Demand
- Low Demand

---

# 📊 Dashboard

Built using **Streamlit**.

Pages:

- 📊 Sales Overview
- 🔮 Forecast Explorer
- 🚨 Anomaly Report
- 📦 Product Demand Segments

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/Retail-Sales-Dashboard.git
```

Move into the project

```bash
cd Retail-Sales-Dashboard
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

# 🌐 Deployment

The application is deployed using **Streamlit Community Cloud**.

Live Demo:

```
https://your-streamlit-app.streamlit.app
```

---



# 📌 Business Insights

- Technology generated the highest revenue.
- West region showed the strongest sales growth.
- Prophet provided the best forecasting performance.
- Seasonal demand peaks occurred during year-end shopping periods.
- Demand segmentation helps optimize inventory management.

---

# 🎯 Future Improvements

- Real-time forecasting
- Database integration
- Automated model retraining
- Sales prediction by individual products
- Cloud database connectivity
- User authentication
- Interactive KPI monitoring

---

# 👩‍💻 Author

**Pokali Deepthikarani**

B.Tech Computer Science & Engineering

Aspiring Data Scientist | Machine Learning Engineer

GitHub: https://github.com/Deepthikarani

LinkedIn: https://linkedin.com/in/deepthikarani-pokali-5304182b8

---

# ⭐ If you found this project useful, consider giving it a star!
