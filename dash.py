import streamlit as st
import pandas as pd
import plotly.express as px

# Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv("customer_churn.csv")  # Replace with actual dataset path
    return df

df = load_data()

# Streamlit Page Config
st.set_page_config(page_title="Customer Churn Dashboard", layout="wide")

# Sidebar - Filters
st.sidebar.header("Filter Options")
geography = st.sidebar.multiselect("Select Geography", df["Geography"].unique(), default=df["Geography"].unique())
gender = st.sidebar.multiselect("Select Gender", df["Gender"].unique(), default=df["Gender"].unique())
tenure_range = st.sidebar.slider("Select Tenure Range", min_value=int(df["Tenure"].min()), 
                                 max_value=int(df["Tenure"].max()), value=(df["Tenure"].min(), df["Tenure"].max()))

# Apply Filters
filtered_df = df[(df["Geography"].isin(geography)) & (df["Gender"].isin(gender)) & 
                 (df["Tenure"].between(tenure_range[0], tenure_range[1]))]

# Main Dashboard Layout
st.title("📊 Customer Churn Analysis Dashboard")

# Churn Distribution
st.subheader("Churn Distribution")
fig1 = px.pie(df, names="Exited", title="Churn vs. Retained Customers", labels={"Exited": "Churned"})
st.plotly_chart(fig1, use_container_width=True)

# Age vs. Churn
st.subheader("Age Impact on Churn")
fig2 = px.histogram(filtered_df, x="Age", color="Exited", barmode="overlay", title="Age Distribution by Churn")
st.plotly_chart(fig2, use_container_width=True)

# Credit Score vs. Churn
st.subheader("Credit Score vs. Churn")
fig3 = px.box(filtered_df, x="Exited", y="CreditScore", color="Exited", title="Credit Score Distribution by Churn")
st.plotly_chart(fig3, use_container_width=True)

# Balance & Salary Influence
col1, col2 = st.columns(2)

with col1:
    st.subheader("Balance Influence on Churn")
    fig4 = px.box(filtered_df, x="Exited", y="Balance", color="Exited", title="Balance vs. Churn")
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    st.subheader("Estimated Salary vs. Churn")
    fig5 = px.histogram(filtered_df, x="EstimatedSalary", color="Exited", title="Salary Distribution by Churn")
    st.plotly_chart(fig5, use_container_width=True)

# Geographical Influence
st.subheader("Churn Rate by Geography")
fig6 = px.bar(filtered_df.groupby("Geography")["Exited"].mean().reset_index(), x="Geography", y="Exited", 
              title="Churn Rate by Country", color="Geography")
st.plotly_chart(fig6, use_container_width=True)

# Summary
st.write("### Key Insights:")
st.write("""
- Older customers tend to churn more/less (depending on data visualization).
- Customers with lower credit scores may have higher churn rates.
- Customers with high balances may have lower churn probability.
- Churn varies across different geographies.
""")

st.write("---")
st.write("📌 **Developed by [Your Name]** | Powered by Streamlit & Plotly")
