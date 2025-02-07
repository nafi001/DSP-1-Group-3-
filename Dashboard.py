import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Obesity Risk Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
@st.cache_data
def load_data():
    return pd.read_csv('Churn_Modelling.csv')

df = load_data()

df['HasCrCard0'] = df['HasCrCard']
df['IsActiveMember0'] = df['IsActiveMember']
df['Exited0'] = df['Exited']

df['HasCrCard'] = df['HasCrCard0'].replace({1: 'Yes', 0: 'No'})
df['IsActiveMember'] = df['IsActiveMember0'].replace({1: 'Yes', 0: 'No'})
df['Exited'] = df['Exited0'].replace({1: 'Yes', 0: 'No'})
    

def sunburst_chart():
    """Create a sunburst chart for churn rate by Geography and Gender."""
    churn_data = df.groupby(['Geography', 'Gender'])['Exited0'].mean().reset_index()
    churn_data['ChurnRate'] = churn_data['Exited0'] * 100
    fig = px.sunburst(churn_data, path=['Geography', 'Gender'], values='ChurnRate',
                      color='ChurnRate', color_continuous_scale='Blues',  # Updated color scale
                      title="Sunburst Chart of Churn Rate by Geography and Gender",
                      labels={'ChurnRate': 'Churn Rate (%)'})
    return fig

def bar_chart_geography_gender():
    """Create a clustered bar chart for churn rate by Geography and Gender."""
    churn_data = df.groupby(['Geography', 'Gender'])['Exited0'].mean().reset_index()
    churn_data['ChurnRate'] = churn_data['Exited0'] * 100
    fig = px.bar(churn_data, x='Geography', y='ChurnRate', color='Gender',
                 barmode='group', title="Churn Rate by Geography and Gender",text_auto='.2f',
                 labels={'ChurnRate': 'Churn Rate (%)'},
                 color_discrete_sequence=px.colors.qualitative.Plotly)  # Updated color scale
    return fig

def churn_pie_chart():
    """Create a pie chart showing the churn distribution."""
    fig = px.pie(df, names='Exited', title='Churn Distribution',
                 color_discrete_sequence=px.colors.qualitative.Plotly)  # Updated color scale
    return fig

def churn_by_age_group():
    """Create a stacked bar chart for churn rate by age group."""
    age_bins = [18, 25, 35, 45, 55, 65, 75, 85, 95]
    age_labels = ['18-25', '25-35', '35-45', '45-55', '55-65', '65-75', '75-85', '85-95']
    df['AgeGroup'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)
    age_group_churn = df.groupby(['AgeGroup', 'Exited']).size().reset_index(name='Count')
    total_counts = df.groupby('AgeGroup').size().reset_index(name='TotalCount')
    age_group_churn = age_group_churn.merge(total_counts, on='AgeGroup')
    age_group_churn['Percentage'] = age_group_churn['Count'] / age_group_churn['TotalCount'] * 100
    fig = px.bar(age_group_churn, x='AgeGroup', y='Percentage', color='Exited',
                 title="Churn Rate by Age Group",
                 color_discrete_sequence=px.colors.qualitative.Plotly,  # Updated color scale
                 labels={'Exited': 'Churn Status', 'Percentage': 'Percentage'},
                 text_auto='.2f', barmode='stack')
    fig.update_layout(yaxis_tickformat='.2f%%')
    return fig

def churn_by_products():
    """Create a histogram for churn rate by the number of products."""
    fig = px.histogram(df, x='NumOfProducts', color='Exited', 
                       barmode='group', text_auto=True, 
                       title="Churn Rate by Number of Products",
                       color_discrete_sequence=px.colors.qualitative.Plotly,  # Updated color scale
                       histnorm='percent')
    return fig

def churn_vs_balance():
    """Create a density contour plot of churn rate by Age and Balance."""
    fig = px.density_contour(df, x='Age', y='Balance', color='Exited',
                             title="Age vs. Balance Density with Churn",
                             color_discrete_sequence=px.colors.qualitative.Plotly,  # Updated color scale
                             labels={'Exited': 'Churn Status'})
    return fig

