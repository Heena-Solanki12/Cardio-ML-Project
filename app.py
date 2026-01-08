import streamlit as st
import numpy as np
import pickle
import json
from datetime import datetime

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Cardiovascular Disease Risk Predictor",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# THEME MANAGEMENT
# ============================================================================
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

# ============================================================================
# DYNAMIC CSS BASED ON THEME
# ============================================================================
def get_theme_css(theme):
    if theme == 'dark':
        return """
        <style>
            .main {
                background-color: #0e1117;
                color: #fafafa;
            }
            .main-header {
                font-size: 3.5rem;
                font-weight: 800;
                background: linear-gradient(135deg, #ff6b9d 0%, #c44569 50%, #8e2c52 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-align: center;
                margin-bottom: 1rem;
                padding: 1rem 0;
            }
            .section-header {
                color: #ff6b9d;
                font-size: 1.8rem;
                font-weight: 700;
                margin-top: 2rem;
                margin-bottom: 1rem;
                border-bottom: 3px solid #ff6b9d;
                padding-bottom: 0.5rem;
            }
            .info-card {
                background: linear-gradient(135deg, rgba(255,107,157,0.15) 0%, rgba(142,44,82,0.15) 100%);
                padding: 1.5rem;
                border-radius: 15px;
                border: 2px solid rgba(255,107,157,0.4);
                margin: 1rem 0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            }
            .metric-card {
                background: linear-gradient(135deg, #1e2530 0%, #2d3748 100%);
                padding: 1.5rem;
                border-radius: 12px;
                border: 2px solid #ff6b9d;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            }
            .risk-high {
                background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
                color: white;
                padding: 2rem;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0 8px 16px rgba(231,76,60,0.4);
                margin: 2rem 0;
            }
            .risk-low {
                background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
                color: white;
                padding: 2rem;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0 8px 16px rgba(39,174,96,0.4);
                margin: 2rem 0;
            }
            .risk-moderate {
                background: linear-gradient(135deg, #f39c12 0%, #d68910 100%);
                color: white;
                padding: 2rem;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0 8px 16px rgba(243,156,18,0.4);
                margin: 2rem 0;
            }
            .prevention-card {
                background: linear-gradient(135deg, rgba(255,107,157,0.1) 0%, rgba(142,44,82,0.1) 100%);
                padding: 1.5rem;
                border-radius: 15px;
                border-left: 5px solid #ff6b9d;
                margin: 1rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
            .warning-box {
                background: linear-gradient(135deg, rgba(231,76,60,0.2) 0%, rgba(192,57,43,0.2) 100%);
                padding: 1.5rem;
                border-radius: 12px;
                border-left: 5px solid #e74c3c;
                margin: 1.5rem 0;
            }
            .stat-box {
                background: #1e2530;
                padding: 1rem;
                border-radius: 10px;
                border: 1px solid #ff6b9d;
                margin: 0.5rem 0;
            }
        </style>
        """
    else:  # light theme
        return """
        <style>
            .main {
                background-color: #ffffff;
                color: #262730;
            }
            .main-header {
                font-size: 3.5rem;
                font-weight: 800;
                background: linear-gradient(135deg, #ff69b4 0%, #ff1493 50%, #c71585 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-align: center;
                margin-bottom: 1rem;
                padding: 1rem 0;
            }
            .section-header {
                color: #ff1493;
                font-size: 1.8rem;
                font-weight: 700;
                margin-top: 2rem;
                margin-bottom: 1rem;
                border-bottom: 3px solid #ff69b4;
                padding-bottom: 0.5rem;
            }
            .info-card {
                background: linear-gradient(135deg, rgba(255,105,180,0.1) 0%, rgba(255,20,147,0.1) 100%);
                padding: 1.5rem;
                border-radius: 15px;
                border: 2px solid rgba(255,105,180,0.3);
                margin: 1rem 0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .metric-card {
                background: linear-gradient(135deg, #fff5f8 0%, #ffe0ec 100%);
                padding: 1.5rem;
                border-radius: 12px;
                border: 2px solid #ff69b4;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .risk-high {
                background: linear-gradient(135deg, #ff1744 0%, #d50000 100%);
                color: white;
                padding: 2rem;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0 8px 16px rgba(255,23,68,0.3);
                margin: 2rem 0;
            }
            .risk-low {
                background: linear-gradient(135deg, #00e676 0%, #00c853 100%);
                color: white;
                padding: 2rem;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0 8px 16px rgba(0,230,118,0.3);
                margin: 2rem 0;
            }
            .risk-moderate {
                background: linear-gradient(135deg, #ffc400 0%, #ff9100 100%);
                color: white;
                padding: 2rem;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0 8px 16px rgba(255,196,0,0.3);
                margin: 2rem 0;
            }
            .prevention-card {
                background: linear-gradient(135deg, rgba(255,105,180,0.08) 0%, rgba(255,20,147,0.08) 100%);
                padding: 1.5rem;
                border-radius: 15px;
                border-left: 5px solid #ff69b4;
                margin: 1rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.08);
            }
            .warning-box {
                background: linear-gradient(135deg, rgba(255,23,68,0.1) 0%, rgba(213,0,0,0.1) 100%);
                padding: 1.5rem;
                border-radius: 12px;
                border-left: 5px solid #ff1744;
                margin: 1.5rem 0;
            }
            .stat-box {
                background: #fff5f8;
                padding: 1rem;
                border-radius: 10px;
                border: 1px solid #ff69b4;
                margin: 0.5rem 0;
            }
        </style>
        """

