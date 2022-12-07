import streamlit as st
import requests
import json
import pandas as pd
import pickle
import xgboost as xgb
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.models import model_from_json

# Title of the page
st.title("COVID-19 mRNA Vaccine Degradation Prediction")

#Loading up the Regression model we created
model = xgb.XGBRegressor()
model.load_model('./output/model_streamlit.json')

#Caching the model for faster loading
@st.cache

# Define the input
def predict(sequence, structure, predicted_loop_type):
    if sequence == 'A':
        sequence = 3
    elif sequence == 'C':
        sequence = 4
    elif sequence == 'G':
        sequence = 5
    elif sequence == 'U':
        sequence = 6

    if structure == '(':
        structure = 0
    elif structure == ')':
        structure = 1
    elif structure == '.':
        structure = 2
    
    if predicted_loop_type == 'B':
        predicted_loop_type = 7
    elif predicted_loop_type == 'E':
        predicted_loop_type = 8
    elif predicted_loop_type == 'H':
        predicted_loop_type = 9
    elif predicted_loop_type == 'I':
        predicted_loop_type = 10
    elif predicted_loop_type == 'M':
        predicted_loop_type = 11
    elif predicted_loop_type == 'S':
        predicted_loop_type = 12
    elif predicted_loop_type == 'X':
        predicted_loop_type = 13

    prediction = model.predict(pd.DataFrame([[sequence, structure, predicted_loop_type]], columns=['sequence', 'structure', 'predicted_loop_type']))
    return prediction

st.title('Predictor')
st.header('Select input:')
sequence = st.selectbox('Base:', ['A', 'C', 'G', 'U'])
structure = st.selectbox('Structure Type:', ['(', ')', '.'])
st.caption('.: Unpaired (: Paired ): Paired')
predicted_loop_type = st.selectbox('Loop Type:', ['B', 'E', 'H', 'I', 'M', 'S', 'X'])
st.caption('S: Stem M: Multiloop I: Internal loop B: Bulge H: Hairpin loop E: dangling End X: external loop')

if st.button('Predict'):
    reactivity = predict(sequence, structure, predicted_loop_type)
    st.success(f'The prediction of reactivity is {reactivity[0]:.4f}')
