import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset (assuming df is your DataFrame)
df = pd.read_csv('Churn_Modelling.csv')  # Adjust file path accordingly







# Load Data
@st.cache_data
def load_data():
    df['HasCrCard0'] = df['HasCrCard']
    df['IsActiveMember0'] = df['IsActiveMember']
    df['Exited0'] = df['Exited']

    df['HasCrCard'] = df['HasCrCard0'].replace({1: 'Yes', 0: 'No'})
    df['IsActiveMember'] = df['IsActiveMember0'].replace({1: 'Yes', 0: 'No'})
    df['Exited'] = df['Exited0'].replace({1: 'Yes', 0: 'No'})
    
    return df


df = load_data()

# Sidebar Filters
st.sidebar.title("🔍 Filters")
selected_geography = st.sidebar.multiselect("🌍 Select Geography:", df["Geography"].unique(), default=df["Geography"].unique())
selected_gender = st.sidebar.multiselect("👤 Select Gender:", df["Gender"].unique(), default=df["Gender"].unique())
selected_products = st.sidebar.multiselect("📦 Number of Products:", df["NumOfProducts"].unique(), default=df["NumOfProducts"].unique())
selected_active_status = st.sidebar.radio("✅ Active Membership:", ["All", "Yes", "No"])

# Apply Filters
filtered_df = df[(df["Geography"].isin(selected_geography)) & 
                 (df["Gender"].isin(selected_gender)) &
                 (df["NumOfProducts"].isin(selected_products))]

if selected_active_status != "All":
    filtered_df = filtered_df[filtered_df["IsActiveMember"] == selected_active_status]

# KPIs Section
st.title("📊 Customer Churn Analysis Dashboard")
st.markdown("### 🏆 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

# KPI Calculations
total_customers = len(filtered_df)
total_churned = filtered_df["Exited0"].sum()
overall_churn_rate = (total_churned / total_customers) * 100

avg_age_churned = filtered_df[filtered_df["Exited"] == "Yes"]["Age"].mean()
avg_credit_score_churned = filtered_df[filtered_df["Exited"] == "Yes"]["CreditScore"].mean()
prop_active_churned = filtered_df[(filtered_df["IsActiveMember"] == "Yes") & (filtered_df["Exited"] == "Yes")].shape[0] / filtered_df[filtered_df["IsActiveMember"] == "Yes"].shape[0] * 100

col1.metric("📉 Overall Churn Rate", f"{overall_churn_rate:.2f}%")
col2.metric("👴 Avg Age of Churned Customers", f"{avg_age_churned:.1f} years")
col3.metric("📊 Avg Credit Score of Churned", f"{avg_credit_score_churned:.0f}")

st.markdown("---")

# 📍 Geographical Trends
st.subheader("📍 Geographical Trends")

churn_by_country = filtered_df.groupby("Geography")["Exited0"].mean().reset_index()
churn_by_country["Churn Rate (%)"] = churn_by_country["Exited0"] * 100

fig_geo = px.bar(churn_by_country, x="Geography", y="Churn Rate (%)", title="🌍 Churn Rate by Country", text_auto='.2f')
st.plotly_chart(fig_geo)

# 📊 Churn by Age Group
st.subheader("📊 Churn Rate by Age Group")

age_bins = [18, 25, 35, 45, 55, 65, 75, 85, 95]
age_labels = ['18-25', '25-35', '35-45', '45-55', '55-65', '65-75', '75-85', '85-95']
filtered_df['AgeGroup'] = pd.cut(filtered_df['Age'], bins=age_bins, labels=age_labels, right=False)

age_group_churn = filtered_df.groupby(['AgeGroup', 'Exited']).size().reset_index(name='Count')
total_counts = filtered_df.groupby('AgeGroup').size().reset_index(name='TotalCount')
age_group_churn = age_group_churn.merge(total_counts, on='AgeGroup')
age_group_churn['Percentage'] = age_group_churn['Count'] / age_group_churn['TotalCount'] * 100

fig_age = px.bar(age_group_churn, x="AgeGroup", y="Percentage", color="Exited",
                 title="👶🧓 Churn Rate by Age Group", text_auto='.2f', barmode="stack")
st.plotly_chart(fig_age)

# 📦 Churn by Number of Products
st.subheader("📦 Churn Rate by Number of Products")

fig_products = px.histogram(filtered_df, x="NumOfProducts", color="Exited", barmode="group", text_auto=True, 
                            title="📦 Churn Rate by Number of Products", histnorm='percent')
st.plotly_chart(fig_products)

# 💰 Churn by Balance (Zero vs Non-Zero)
st.subheader("💰 Churn Rate by Balance")

filtered_df['ZeroBalance'] = filtered_df['Balance'].apply(lambda x: "Zero" if x == 0 else "Non-Zero")
balance_churn_data = filtered_df.groupby(['Exited', 'ZeroBalance']).size().reset_index(name='Count')
balance_churn_data['Percentage'] = balance_churn_data.groupby('Exited')['Count'].transform(lambda x: x / x.sum() * 100)
balance_churn_data['PercentageText'] = balance_churn_data['Percentage'].apply(lambda x: f'{x:.2f}%')

fig_balance = px.bar(balance_churn_data, x="Exited", y="Percentage", color="ZeroBalance",
                     barmode="group", title="💰 Churn Rate by Zero vs Non-Zero Balance", text="PercentageText")
st.plotly_chart(fig_balance)

# ⏳ Churn by Tenure
st.subheader("⏳ Churn Rate vs Tenure")

churn_by_tenure = filtered_df.groupby("Tenure")["Exited0"].agg(["count", "sum"]).reset_index()
churn_by_tenure["Churn Rate"] = (churn_by_tenure["sum"] / churn_by_tenure["count"]) * 100

fig_tenure = px.line(churn_by_tenure, x="Tenure", y="Churn Rate", markers=True, 
                     title="⏳ Churn Rate by Tenure")
st.plotly_chart(fig_tenure)

# 🏦 Churn by Active Membership
st.subheader("🏦 Churn Rate by Active Membership")

fig_active = px.pie(filtered_df, names="IsActiveMember", title="🏦 Churn Distribution by Active Membership")
st.plotly_chart(fig_active)

# 📊 Density Plot - Age vs Balance
st.subheader("📊 Age vs. Balance Density")

fig_density = px.density_contour(filtered_df, x="Age", y="Balance", color="Exited",
                                 title="📊 Age vs. Balance Density with Churn")
st.plotly_chart(fig_density)

st.markdown("---")
st.write("📢 **Insights:**\n- Customers with 0 balance have higher churn rates.\n- Older customers tend to have a lower churn rate.\n- Customers with more than 2 products have lower churn.")


                 labels={'Percentage': 'Percentage of Customers'}, text='PercentageText')
    fig.update_layout(xaxis_title="Churn Status", yaxis_title="Percentage of Customers")
    return fig