st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

# ============================================================================
# LOAD MODEL & SCALER
# ============================================================================
@st.cache_resource
def load_model_and_scaler():
    try:
        with open("model/logistic_model.pkl", "rb") as f:
            model = pickle.load(f)
        with open("model/scaler.pkl", "rb") as f:
            scaler = pickle.load(f)
        return model, scaler, None
    except Exception as e:
        return None, None, str(e)

model, scaler, error = load_model_and_scaler()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "🔵", "Consider gaining weight healthily"
    elif 18.5 <= bmi < 25:
        return "Normal", "🟢", "Maintain your current weight"
    elif 25 <= bmi < 30:
        return "Overweight", "🟡", "Consider weight management"
    else:
        return "Obese", "🔴", "Weight loss recommended"

def get_bp_category(systolic, diastolic):
    if systolic < 120 and diastolic < 80:
        return "Normal", "🟢"
    elif 120 <= systolic < 130 and diastolic < 80:
        return "Elevated", "🟡"
    elif 130 <= systolic < 140 or 80 <= diastolic < 90:
        return "High BP Stage 1", "🟠"
    elif systolic >= 140 or diastolic >= 90:
        return "High BP Stage 2", "🔴"
    else:
        return "Normal", "🟢"

def get_risk_level(probability):
    if probability < 0.3:
        return "LOW", "low", "🟢", "#00e676"
    elif probability < 0.7:
        return "MODERATE", "moderate", "🟡", "#ffc400"
    else:
        return "HIGH", "high", "🔴", "#ff1744"

def get_prevention_tips(risk_level, bmi, bp_category, cholesterol, glucose, smoke, alco, active):
    tips = []
    
    # General tips
    tips.append({
        "icon": "🏥",
        "title": "Regular Check-ups",
        "description": "Schedule annual health screenings and monitor your cardiovascular health regularly."
    })
    
    # Risk-specific tips
    if risk_level == "high":
        tips.append({
            "icon": "⚠️",
            "title": "Immediate Medical Consultation",
            "description": "Consult a cardiologist immediately for comprehensive evaluation and personalized treatment plan."
        })
    
    # BMI-based tips
    if bmi >= 25:
        tips.append({
            "icon": "🏃",
            "title": "Weight Management",
            "description": "Aim for gradual weight loss through balanced diet and regular exercise (150 min/week of moderate activity)."
        })
    
    # BP-based tips
    if "High" in bp_category:
        tips.append({
            "icon": "🧂",
            "title": "Blood Pressure Control",
            "description": "Reduce sodium intake (<2,300mg/day), practice stress management, and consider DASH diet."
        })
    
    # Cholesterol tips
    if cholesterol > 0:
        tips.append({
            "icon": "🥗",
            "title": "Cholesterol Management",
            "description": "Adopt heart-healthy diet rich in omega-3, fiber, and limit saturated fats. Consider statins if prescribed."
        })
    
    # Glucose tips
    if glucose > 0:
        tips.append({
            "icon": "🍎",
            "title": "Blood Sugar Control",
            "description": "Monitor glucose levels, reduce refined carbs, increase fiber intake, and maintain healthy weight."
        })
    
    # Smoking tips
    if smoke == 1:
        tips.append({
            "icon": "🚭",
            "title": "Smoking Cessation - CRITICAL",
            "description": "Quitting smoking is the single most important step. Seek support through counseling or nicotine replacement therapy."
        })
    
    # Alcohol tips
    if alco == 1:
        tips.append({
            "icon": "🚫",
            "title": "Limit Alcohol Consumption",
            "description": "Reduce alcohol intake to moderate levels (≤1 drink/day for women, ≤2 for men) or eliminate completely."
        })
    
    # Physical activity tips
    if active == 0:
        tips.append({
            "icon": "💪",
            "title": "Increase Physical Activity",
            "description": "Start with 30 minutes of moderate exercise 5 days/week. Include cardio, strength training, and flexibility exercises."
        })
    
    # Additional universal tips
    tips.append({
        "icon": "😌",
        "title": "Stress Management",
        "description": "Practice relaxation techniques like meditation, yoga, or deep breathing. Ensure 7-9 hours of quality sleep."
    })
    
    tips.append({
        "icon": "🥦",
        "title": "Heart-Healthy Diet",
        "description": "Focus on fruits, vegetables, whole grains, lean proteins, and healthy fats. Limit processed foods and added sugars."
    })
    
    return tips

