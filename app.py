import streamlit as st
import joblib
import pandas as pd

# Load the trained model
model = joblib.load('model_pipeline_RF_2.joblib')

# Set page configuration for better design
st.set_page_config(page_title="Customer Churn Prediction", layout="wide")

# Title of the web app with a professional look and icons
st.markdown("""
    <style>
        .title {
            color: #0E4D92;
            font-size: 35px;
            font-weight: bold;
        }
        .subtitle {
            font-size: 18px;
            color: #555555;
        }
        .prediction-text {
            font-size: 20px;
            font-weight: bold;
            color: #2E8B57;
        }
        .footer-text {
            font-size: 12px;
            color: #888888;
        }
        .card {
            background-color: #F0F8FF;
            border-radius: 8px;
            padding: 20px;
            margin-top: 10px;
        }
        .icon {
            color: #0E4D92;
            font-size: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Title with icon
st.title("Customer Churn Prediction " + ":chart_with_upwards_trend:")

# Subtitle with a description and icon
st.markdown('<p class="subtitle">This web app predicts whether a customer will churn based on their details. <i class="fas fa-info-circle"></i></p>', unsafe_allow_html=True)

# Use an informative layout for the input fields
st.markdown("### Enter Customer Details: :memo:")

# Use expanders for input sections to organize the inputs visually
with st.expander("Customer Information :bust_in_silhouette:", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        credit_score = st.number_input('Credit Score', min_value=350, max_value=1000, value=600)
        age = st.number_input('Age', min_value=18, max_value=100, value=30)
        tenure = st.number_input('Tenure (years)', min_value=0, max_value=15, value=5)
        balance = st.number_input('Balance', min_value=0.0, value=50000.0)
        num_of_products = st.number_input('Number of Products', min_value=1, max_value=10, value=1)

    with col2:
        geography = st.selectbox('Geography', ['France', 'Germany', 'Spain'])
        gender = st.selectbox('Gender', ['Male', 'Female'])
        has_cr_card = st.selectbox('Has Credit Card', ['Yes', 'No'])
        is_active_member = st.selectbox('Is Active Member', ['Yes', 'No'])
        estimated_salary = st.number_input('Estimated Salary', min_value=0.0, value=50000.0)

# Prepare the input data for prediction
input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    'Geography': [geography],
    'Gender': [gender],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_member],
    'EstimatedSalary': [estimated_salary]
})

# Prediction and output display
if st.button('Predict', use_container_width=True):
    prediction = model.predict(input_data)
    if prediction[0] == "Yes":
        st.markdown('<p class="prediction-text">The customer is likely to churn. <i class="fas fa-exclamation-triangle"></i></p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="prediction-text">The customer is not likely to churn. <i class="fas fa-check-circle"></i></p>', unsafe_allow_html=True)

