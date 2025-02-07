import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset (assuming df is your DataFrame)
df = pd.read_csv('Churn_Modelling.csv')  # Adjust file path accordingly

# Convert categorical columns back to numeric for analysis
df['Exited0'] = df['Exited'].replace({'No': 0, 'Yes': 1})
df['IsActiveMember0'] = df['IsActiveMember'].replace({'No': 0, 'Yes': 1})

def calculate_kpis(df):
    total_customers = len(df)
    total_exited = df['Exited0'].sum()
    churn_rate = (total_exited / total_customers) * 100
    avg_age_churned = df[df['Exited0'] == 1]['Age'].mean()
    avg_credit_churned = df[df['Exited0'] == 1]['CreditScore'].mean()
    active_churn_proportion = df[df['Exited0'] == 1]['IsActiveMember0'].mean() * 100
    avg_tenure_churned = df[df['Exited0'] == 1]['Tenure'].mean()
    avg_tenure_not_churned = df[df['Exited0'] == 0]['Tenure'].mean()
    avg_balance_churned = df[df['Exited0'] == 1]['Balance'].mean()
    avg_balance_not_churned = df[df['Exited0'] == 0]['Balance'].mean()
    
    return {
        'Overall Churn Rate': churn_rate,
        'Avg Age of Churned': avg_age_churned,
        'Avg Credit Score of Churned': avg_credit_churned,
        'Proportion of Active Churned': active_churn_proportion,
        'Avg Tenure (Churned)': avg_tenure_churned,
        'Avg Tenure (Not Churned)': avg_tenure_not_churned,
        'Avg Balance (Churned)': avg_balance_churned,
        'Avg Balance (Not Churned)': avg_balance_not_churned
    }

# Sidebar
st.sidebar.title("Customer Churn Analysis")
segment = st.sidebar.radio("Select Analysis Category", [
    "KPIs", "Demographics", "Banking Behavior", "Product Engagement"
])

# KPIs
kpis = calculate_kpis(df)
if segment == "KPIs":
    st.title("Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Churn Rate", f"{kpis['Overall Churn Rate']:.2f}%")
    col2.metric("Avg Age of Churned", f"{kpis['Avg Age of Churned']:.1f} years")
    col3.metric("Avg Credit Score (Churned)", f"{kpis['Avg Credit Score of Churned']:.1f}")
    col1.metric("Active Members Churned", f"{kpis['Proportion of Active Churned']:.2f}%")
    col2.metric("Avg Tenure (Churned)", f"{kpis['Avg Tenure (Churned'):.1f} years")
    col3.metric("Avg Balance (Churned)", f"${kpis['Avg Balance (Churned)']:.2f}")

# Demographics Analysis
elif segment == "Demographics":
    st.title("Churn by Geography & Gender")
    churn_data = df.groupby(['Geography', 'Gender'])['Exited0'].mean().reset_index()
    churn_data['ChurnRate'] = churn_data['Exited0'] * 100
    fig1 = px.sunburst(churn_data, path=['Geography', 'Gender'], values='ChurnRate',
                        color='ChurnRate', color_continuous_scale='RdBu',
                        title="Churn Rate by Geography & Gender")
    st.plotly_chart(fig1)
    
    fig2 = px.bar(churn_data, x='Geography', y='ChurnRate', color='Gender',
                  title="Churn Rate by Geography and Gender", barmode='group')
    st.plotly_chart(fig2)

# Banking Behavior
elif segment == "Banking Behavior":
    st.title("Banking Behavior and Churn")
    
    # Churn by Number of Products
    fig3 = px.histogram(df, x='NumOfProducts', color='Exited',
                        barmode='group', title="Churn Rate by Number of Products")
    st.plotly_chart(fig3)
    
    # Churn Rate by Balance
    fig4 = px.density_contour(df, x='Age', y='Balance', color='Exited',
                              title="Age vs. Balance Density with Churn")
    st.plotly_chart(fig4)
    
    # Churn Rate vs Tenure
    tenure_churn = df.groupby('Tenure')['Exited0'].mean().reset_index()
    fig5 = px.line(tenure_churn, x='Tenure', y='Exited0',
                   title="Churn Rate vs Tenure", markers=True)
    st.plotly_chart(fig5)

# Product Engagement
elif segment == "Product Engagement":
    st.title("Product Engagement and Churn")
    
    # Churn Rate by Age Group
    age_bins = [18, 25, 35, 45, 55, 65, 75, 85, 95]
    age_labels = ['18-25', '25-35', '35-45', '45-55', '55-65', '65-75', '75-85', '85-95']
    df['AgeGroup'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)
    age_group_churn = df.groupby(['AgeGroup', 'Exited']).size().reset_index(name='Count')
    fig6 = px.bar(age_group_churn, x='AgeGroup', y='Count', color='Exited',
                  title="Churn Rate by Age Group", barmode='stack')
    st.plotly_chart(fig6)
    
    # Churn Rate by Zero vs Non-Zero Balance
    df['ZeroBalance'] = df['Balance'].apply(lambda x: 1 if x == 0 else 0)
    balance_churn = df.groupby(['Exited', 'ZeroBalance']).size().reset_index(name='Count')
    balance_churn['Exited'] = balance_churn['Exited'].map({'No': 'No', 'Yes': 'Yes'})
    balance_churn['ZeroBalance'] = balance_churn['ZeroBalance'].map({0: 'Non-Zero Balance', 1: 'Zero Balance'})
    fig7 = px.bar(balance_churn, x='Exited', y='Count', color='ZeroBalance',
                  barmode='group', title="Churn by Zero vs Non-Zero Balance")
    st.plotly_chart(fig7)

st.sidebar.info("This dashboard provides insights into customer churn trends and factors influencing customer exit.")

