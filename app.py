import streamlit as st
import numpy as np
import pickle

# Page config
st.set_page_config(
    page_title="❤️ Cardiovascular Disease Prediction",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Pink theme CSS - Clean & Minimal
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ff69b4 0%, #ff1493 50%, #c71585 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .input-group {
        background: linear-gradient(135deg, rgba(255,105,180,0.1) 0%, rgba(255,20,147,0.1) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid rgba(255,105,180,0.3);
        margin: 1rem 0;
    }
    .pink-accent {
        color: #ff69b4;
        font-weight: 600;
    }
    .bmi-card {
        background: linear-gradient(135deg, #ffb6c1, #ff69b4);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
    }
    .result-high {
        background: linear-gradient(135deg, #ff1493, #c71585);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    .result-low {
        background: linear-gradient(135deg, #ff69b4, #ffb6c1);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    .stSlider > div > div > div > div { background-color: #ff69b4 !important; }
    .stSelectbox > div > div > div { color: #ff1493; }
</style>
""", unsafe_allow_html=True)

# Load model & scaler (UNCHANGED)
with open("model/logistic_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("model/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# Header
st.markdown('<h1 class="main-header">❤️ Cardio Risk Predictor</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ff69b4; font-size: 1.2rem;'>Enter your details for instant risk assessment</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 💕 Quick Info")
    st.markdown("**<span class='pink-accent'>What we analyze:</span>**", unsafe_allow_html=True)
    st.markdown("- 👤 Age & BMI")
    st.markdown("- 🩺 Blood Pressure")
    st.markdown("- 🧪 Cholesterol/Glucose") 
    st.markdown("- 🚬 Lifestyle habits")

# Clean Input Layout - NO BIG BOXES
st.markdown("### 👤 Personal Details")
col1, col2 = st.columns(2)
with col1:
    age_years = st.slider("🎂 Age (years)", 18, 100, 45)
with col2:
    gender = st.selectbox("👩‍🦰 Gender", ["Female", "Male"])

col1, col2 = st.columns(2)
with col1:
    height = st.slider("📏 Height (cm)", 120, 220, 165)
with col2:
    weight = st.slider("⚖️ Weight (kg)", 30, 200, 70)

# Health Metrics
st.markdown("### 🩺 Health Metrics")
col1, col2 = st.columns(2)
with col1:
    ap_hi = st.slider("📈 Systolic BP", 80, 250, 120)
    ap_lo = st.slider("📉 Diastolic BP", 40, 150, 80)
with col2:
    cholesterol = st.selectbox("🧪 Cholesterol", ["Normal", "Above Normal", "Well Above Normal"])
    gluc = st.selectbox("🍬 Glucose", ["Normal", "Above Normal", "Well Above Normal"])

# Lifestyle - Clean row
st.markdown("### 🚀 Lifestyle")
lifestyle_col1, lifestyle_col2, lifestyle_col3 = st.columns(3)
smoke = lifestyle_col1.radio("🚭 Smoking", ["No", "Yes"], horizontal=True)
alco = lifestyle_col2.radio("🍺 Alcohol", ["No", "Yes"], horizontal=True)
active = lifestyle_col3.radio("🏃 Active", ["No", "Yes"], horizontal=True)

# BMI Display
BMI = weight / ((height / 100) ** 2)
col1, col2 = st.columns([3, 1])
with col2:
    st.markdown(f'''
    <div class="bmi-card">
        <h3>📏 BMI</h3>
        <h2>{BMI:.1f}</h2>
    </div>
    ''', unsafe_allow_html=True)

# ENCODE (UNCHANGED)
gender = 1 if gender == "Male" else 0
cholesterol = ["Normal", "Above Normal", "Well Above Normal"].index(cholesterol)
gluc = ["Normal", "Above Normal", "Well Above Normal"].index(gluc)
smoke = 1 if smoke == "Yes" else 0
alco = 1 if alco == "Yes" else 0
active = 1 if active == "Yes" else 0

# Predict Button
if st.button("💖 **Predict My Risk**", type="primary", use_container_width=True):
    with st.spinner("✨ Analyzing..."):
        numeric_features = np.array([[age_years, height, weight, ap_hi, ap_lo, BMI]])
        numeric_scaled = scaler.transform(numeric_features)
        categorical_features = np.array([[gender, cholesterol, gluc, smoke, alco, active]])
        input_final = np.hstack((numeric_scaled, categorical_features))
        
        prob = model.predict_proba(input_final)[0]
        pred = model.predict(input_final)[0]

    # Results - FIXED probability display
    st.markdown("---")
    st.markdown("## 🎯 **Your Results**")
    
    result_col1, result_col2 = st.columns([3,1])
    
    with result_col1:
        if pred == 1:
            st.markdown('<div class="result-high">', unsafe_allow_html=True)
            st.markdown("### ⚠️ **HIGH RISK**")
            st.markdown(f"**Probability**: `{prob:.2f}`")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-low">', unsafe_allow_html=True)
            st.markdown("### ✅ **LOW RISK**")
            st.markdown(f"**Probability**: `{prob:.2f}`")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with result_col2:
        risk_emoji = "🔴" if pred == 1 else "🩷"
        st.markdown(f'<div style="font-size: 4rem; text-align: center;">{risk_emoji}</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #ff69b4; font-style: italic;'>"
    "💕 Built with love | For educational purposes only | Consult a doctor"
    "</p>", 
    unsafe_allow_html=True
)
