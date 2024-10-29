import streamlit as st
import pickle
import pandas as pd
import numpy as np
import time

# Load the model and data
pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))

# Display title
st.title('Laptop Price Predictor')

# Inputs
company = st.selectbox('Select Brand', df['Company'].unique())
type = st.selectbox('Laptop Type', df['TypeName'].unique())
ram = st.selectbox('RAM (in GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64])
weight = st.number_input('Weight of the Laptop (in kg)', step=0.1)
touchscreen = st.selectbox('Touchscreen', ['No', 'Yes'])
ips = st.selectbox('IPS Display', ['No', 'Yes'])
screen_size = st.slider('Screen Size (inches)', 10.0, 18.0, 13.0)
resolution = st.selectbox('Screen Resolution', [
    '1920x1080', '1366x768', '1600x900', '3840x2160', '3200x1800',
    '2880x1800', '2560x1600', '2560x1440', '2304x1440'])
cpu = st.selectbox('CPU', df['Cpu brand'].unique())
hdd = st.selectbox('HDD (in GB)', [0, 128, 256, 512, 1024, 2048])
ssd = st.selectbox('SSD (in GB)', [0, 8, 128, 256, 512, 1024])
gpu = st.selectbox('GPU', df['Gpu brand'].unique())
os = st.selectbox('Operating System', df['os'].unique())

# Prediction Button
if st.button('Predict Price'):
    touchscreen = 1 if touchscreen == 'Yes' else 0
    ips = 1 if ips == 'Yes' else 0
    X_res, Y_res = map(int, resolution.split('x'))
    ppi = ((X_res ** 2) + (Y_res ** 2)) ** 0.5 / screen_size
    query = np.array([company, type, ram, weight, touchscreen, ips, ppi, cpu, hdd, ssd, gpu, os])
    query = np.array(query, dtype=object).reshape(1, 12)
    
    # Simulating a delay for demonstration purposes
    time.sleep(2)
    
    # Display the prediction result
    st.success(f"The estimated price of this laptop configuration is: ₹{int(np.exp(pipe.predict(query)[0])):,}")

# Load the pickled DataFrame
try:
    with open('df.pkl', 'rb') as file:
        df = pickle.load(file)
except Exception as e:
    st.error(f"Error loading the DataFrame: {e}")
