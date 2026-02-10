import streamlit as st
import pickle
import pandas as pd
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Delivery Predictor",
    page_icon="🚚",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

body {
    background-color: #0e1117;
}

.main {
    background-color: #0e1117;
}

.result-card {
    background: #1c1f26;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.4);
    text-align: center;
    margin-top: 30px;
}

.big-text {
    font-size: 40px;
    font-weight: bold;
    color: #00ffcc;
}

.subtitle {
    font-size: 18px;
    color: #aaaaaa;
}

.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    font-size: 18px;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
}

.sidebar .sidebar-content {
    background-color: #161a23;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🚚 Food Delivery Time Predictor")
st.markdown("<p class='subtitle'>AI Powered Estimation using Optimized Random Forest Model</p>", unsafe_allow_html=True)

st.markdown("---")

# ---------------- LOAD MODEL ----------------
with open('optimized_rf_model.pkl', 'rb') as file:
    optimized_rf_model = pickle.load(file)

with open('label_encoders.pkl', 'rb') as file:
    label_encoders = pickle.load(file)

# ---------------- SIDEBAR INPUT ----------------
st.sidebar.header("📌 Delivery Details")

distance_km = st.sidebar.slider("Distance (km)", 0.1, 100.0, 10.0)
preparation_time_min = st.sidebar.slider("Preparation Time (min)", 1, 60, 20)
courier_experience_yrs = st.sidebar.slider("Courier Experience (yrs)", 0.0, 20.0, 2.0)

weather_selected = st.sidebar.selectbox("Weather", label_encoders['Weather'].classes_)
traffic_level_selected = st.sidebar.selectbox("Traffic Level", label_encoders['Traffic_Level'].classes_)
time_of_day_selected = st.sidebar.selectbox("Time of Day", label_encoders['Time_of_Day'].classes_)
vehicle_type_selected = st.sidebar.selectbox("Vehicle Type", label_encoders['Vehicle_Type'].classes_)

predict_btn = st.sidebar.button("🚀 Predict Now")

# ---------------- MAIN RESULT SECTION ----------------

if predict_btn:

    with st.spinner("Analyzing delivery conditions..."):
        time.sleep(1.5)

        weather_encoded = label_encoders['Weather'].transform([weather_selected])[0]
        traffic_level_encoded = label_encoders['Traffic_Level'].transform([traffic_level_selected])[0]
        time_of_day_encoded = label_encoders['Time_of_Day'].transform([time_of_day_selected])[0]
        vehicle_type_encoded = label_encoders['Vehicle_Type'].transform([vehicle_type_selected])[0]

        input_data = pd.DataFrame([[distance_km, weather_encoded, traffic_level_encoded,
                                    time_of_day_encoded, vehicle_type_encoded,
                                    preparation_time_min, courier_experience_yrs]],
                                  columns=['Distance_km', 'Weather', 'Traffic_Level',
                                           'Time_of_Day', 'Vehicle_Type',
                                           'Preparation_Time_min',
                                           'Courier_Experience_yrs'])

        prediction = optimized_rf_model.predict(input_data)

    st.markdown(f"""
    <div class='result-card'>
        <h2>⏱ Estimated Delivery Time</h2>
        <div class='big-text'>{prediction[0]:.2f} Minutes</div>
        <br>
    """, unsafe_allow_html=True)

    if prediction[0] < 30:
        st.success("⚡ Fast Delivery Expected")
    elif prediction[0] < 50:
        st.warning("⏳ Moderate Delivery Time")
    else:
        st.error("🚦 Heavy Traffic — Delay Possible")

    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown("""
    <div class='result-card'>
        <h2>🚀 Ready to Predict?</h2>
        <p>Fill the delivery details from the left panel and click <b>Predict Now</b>.</p>
    </div>
    """, unsafe_allow_html=True)
