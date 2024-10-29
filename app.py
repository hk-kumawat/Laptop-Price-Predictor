import streamlit as st
import pickle
import numpy as np
import time

# Load the model and data
pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))

# CSS styling for enhanced UI effects, fixing overlay issues, and removing unwanted elements
st.markdown("""
    <style>
        /* Background animation for the whole page */
        body {
            background: linear-gradient(135deg, #e66465, #9198e5);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            color: #FFFFFF;
            font-family: Arial, sans-serif;
        }
        
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Title glow animation */
        .title {
            font-family: 'Courier New', Courier, monospace;
            color: #ffcf56;
            text-align: center;
            font-size: 3em;
            padding: 20px;
            animation: glow 1.5s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from { text-shadow: 0 0 10px #ffcf56, 0 0 20px #ffcf56; }
            to { text-shadow: 0 0 20px #ffcf56, 0 0 30px #ffcf56; }
        }

        /* Input block styling with hover effect */
        .stSelectbox:hover, .stNumberInput:hover, .stSlider:hover {
            position: relative;
            border: 1px solid #FFC857;
            cursor: pointer;
            transition: box-shadow 0.3s ease, transform 0.3s ease;
            transform: scale(1.05);
            box-shadow: 0px 0px 15px rgba(255, 200, 87, 0.5);
        }
        
        /* Animated label text overlay on hover */
        .stSelectbox:hover > label, .stNumberInput:hover > label, .stSlider:hover > label {
            color: #ffcf56;
            font-size: 1.1em;
            opacity: 0.9;
            transition: font-size 0.2s ease, opacity 0.2s ease;
            transform: scale(1.1);
        }

        /* Predict Button animation */
        .stButton > button {
            font-size: 20px;
            font-weight: bold;
            color: #FFFFFF;
            background: linear-gradient(45deg, #ff6b6b, #f09433);
            border: none;
            border-radius: 10px;
            padding: 15px 30px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
            overflow: hidden;
            cursor: pointer;
        }

        .stButton > button:hover {
            color: #000000;  /* Change text color to black on hover */
            box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.5);
        }

        /* Animate the button on click */
        .stButton > button:active {
            background: #FF4500;  /* Change color on click */
            animation: clickEffect 0.3s;
        }

        @keyframes clickEffect {
            0% { transform: scale(1); }
            50% { transform: scale(0.95); }
            100% { transform: scale(1); }
        }

        /* Prediction overlay animation */
        .prediction-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            color: #ffffff;
            font-size: 3em;
            display: flex;
            justify-content: center;
            align-items: center;
            animation: fadeIn 0.5s forwards;  /* Fade in effect */
        }

        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }

        @keyframes fadeOut {
            0% { opacity: 1; }
            100% { opacity: 0; display: none; }
        }

        /* Footer with subtle animation */
        .footer {
            font-size: 14px;
            color: #888888;
            text-align: center;
            padding: 10px;
            background-color: rgba(20, 30, 48, 0.7);
        }
    </style>
""", unsafe_allow_html=True)

# Display title with animation
st.markdown("<div class='title'>💻 Laptop Price Predictor 💻</div>", unsafe_allow_html=True)

# Inputs with enhanced hover effects
company = st.selectbox('🔹 Select Brand', df['Company'].unique())
type = st.selectbox('🔹 Laptop Type', df['TypeName'].unique())
ram = st.selectbox('🔹 RAM (in GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64])
weight = st.number_input('🔹 Weight of the Laptop (in kg)', step=0.1)
touchscreen = st.selectbox('🔹 Touchscreen', ['No', 'Yes'])
ips = st.selectbox('🔹 IPS Display', ['No', 'Yes'])
screen_size = st.slider('🔹 Screen Size (inches)', 10.0, 18.0, 13.0)
resolution = st.selectbox('🔹 Screen Resolution', [
    '1920x1080', '1366x768', '1600x900', '3840x2160', '3200x1800',
    '2880x1800', '2560x1600', '2560x1440', '2304x1440'
])
cpu = st.selectbox('🔹 CPU', df['Cpu brand'].unique())
hdd = st.selectbox('🔹 HDD (in GB)', [0, 128, 256, 512, 1024, 2048])
ssd = st.selectbox('🔹 SSD (in GB)', [0, 8, 128, 256, 512, 1024])
gpu = st.selectbox('🔹 GPU', df['Gpu brand'].unique())
os = st.selectbox('🔹 Operating System', df['os'].unique())

# Prediction Button and Prediction Overlay Animation
if st.button('✨ Predict Price ✨'):
    # Create a placeholder for the overlay
    overlay = st.empty()
    # Display prediction overlay animation
    overlay.markdown(f"<div class='prediction-overlay'>Predicting... Please wait...</div>", unsafe_allow_html=True)
    
    # Calculate prediction
    touchscreen = 1 if touchscreen == 'Yes' else 0
    ips = 1 if ips == 'Yes' else 0
    X_res, Y_res = map(int, resolution.split('x'))
    ppi = ((X_res ** 2) + (Y_res ** 2)) ** 0.5 / screen_size
    query = np.array([company, type, ram, weight, touchscreen, ips, ppi, cpu, hdd, ssd, gpu, os], dtype=object).reshape(1, 12)
    
    # Simulating a delay for demonstration purposes
    time.sleep(2)  # Simulate some processing time

    # Clear the overlay
    overlay.empty()
    
    # Display the prediction result
    st.success(f"✨ The estimated price of this laptop configuration is: ₹{int(np.exp(pipe.predict(query)[0])):,} 💸")

# Footer with subtle animation
st.markdown("<div class='footer'>Made with ❤️ by Harshal Kumawat | 2024</div>", unsafe_allow_html=True)



# Load the pickled DataFrame
try:
    with open('df.pkl', 'rb') as file:
        df = pickle.load(file)
except Exception as e:
    st.error(f"Error loading the DataFrame: {e}")
