import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset (assuming df is your DataFrame)
df = pd.read_csv('Churn_Modelling.csv')  # Adjust file path accordingly

# Data Preprocessing (converting binary columns to 'Yes'/'No' labels)
df['HasCrCard0'] = df['HasCrCard'].replace({1: 'Yes', 0: 'No'})
df['IsActiveMember0'] = df['IsActiveMember'].replace({1: 'Yes', 0: 'No'})
df['Exited0'] = df['Exited'].replace({1: 'Yes', 0: 'No'})

# Overall Churn Rate
total_customers = len(df)
total_exited = df['Exited'].sum()
overall_churn_rate = (total_exited / total_customers) * 100

# Churn Rate by Country
churn_by_country = df.groupby('Geography')['Exited'].mean().reset_index()
churn_by_country['ChurnRate'] = churn_by_country['Exited'] * 100

# Average Age of Churned Customers
avg_age_churned = df[df['Exited0'] == 'Yes']['Age'].mean()

# Average Credit Score of Churned Customers
avg_credit_score_churned = df[df['Exited0'] == 'Yes']['CreditScore'].mean()

# Proportion of Active Members Who Churned
active_members = df[df['IsActiveMember0'] == 'Yes']
proportion_active_churned = (active_members['Exited0'].sum() / len(active_members)) * 100

# Average Tenure of Churned vs Non-Churned Customers
avg_tenure_churned = df[df['Exited0'] == 'Yes']['Tenure'].mean()
avg_tenure_non_churned = df[df['Exited0'] == 'No']['Tenure'].mean()

# Average Balance of Churned vs Non-Churned Customers
avg_balance_churned = df[df['Exited0'] == 'Yes']['Balance'].mean()
avg_balance_non_churned = df[df['Exited0'] == 'No']['Balance'].mean()

# Churn Rate by Number of Products
churn_by_products = df.groupby('NumOfProducts')['Exited0'].mean().reset_index()
churn_by_products['ChurnRate'] = churn_by_products['Exited0'] * 100

# Streamlit Dashboard Layout
st.title('Customer Churn Analysis Dashboard')

# Section 1: KPIs
st.subheader('Key Performance Indicators (KPIs)')
col1, col2 = st.columns(2)
with col1:
    st.metric('Overall Churn Rate (%)', f"{overall_churn_rate:.2f}")
    st.metric('Average Age of Churned Customers', f"{avg_age_churned:.2f} years")
    st.metric('Average Credit Score of Churned Customers', f"{avg_credit_score_churned:.2f}")
    st.metric('Proportion of Active Members Who Churned (%)', f"{proportion_active_churned:.2f}")
with col2:
    st.metric('Average Tenure (Churned)', f"{avg_tenure_churned:.2f} years")
    st.metric('Average Tenure (Non-Churned)', f"{avg_tenure_non_churned:.2f} years")
    st.metric('Average Balance (Churned)', f"${avg_balance_churned:,.2f}")
    st.metric('Average Balance (Non-Churned)', f"${avg_balance_non_churned:,.2f}")

# Section 2: Churn Rate by Geography and Gender
st.subheader('Churn Rate by Geography and Gender')
churn_by_geography_gender = df.groupby(['Geography', 'Gender'])['Exited0'].mean().reset_index()
churn_by_geography_gender['ChurnRate'] = churn_by_geography_gender['Exited0'] * 100
fig_geo_gender = px.sunburst(churn_by_geography_gender, 
                            path=['Geography', 'Gender'], 
                            values='ChurnRate', 
                            color='ChurnRate', 
                            color_continuous_scale='RdBu', 
                            title="Churn Rate by Geography and Gender")
st.plotly_chart(fig_geo_gender)

# Section 3: Churn Rate by Number of Products
st.subheader('Churn Rate by Number of Products')
fig_products = px.bar(churn_by_products, 
                      x='NumOfProducts', 
                      y='ChurnRate', 
                      title="Churn Rate by Number of Products", 
                      labels={'ChurnRate': 'Churn Rate (%)'})
st.plotly_chart(fig_products)

# Section 4: Churn Rate by Age Group
st.subheader('Churn Rate by Age Group')
age_bins = [18, 25, 35, 45, 55, 65, 75, 85, 95]
age_labels = ['18-25', '25-35', '35-45', '45-55', '55-65', '65-75', '75-85', '85-95']
df['AgeGroup'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)

age_group_churn = df.groupby(['AgeGroup', 'Exited0']).size().reset_index(name='Count')
total_counts = df.groupby('AgeGroup').size().reset_index(name='TotalCount')
age_group_churn = age_group_churn.merge(total_counts, on='AgeGroup')
age_group_churn['Percentage'] = age_group_churn['Count'] / age_group_churn['TotalCount'] * 100

fig_age_group = px.bar(age_group_churn, 
                       x='AgeGroup', 
                       y='Percentage', 
                       color='Exited0', 
                       title="Churn Rate by Age Group", 
                       labels={'Percentage': 'Percentage of Customers'}, 
                       text_auto='.2f', barmode='stack')
fig_age_group.update_layout(yaxis_tickformat='.2f%%')
st.plotly_chart(fig_age_group)

# Section 5: Customer Churn Distribution
st.subheader('Churn Distribution')
fig_churn_dist = px.pie(df, names='Exited0', title='Customer Churn Distribution')
st.plotly_chart(fig_churn_dist)

# Add additional sections or plots as needed