# ============================================================================
# HEADER WITH THEME TOGGLE
# ============================================================================
col1, col2, col3 = st.columns([1, 6, 1])
with col3:
    theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
    if st.button(theme_icon, help="Toggle theme"):
        toggle_theme()
        st.rerun()

st.markdown('<h1 class="main-header">🫀 Cardiovascular Disease Risk Predictor</h1>', unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 1.2rem; color: #888; margin-bottom: 2rem;'>"
    "Advanced AI-powered cardiovascular risk assessment with personalized recommendations"
    "</p>",
    unsafe_allow_html=True
)

# ============================================================================
# NAVIGATION TABS
# ============================================================================
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Risk Assessment", "📊 About Model", "ℹ️ About Website", "⚠️ Disclaimer"])

# ============================================================================
# TAB 1: RISK ASSESSMENT
# ============================================================================
with tab1:
    if error:
        st.error(f"❌ Error loading model: {error}")
        st.stop()
    
    # Sidebar Information
    with st.sidebar:
        st.markdown("### 📋 Input Parameters")
        st.info("""
        **Required Information:**
        - Personal demographics
        - Physical measurements
        - Health metrics
        - Lifestyle factors
        """)
        
        st.markdown("### 🎯 Risk Categories")
        st.success("🟢 **Low Risk**: <30% probability")
        st.warning("🟡 **Moderate Risk**: 30-70% probability")
        st.error("🔴 **High Risk**: >70% probability")
        
        st.markdown("### 📞 Emergency")
        st.error("""
        **Call emergency services if:**
        - Chest pain/pressure
        - Shortness of breath
        - Sudden dizziness
        - Arm/jaw pain
        """)
    
    # Input Form
    st.markdown('<h2 class="section-header">📝 Patient Information</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👤 Demographics")
        age_years = st.slider("Age (years)", 18, 100, 45, help="Patient's age in years")
        gender = st.selectbox("Gender", ["Female", "Male"], help="Biological sex")
        
        st.markdown("#### 📏 Physical Measurements")
        height = st.slider("Height (cm)", 120, 220, 165, help="Height in centimeters")
        weight = st.slider("Weight (kg)", 30, 200, 70, help="Weight in kilograms")
    
    with col2:
        st.markdown("#### 🩺 Blood Pressure")
        ap_hi = st.slider("Systolic BP (mmHg)", 80, 250, 120, help="Upper blood pressure reading")
        ap_lo = st.slider("Diastolic BP (mmHg)", 40, 150, 80, help="Lower blood pressure reading")
        
        st.markdown("#### 🧪 Lab Results")
        cholesterol = st.selectbox(
            "Cholesterol Level",
            ["Normal", "Above Normal", "Well Above Normal"],
            help="Cholesterol test results"
        )
        gluc = st.selectbox(
            "Glucose Level",
            ["Normal", "Above Normal", "Well Above Normal"],
            help="Blood glucose test results"
        )
    
    st.markdown('<h2 class="section-header">🏃 Lifestyle Factors</h2>', unsafe_allow_html=True)
    
    lifestyle_col1, lifestyle_col2, lifestyle_col3 = st.columns(3)
    
    with lifestyle_col1:
        smoke = st.radio("🚬 Smoking Status", ["Non-smoker", "Smoker"], horizontal=False)
    with lifestyle_col2:
        alco = st.radio("🍷 Alcohol Consumption", ["No", "Yes"], horizontal=False)
    with lifestyle_col3:
        active = st.radio("💪 Physically Active", ["No", "Yes"], horizontal=False)
    
    # Calculate BMI and display metrics
    BMI = weight / ((height / 100) ** 2)
    bmi_cat, bmi_emoji, bmi_advice = get_bmi_category(BMI)
    bp_cat, bp_emoji = get_bp_category(ap_hi, ap_lo)
    
    st.markdown('<h2 class="section-header">📊 Current Health Metrics</h2>', unsafe_allow_html=True)
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>BMI</h4>
            <h2>{BMI:.1f}</h2>
            <p>{bmi_emoji} {bmi_cat}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Blood Pressure</h4>
            <h2>{ap_hi}/{ap_lo}</h2>
            <p>{bp_emoji} {bp_cat}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Cholesterol</h4>
            <h2>{cholesterol}</h2>
            <p>{"🟢" if cholesterol == "Normal" else "🔴"}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col4:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Glucose</h4>
            <h2>{gluc}</h2>
            <p>{"🟢" if gluc == "Normal" else "🔴"}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Predict Button
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🔬 Analyze Cardiovascular Risk", type="primary", use_container_width=True):
        with st.spinner("🔄 Processing data and analyzing risk factors..."):
            # Encode categorical variables
            gender_encoded = 1 if gender == "Male" else 0
            cholesterol_encoded = ["Normal", "Above Normal", "Well Above Normal"].index(cholesterol)
            gluc_encoded = ["Normal", "Above Normal", "Well Above Normal"].index(gluc)
            smoke_encoded = 1 if smoke == "Smoker" else 0
            alco_encoded = 1 if alco == "Yes" else 0
            active_encoded = 1 if active == "Yes" else 0
            
            # Prepare features
            numeric_features = np.array([[age_years, height, weight, ap_hi, ap_lo, BMI]])
            numeric_scaled = scaler.transform(numeric_features)
            categorical_features = np.array([[gender_encoded, cholesterol_encoded, gluc_encoded, 
                                            smoke_encoded, alco_encoded, active_encoded]])
            input_final = np.hstack((numeric_scaled, categorical_features))
            
            # Prediction
            prob = model.predict_proba(input_final)[0]  # Probability of disease
            pred = model.predict(input_final)[0]
            
            risk_text, risk_class, risk_emoji, risk_color = get_risk_level(prob)
        
        # Display Results
        st.markdown('<h2 class="section-header">🎯 Risk Assessment Results</h2>', unsafe_allow_html=True)
        
        # Main Risk Card
        st.markdown(f"""
        <div class="risk-{risk_class}">
            <h1>{risk_emoji} {risk_text} RISK</h1>
            <h2>Cardiovascular Disease Probability: {prob*100:.1f}%</h2>
            <p style="font-size: 1.1rem; margin-top: 1rem;">
                Based on the provided health metrics and lifestyle factors
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Detailed Analysis
        st.markdown('<h3 class="section-header">📈 Detailed Risk Analysis</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown("#### 🎲 Probability Breakdown")
            st.progress(prob)
            st.markdown(f"""
            - **Disease Probability**: {prob*100:.1f}%
            - **Healthy Probability**: {(1-prob)*100:.1f}%
            - **Risk Category**: {risk_text}
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown("#### ⚠️ Key Risk Factors Identified")
            risk_factors = []
            
            if BMI >= 25:
                risk_factors.append(f"• High BMI ({BMI:.1f})")
            if "High" in bp_cat:
                risk_factors.append(f"• {bp_cat}")
            if cholesterol != "Normal":
                risk_factors.append(f"• {cholesterol} Cholesterol")
            if gluc != "Normal":
                risk_factors.append(f"• {gluc} Glucose")
            if smoke_encoded == 1:
                risk_factors.append("• Smoking")
            if alco_encoded == 1:
                risk_factors.append("• Alcohol consumption")
            if active_encoded == 0:
                risk_factors.append("• Physical inactivity")
            
            if risk_factors:
                for factor in risk_factors:
                    st.markdown(factor)
            else:
                st.markdown("✅ No major risk factors identified")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Prevention Tips
        st.markdown('<h3 class="section-header">💡 Personalized Prevention & Management Tips</h3>', unsafe_allow_html=True)
        
        prevention_tips = get_prevention_tips(
            risk_class, BMI, bp_cat, cholesterol_encoded, gluc_encoded,
            smoke_encoded, alco_encoded, active_encoded
        )
        
        cols = st.columns(2)
        for idx, tip in enumerate(prevention_tips):
            with cols[idx % 2]:
                st.markdown(f"""
                <div class="prevention-card">
                    <h4>{tip['icon']} {tip['title']}</h4>
                    <p>{tip['description']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Warning Box
        st.markdown("""
        <div class="warning-box">
            <h4>⚠️ Important Medical Disclaimer</h4>
            <p>
                This prediction is based on statistical models and should NOT replace professional medical advice.
                Please consult with a qualified healthcare provider for proper diagnosis and treatment.
                If you experience symptoms like chest pain, shortness of breath, or severe discomfort,
                <strong>seek immediate medical attention</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Download Report
        report_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "patient_info": {
                "age": age_years,
                "gender": gender,
                "height_cm": height,
                "weight_kg": weight,
                "bmi": round(BMI, 2)
            },
            "health_metrics": {
                "systolic_bp": ap_hi,
                "diastolic_bp": ap_lo,
                "bp_category": bp_cat,
                "cholesterol": cholesterol,
                "glucose": gluc
            },
            "lifestyle": {
                "smoking": smoke,
                "alcohol": alco,
                "physical_activity": active
            },
            "results": {
                "risk_level": risk_text,
                "disease_probability": round(prob * 100, 2),
                "prediction": "Positive" if pred == 1 else "Negative"
            }
        }
        
        st.download_button(
            label="📥 Download Detailed Report (JSON)",
            data=json.dumps(report_data, indent=2),
            file_name=f"cardio_risk_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# ============================================================================
# TAB 2: ABOUT MODEL
# ============================================================================
with tab2:
    st.markdown('<h2 class="section-header">🤖 Machine Learning Model Information</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("""
    ### 📊 Model Architecture
    
    **Algorithm**: Logistic Regression (Built from Scratch)
    
    **Type**: Binary Classification Model
    
    **Purpose**: Predict the presence or absence of cardiovascular disease based on patient health metrics and lifestyle factors.
    
    #### 🔧 Technical Specifications
    
    - **Learning Rate**: 0.005
    - **Iterations**: 3,000
    - **Optimization**: Gradient Descent
    - **Implementation**: Custom implementation without external ML libraries
    - **Regularization**: None (standard logistic regression)
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("""
        ### 📥 Input Features (12 total)
        
        #### Numerical Features (6):
        1. **Age** - Patient age in years
        2. **Height** - Height in centimeters
        3. **Weight** - Weight in kilograms
        4. **Systolic BP** - Upper blood pressure
        5. **Diastolic BP** - Lower blood pressure
        6. **BMI** - Body Mass Index (calculated)
        
        #### Categorical Features (6):
        7. **Gender** - Male/Female (binary)
        8. **Cholesterol** - Normal/Above/Well Above (0/1/2)
        9. **Glucose** - Normal/Above/Well Above (0/1/2)
        10. **Smoking** - Yes/No (binary)
        11. **Alcohol** - Yes/No (binary)
        12. **Physical Activity** - Yes/No (binary)
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("""
        ### 📤 Model Output
        
        **Binary Classification**:
        - **0**: No cardiovascular disease
        - **1**: Cardiovascular disease present
        
        **Probability Score**:
        - Range: 0.0 to 1.0
        - Represents likelihood of disease
        - Used for risk stratification
        
        **Risk Categories**:
        - 🟢 **Low**: <30% probability
        - 🟡 **Moderate**: 30-70% probability
        - 🔴 **High**: >70% probability
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("""
    ### 📊 Model Performance Metrics
    
    *Note: Run the enhanced train.py to generate detailed performance metrics*
    
    **Key Metrics to Monitor**:
    - **Accuracy**: Overall correct predictions
    - **Precision**: True positive rate among positive predictions
    - **Recall (Sensitivity)**: True positive detection rate
    - **F1-Score**: Harmonic mean of precision and recall
    - **ROC-AUC**: Model's discrimination capability
    
    **Model Validation**:
    - Training/Test split with proper stratification
    - Cross-validation for robust performance estimation
    - Overfitting/Underfitting analysis through train vs test metrics
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("""
    ### 🔄 Data Preprocessing
    
    **Feature Scaling**:
    - Numerical features normalized using StandardScaler
    - Ensures all features contribute equally to predictions
    - Prevents features with larger ranges from dominating
    
    **Categorical Encoding**:
    - Binary features: 0/1 encoding
    - Ordinal features (cholesterol, glucose): 0/1/2 encoding
    - Gender: Male=1, Female=0
    
    **Feature Engineering**:
    - BMI calculated from height and weight
    - All features validated for medical plausibility
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# TAB 3: ABOUT WEBSITE
# ============================================================================
with tab3:
    st.markdown('<h2 class="section-header">ℹ️ About This Application</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("""
    ### 🎯 Purpose & Mission
    
    The **Cardiovascular Disease Risk Predictor** is an AI-powered web application designed to provide
    preliminary cardiovascular risk assessment based on patient health metrics and lifestyle factors.
    
    **Our Mission**:
    - Raise awareness about cardiovascular disease risk factors
    - Provide accessible preliminary health screening
    - Encourage proactive health management
    - Bridge the gap between individuals and healthcare providers
    
    **Target Audience**:
    - Individuals concerned about heart health
    - Healthcare professionals for preliminary screening
    - Medical students and researchers
    - Health-conscious individuals seeking self-assessment
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("""
        ### ✨ Key Features
        
        - **🎨 Theme Toggle**: Light/Dark mode for comfortable viewing
        - **📊 Real-time Risk Assessment**: Instant predictions
        - **💡 Personalized Recommendations**: Tailored prevention tips
        - **📈 Health Metrics Dashboard**: Visual health indicators
        - **📥 Report Export**: Download detailed JSON reports
        - **🔒 Privacy First**: No data storage or tracking
        - **📱 Responsive Design**: Works on all devices
        - **♿ Accessible**: User-friendly interface for all
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("""
        ### 🛠️ Technology Stack
        
        - **Frontend**: Streamlit
        - **ML Framework**: Custom Logistic Regression
        - **Data Processing**: NumPy, Pandas
        - **Styling**: Custom CSS with gradient themes
        - **Export**: JSON format for interoperability
        - **Deployment**: Python 3.x compatible
        
        **Development Principles**:
        - Clean, maintainable code
        - Medical accuracy prioritization
        - Ethical AI practices
        - User privacy protection
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("""
    ### 🔐 Privacy & Data Security
    
    **Your Privacy Matters**:
    - ✅ No data is stored on servers
    - ✅ No personal information collected
    - ✅ No tracking or cookies used
    - ✅ All processing done locally in your browser session
    - ✅ No third-party data sharing
    
    **Session Data**:
    - Input data exists only during your session
    - Automatically cleared when you close the browser
    - You control all data through export features
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("""
    ### 📚 Educational Value
    
    This application serves as an educational tool to:
    
    1. **Understand Risk Factors**: Learn which factors contribute to cardiovascular disease
    2. **Health Awareness**: Recognize the importance of lifestyle modifications
    3. **Preventive Care**: Understand preventive measures and their impact
    4. **Data Literacy**: See how health data translates to risk assessment
    5. **ML Applications**: Demonstrate practical machine learning in healthcare
    
    **Learning Resources**:
    - Interactive risk assessment
    - Detailed prevention strategies
    - Real-time health metric interpretation
    - Comprehensive model documentation
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# TAB 4: DISCLAIMER
# ============================================================================
with tab4:
    st.markdown('<h2 class="section-header">⚠️ Important Disclaimers</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="warning-box">
        <h3>🚨 Medical Disclaimer</h3>
        <p style="font-size: 1.1rem; line-height: 1.8;">
            <strong>THIS APPLICATION IS FOR EDUCATIONAL AND INFORMATIONAL PURPOSES ONLY.</strong>
        </p>
        <p style="line-height: 1.8;">
            The predictions and information provided by this cardiovascular disease risk predictor
            are based on statistical models and machine learning algorithms. They are NOT intended
            to be a substitute for professional medical advice, diagnosis, or treatment.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("""
    ### ⚕️ Professional Medical Advice Required
    
    **ALWAYS consult qualified healthcare professionals**:
    
    - **Diagnosis**: Only licensed physicians can diagnose cardiovascular disease
    - **Treatment**: Medical treatment requires proper clinical evaluation
    - **Medication**: Never start or stop medications without doctor consultation
    - **Emergency**: Chest pain, shortness of breath → Call emergency services immediately
    
    **This tool cannot replace**:
    - Physical examination by a doctor
    - Medical imaging (ECG, echocardiogram, stress tests)
    - Blood work and laboratory analysis
    - Clinical judgment and medical expertise
    - Comprehensive patient history evaluation
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("""
    ### 🎯 Limitations of This Model
    
    **Model Limitations**:
    
    1. **Statistical Nature**: Predictions are probabilistic, not definitive
    2. **Training Data**: Limited to patterns in historical data
    3. **Individual Variation**: Cannot account for all personal health factors
    4. **Simplified Features**: Uses limited set of health metrics
    5. **No Context**: Cannot consider full medical history
    6. **No Imaging**: Cannot analyze medical scans or tests
    7. **Population-Based**: May not reflect individual circumstances
    8. **No Follow-up**: Cannot monitor disease progression
    
    **Not Suitable For**:
    - Emergency medical situations
    - Definitive diagnosis
    - Treatment planning
    - Medication adjustment
    - Replacing doctor visits
    - Legal or insurance purposes
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("""
    ### ⚖️ Liability & Responsibility
    
    **User Responsibility**:
    
    By using this application, you acknowledge and agree that:
    
    - You understand this is an educational tool only
    - You will not use results for self-diagnosis or self-treatment
    - You will consult healthcare professionals for medical decisions
    - You accept all responsibility for how you use this information
    - You will not hold developers liable for any health outcomes
    
    **Developer Limitations**:
    
    - No warranty of accuracy or reliability
    - No guarantee of model performance
    - No liability for decisions made based on predictions
    - Not responsible for misuse or misinterpretation
    - Continuous improvement but no perfection guarantee
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("""
    ### 🚑 When to Seek Immediate Medical Help
    
    **Call Emergency Services (911/112) IMMEDIATELY if you experience**:
    
    - 🚨 **Chest pain or pressure** (especially lasting >5 minutes)
    - 🚨 **Severe shortness of breath**
    - 🚨 **Pain radiating to arm, jaw, neck, or back**
    - 🚨 **Sudden severe headache**
    - 🚨 **Loss of consciousness or fainting**
    - 🚨 **Irregular or rapid heartbeat with symptoms**
    - 🚨 **Cold sweats with chest discomfort**
    - 🚨 **Sudden weakness or numbness** (especially one-sided)
    
    **DO NOT**:
    - ❌ Wait to see if symptoms improve
    - ❌ Drive yourself to hospital
    - ❌ Rely on this app during emergencies
    
    **Time is critical** in cardiovascular emergencies. Every minute counts.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("""
    ### 📋 Recommended Actions
    
    **If you receive a HIGH RISK result**:
    
    1. ✅ Schedule appointment with primary care physician
    2. ✅ Request comprehensive cardiovascular evaluation
    3. ✅ Consider seeing a cardiologist
    4. ✅ Discuss lifestyle modifications with doctor
    5. ✅ Get recommended medical tests (ECG, blood work, etc.)
    6. ✅ Start tracking your blood pressure and other metrics
    
    **If you receive a LOW/MODERATE RISK result**:
    
    1. ✅ Maintain regular health check-ups
    2. ✅ Continue healthy lifestyle habits
    3. ✅ Monitor changes in health status
    4. ✅ Discuss results with doctor at next visit
    5. ✅ Stay informed about cardiovascular health
    
    **Remember**: ANY risk level warrants professional medical consultation.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="warning-box">
        <h3>✅ Acceptance of Terms</h3>
        <p style="line-height: 1.8;">
            By using this application, you acknowledge that you have read, understood, and agree
            to all disclaimers and limitations stated above. You confirm that you will use this
            tool responsibly as an educational resource only and will seek professional medical
            advice for all health-related decisions.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 2rem 0; color: #888;'>
        <p style='font-size: 0.9rem;'>
            🫀 <strong>Cardiovascular Disease Risk Predictor</strong> | 
            Built for Educational Purposes | 
            © 2024
        </p>
        <p style='font-size: 0.85rem; font-style: italic; margin-top: 0.5rem;'>
            Always consult qualified healthcare professionals for medical advice
        </p>
    </div>
    """,
    unsafe_allow_html=True
)