def churn_by_balance():
    """Create a bar chart for churn rate by Zero vs. Non-Zero Balance."""
    df['ZeroBalance'] = df['Balance'].apply(lambda x: 1 if x == 0 else 0)
    balance_churn_data = df.groupby(['Exited', 'ZeroBalance']).size().reset_index(name='Count')
    balance_churn_data['Percentage'] = balance_churn_data.groupby('Exited')['Count'].transform(lambda x: x / x.sum() * 100)
    balance_churn_data['Exited'] = balance_churn_data['Exited'].map({'No': 'No', 'Yes': 'Yes'})
    balance_churn_data['ZeroBalance'] = balance_churn_data['ZeroBalance'].map({0: 'Non-Zero Balance', 1: 'Zero Balance'})
    balance_churn_data['PercentageText'] = balance_churn_data['Percentage'].apply(lambda x: f'{x:.2f}%')
    fig = px.bar(balance_churn_data, x='Exited', y='Percentage', color='ZeroBalance',
                 barmode='group', title="Churn Rate by Zero vs Non-Zero Balance",
                 labels={'Percentage': 'Percentage of Customers'}, text='PercentageText',
                 color_discrete_sequence=px.colors.qualitative.Plotly)  # Updated color scale
    fig.update_layout(xaxis_title="Churn Status", yaxis_title="Percentage of Customers")
    return fig



def churn_by_tenure():
    churn_data = df.groupby('Tenure')['Exited0'].agg(['count', 'sum']).reset_index()
    churn_data['Churn_Rate'] = churn_data['sum'] / churn_data['count']  # Churn Rate = Churned / Total

    # Line Chart
    fig = px.line(churn_data, x='Tenure', y='Churn_Rate', 
              title="Churn Rate vs. Tenure",
              labels={'Churn_Rate': 'Churn Rate', 'Tenure': 'Tenure (Years)'},
              markers=True)
    return fig

# ============================================
# Dashboard Layout
# ============================================
# ============================================
# Dashboard Layout - Customer Churn Analytics
# ============================================

# Row 1: Key Performance Indicators
st.header("📊 Key Performance Indicators")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Customers", f"{len(df):,}")
with col2:
    churn_rate = df['Exited0'].mean() * 100
    st.metric("Overall Churn Rate", f"{churn_rate:.1f}%")
with col3:
    st.metric("Average Credit Score of Churned Customers", f"${df[df["Exited0"] == 1]["CreditScore"].mean():,.2f}")

# Row 2: Churn Overview
st.header("🔍 Churn Overview")
col1, col2 = st.columns([2, 3])
with col1:
    st.plotly_chart(churn_pie_chart(), use_container_width=True)
with col2:
    st.plotly_chart(churn_by_tenure(), use_container_width=True)

# Row 3: Demographic Analysis


# Row 4: Customer Profile Analysis
st.header("📈 Customer Profile Insights")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(churn_by_age_group(), use_container_width=True)
with col2:
    st.plotly_chart(churn_vs_balance(), use_container_width=True)

# Row 5: Product & Financial Analysis
st.header("💳 Product & Financial Patterns")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(churn_by_products(), use_container_width=True)
with col2:
    st.plotly_chart(churn_by_balance(), use_container_width=True)

st.header("👥 Demographic Breakdown")
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(sunburst_chart(), use_container_width=True)
with col2:
    st.plotly_chart(bar_chart_geography_gender(), use_container_width=True)
    

st.header("📊 Churn Metrics")
col4, col5= st.columns(2)

with col4:
    avg_tenure_churned = df[df["Exited0"] == 1]["Tenure"].mean()
    avg_tenure_non_churned = df[df["Exited0"] == 0]["Tenure"].mean()
    st.metric("Avg Tenure (Churned)", f"{avg_tenure_churned:.1f} years")
    st.metric("Avg Tenure (Non-Churned)", f"{avg_tenure_non_churned:.1f} years")

with col5:
    avg_balance_churned = df[df["Exited0"] == 1]["Balance"].mean()
    avg_balance_non_churned = df[df["Exited0"] == 0]["Balance"].mean()
    st.metric("Avg Balance (Churned)", f"${avg_balance_churned:,.0f}")
    st.metric("Avg Balance (Non-Churned)", f"${avg_balance_non_churned:,.0f}")





# Row 6: Additional Metrics
st.header("📌 Supplementary Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    active_rate = df['IsActiveMember0'].mean() * 100
    st.metric("Active Members", f"{active_rate:.1f}%")

with col2:
    credit_card_holders = df['HasCrCard0'].mean() * 100
    st.metric("Credit Card Holders", f"{credit_card_holders:.1f}%")

with col3:
    avg_products = df['NumOfProducts'].mean()
    st.metric("Avg Products/Customer", f"{avg_products:.1f}")



