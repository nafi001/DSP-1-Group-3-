import streamlit as st
import joblib
import numpy as np

# Load the trained model
model = joblib.load('model.joblib')

# Title of the web app
st.title('Customer Churn Prediction')

# Subtitle of the web app
st.write('This web app predicts whether a customer will churn based on their details.')

# Input fields
credit_score = st.number_input('Credit Score', min_value=350, max_value=850, value=600)
geography = st.selectbox('Geography', ['France', 'Germany', 'Spain'])
gender = st.selectbox('Gender', ['Male', 'Female'])
age = st.number_input('Age', min_value=18, max_value=100, value=30)
tenure = st.number_input('Tenure (years)', min_value=0, max_value=10, value=5)
balance = st.number_input('Balance', min_value=0.0, value=50000.0)
num_of_products = st.number_input('Number of Products', min_value=1, max_value=4, value=1)
has_cr_card = st.selectbox('Has Credit Card', ['Yes', 'No'])
is_active_member = st.selectbox('Is Active Member', ['Yes', 'No'])
estimated_salary = st.number_input('Estimated Salary', min_value=0.0, value=50000.0)

# Convert categorical variables to numerical
geography_dict = {'France': 0, 'Germany': 1, 'Spain': 2}
gender_dict = {'Male': 0, 'Female': 1}
has_cr_card_dict = {'Yes': 1, 'No': 0}
is_active_member_dict = {'Yes': 1, 'No': 0}

geography = geography_dict[geography]
gender = gender_dict[gender]
has_cr_card = has_cr_card_dict[has_cr_card]
is_active_member = is_active_member_dict[is_active_member]

# Prepare the input data for prediction
input_data = np.array([[credit_score, geography, gender, age, tenure, balance, num_of_products, has_cr_card, is_active_member, estimated_salary]])

# Make prediction
if st.button('Predict'):
    prediction = model.predict(input_data)
    if prediction[0] == 1:
        st.write('The customer is likely to churn.')
    else:
        st.write('The customer is not likely to churn.')

# Footer
st.write('---')
st.write('Developed by [Your Name]')
