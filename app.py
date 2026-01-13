import streamlit as st
import numpy as np
import pandas as pd
import pickle
import json
import plotly.graph_objects as go
from datetime import datetime

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="CardioGuard AI - Cardiovascular Disease Predictor",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

if 'show_results' not in st.session_state:
    st.session_state.show_results = False

if 'current_section' not in st.session_state:
    st.session_state.current_section = 'home'

def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

def navigate_to(section):
    st.session_state.current_section = section

# ============================================================================
# ENHANCED CSS WITH FIXED NAVIGATION AND SCROLLING
# ============================================================================
def get_theme_css(theme):
    if theme == 'dark':
        return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
            
            * {
                font-family: 'Inter', sans-serif;
            }
            
            /* Hide Streamlit defaults */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            [data-testid="stAppViewContainer"] {
                background: #0a0e27;
            }
            
            [data-testid="stHeader"] {
                background: transparent;
            }
            
            [data-testid="stSidebar"] {
                display: none;
            }
            
            /* Smooth scroll */
            html {
                scroll-behavior: smooth;
            }
            
            /* Fixed Navigation Bar */
            .navbar {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                z-index: 9999;
                background: rgba(10, 14, 39, 0.98);
                backdrop-filter: blur(10px);
                padding: 1rem 0;
                border-bottom: 1px solid rgba(59, 130, 246, 0.2);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            }
            
            .navbar-container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 0 2rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .navbar-brand {
                font-size: 1.8rem;
                font-weight: 800;
                background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                cursor: pointer;
            }
            
            .navbar-menu {
                display: flex;
                gap: 2.5rem;
                align-items: center;
            }
            
            .nav-link {
                color: #e2e8f0;
                text-decoration: none;
                font-weight: 500;
                font-size: 0.95rem;
                transition: all 0.3s;
                cursor: pointer;
                padding: 0.5rem 1rem;
                border-radius: 8px;
            }
            
            .nav-link:hover {
                color: #3b82f6;
                background: rgba(59, 130, 246, 0.1);
            }
            
            /* Content padding for fixed navbar */
            .main .block-container {
                padding-top: 0 !important;
                max-width: 100% !important;
            }
            
            /* Hero Section */
            .hero-section {
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, rgba(10, 14, 39, 0.9) 0%, rgba(26, 31, 58, 0.9) 100%);
                padding: 8rem 2rem 4rem;
                margin-top: 70px;
            }
            
            .hero-content {
                max-width: 1400px;
                width: 100%;
                text-align: center;
            }
            
            .hero-title {
                font-size: 4.5rem;
                font-weight: 800;
                background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 50%, #8b5cf6 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 1.5rem;
                line-height: 1.2;
            }
            
            .hero-subtitle {
                font-size: 1.5rem;
                color: #94a3b8;
                margin-bottom: 3rem;
                font-weight: 400;
            }
            
            /* Section */
            .section {
                padding: 6rem 2rem;
                max-width: 1400px;
                margin: 0 auto;
            }
            
            .section-title {
                font-size: 3rem;
                font-weight: 800;
                text-align: center;
                background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 1rem;
            }
            
            .section-subtitle {
                font-size: 1.2rem;
                color: #94a3b8;
                text-align: center;
                margin-bottom: 4rem;
            }
            
            /* Stats Grid */
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 2rem;
                margin-top: 3rem;
            }
            
            .stat-card {
                background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
                padding: 2rem;
                border-radius: 16px;
                text-align: center;
                border: 2px solid #3b82f6;
            }
            
            .stat-number {
                font-size: 3rem;
                font-weight: 800;
                color: white;
                margin-bottom: 0.5rem;
            }
            
            .stat-label {
                font-size: 1rem;
                color: #bfdbfe;
            }
            
            /* Features Grid */
            .features-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 2rem;
                margin-top: 3rem;
            }
            
            .feature-card {
                background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                padding: 2.5rem;
                border-radius: 20px;
                border: 2px solid rgba(59, 130, 246, 0.2);
                transition: all 0.3s;
                text-align: center;
            }
            
            .feature-card:hover {
                transform: translateY(-10px);
                border-color: #3b82f6;
                box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3);
            }
            
            .feature-icon {
                font-size: 3rem;
                margin-bottom: 1.5rem;
            }
            
            .feature-title {
                font-size: 1.5rem;
                font-weight: 700;
                color: #e2e8f0;
                margin-bottom: 1rem;
            }
            
            .feature-text {
                font-size: 1rem;
                color: #94a3b8;
                line-height: 1.6;
            }
            
            /* Assessment Container */
            .assessment-container {
                background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                padding: 3rem;
                border-radius: 24px;
                border: 2px solid rgba(59, 130, 246, 0.3);
                margin-top: 3rem;
            }
            
            .form-section-title {
                font-size: 1.5rem;
                font-weight: 700;
                color: #3b82f6;
                margin-bottom: 1.5rem;
            }
            
            /* Results */
            .results-hero {
                background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                padding: 3rem;
                border-radius: 24px;
                border: 3px solid #3b82f6;
                margin: 3rem 0;
                text-align: center;
            }
            
            .risk-badge {
                display: inline-block;
                padding: 1rem 3rem;
                border-radius: 50px;
                font-size: 2.5rem;
                font-weight: 800;
                margin-bottom: 1.5rem;
            }
            
            .risk-low {
                background: linear-gradient(135deg, #059669 0%, #047857 100%);
                color: white;
            }
            
            .risk-moderate {
                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                color: white;
            }
            
            .risk-high {
                background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
                color: white;
            }
            
            /* Footer */
            .footer {
                background: #0a0e27;
                padding: 3rem 2rem;
                text-align: center;
                border-top: 1px solid rgba(59, 130, 246, 0.2);
                margin-top: 4rem;
            }
            
            .footer-text {
                color: #94a3b8;
                font-size: 0.95rem;
                margin: 0.5rem 0;
            }
            
            /* Streamlit Overrides */
            .stButton>button {
                width: 100%;
                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                color: white;
                padding: 1rem 2rem;
                font-size: 1.1rem;
                font-weight: 700;
                border: none;
                border-radius: 12px;
                box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
                transition: all 0.3s ease;
            }
            
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 32px rgba(59, 130, 246, 0.6);
            }
            
            /* Form elements */
            .stSlider {
                padding: 1rem 0;
            }
            
            .stSelectbox {
                padding: 0.5rem 0;
            }
            
            .stRadio {
                padding: 0.5rem 0;
            }
            
            /* Text colors - Dark Theme */
            .main h1, .main h2, .main h3, .main h4 {
                color: #e2e8f0 !important;
            }
            
            .main p, .main span, .main div, .main label {
                color: #e2e8f0 !important;
            }
            
            /* Metric styling */
            [data-testid="stMetricValue"] {
                color: #3b82f6 !important;
                font-size: 2rem !important;
                font-weight: 800 !important;
            }
            
            [data-testid="stMetricLabel"] {
                color: #94a3b8 !important;
            }
            
            [data-testid="stMetricDelta"] {
                color: #94a3b8 !important;
            }
            
            /* Fix Streamlit elements in dark theme */
            .stMarkdown, .stMarkdown p {
                color: #e2e8f0 !important;
            }
            
            /* Input labels */
            label[data-testid="stWidgetLabel"] {
                color: #94a3b8 !important;
            }
        </style>
        """
    else:  # light theme
        return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
            
            * {
                font-family: 'Inter', sans-serif;
            }
            
            /* Hide Streamlit defaults */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            [data-testid="stAppViewContainer"] {
                background: #ffffff;
            }
            
            [data-testid="stHeader"] {
                background: transparent;
            }
            
            [data-testid="stSidebar"] {
                display: none;
            }
            
            /* Smooth scroll */
            html {
                scroll-behavior: smooth;
            }
            
            /* Fixed Navigation Bar */
            .navbar {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                z-index: 9999;
                background: rgba(255, 255, 255, 0.98);
                backdrop-filter: blur(10px);
                padding: 1rem 0;
                border-bottom: 1px solid rgba(59, 130, 246, 0.1);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            }
            
            .navbar-container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 0 2rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .navbar-brand {
                font-size: 1.8rem;
                font-weight: 800;
                background: linear-gradient(135deg, #1e40af 0%, #0891b2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                cursor: pointer;
            }
            
            .navbar-menu {
                display: flex;
                gap: 2.5rem;
                align-items: center;
            }
            
            .nav-link {
                color: #1e293b;
                text-decoration: none;
                font-weight: 500;
                font-size: 0.95rem;
                transition: all 0.3s;
                cursor: pointer;
                padding: 0.5rem 1rem;
                border-radius: 8px;
            }
            
            .nav-link:hover {
                color: #3b82f6;
                background: rgba(59, 130, 246, 0.1);
            }
            
            /* Content padding for fixed navbar */
            .main .block-container {
                padding-top: 0 !important;
                max-width: 100% !important;
            }
            
            /* Hero Section */
            .hero-section {
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                padding: 8rem 2rem 4rem;
                margin-top: 70px;
            }
            
            .hero-content {
                max-width: 1400px;
                width: 100%;
                text-align: center;
            }
            
            .hero-title {
                font-size: 4.5rem;
                font-weight: 800;
                background: linear-gradient(135deg, #1e40af 0%, #0891b2 50%, #7c3aed 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 1.5rem;
                line-height: 1.2;
            }
            
            .hero-subtitle {
                font-size: 1.5rem;
                color: #64748b;
                margin-bottom: 3rem;
                font-weight: 400;
            }
            
            /* Section */
            .section {
                padding: 6rem 2rem;
                max-width: 1400px;
                margin: 0 auto;
            }
            
            .section-title {
                font-size: 3rem;
                font-weight: 800;
                text-align: center;
                background: linear-gradient(135deg, #1e40af 0%, #0891b2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 1rem;
            }
            
            .section-subtitle {
                font-size: 1.2rem;
                color: #64748b;
                text-align: center;
                margin-bottom: 4rem;
            }
            
            /* Stats Grid */
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 2rem;
                margin-top: 3rem;
            }
            
            .stat-card {
                background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
                padding: 2rem;
                border-radius: 16px;
                text-align: center;
                border: 2px solid #3b82f6;
            }
            
            .stat-number {
                font-size: 3rem;
                font-weight: 800;
                color: #1e40af;
                margin-bottom: 0.5rem;
            }
            
            .stat-label {
                font-size: 1rem;
                color: #3b82f6;
            }
            
            /* Features Grid */
            .features-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 2rem;
                margin-top: 3rem;
            }
            
            .feature-card {
                background: white;
                padding: 2.5rem;
                border-radius: 20px;
                border: 2px solid rgba(59, 130, 246, 0.15);
                transition: all 0.3s;
                text-align: center;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
            }
            
            .feature-card:hover {
                transform: translateY(-10px);
                border-color: #3b82f6;
                box-shadow: 0 20px 40px rgba(59, 130, 246, 0.2);
            }
            
            .feature-icon {
                font-size: 3rem;
                margin-bottom: 1.5rem;
            }
            
            .feature-title {
                font-size: 1.5rem;
                font-weight: 700;
                color: #1e293b;
                margin-bottom: 1rem;
            }
            
            .feature-text {
                font-size: 1rem;
                color: #64748b;
                line-height: 1.6;
            }
            
            /* Assessment Container */
            .assessment-container {
                background: white;
                padding: 3rem;
                border-radius: 24px;
                border: 2px solid rgba(59, 130, 246, 0.2);
                margin-top: 3rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
            }
            
            .form-section-title {
                font-size: 1.5rem;
                font-weight: 700;
                color: #3b82f6;
                margin-bottom: 1.5rem;
            }
            
            /* Results */
            .results-hero {
                background: white;
                padding: 3rem;
                border-radius: 24px;
                border: 3px solid #3b82f6;
                margin: 3rem 0;
                text-align: center;
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
            }
            
            .risk-badge {
                display: inline-block;
                padding: 1rem 3rem;
                border-radius: 50px;
                font-size: 2.5rem;
                font-weight: 800;
                margin-bottom: 1.5rem;
            }
            
            .risk-low {
                background: linear-gradient(135deg, #059669 0%, #047857 100%);
                color: white;
            }
            
            .risk-moderate {
                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                color: white;
            }
            
            .risk-high {
                background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
                color: white;
            }
            
            /* Footer */
            .footer {
                background: #f8fafc;
                padding: 3rem 2rem;
                text-align: center;
                border-top: 1px solid rgba(59, 130, 246, 0.1);
                margin-top: 4rem;
            }
            
            .footer-text {
                color: #64748b;
                font-size: 0.95rem;
                margin: 0.5rem 0;
            }
            
            /* Streamlit Overrides */
            .stButton>button {
                width: 100%;
                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                color: white;
                padding: 1rem 2rem;
                font-size: 1.1rem;
                font-weight: 700;
                border: none;
                border-radius: 12px;
                box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
                transition: all 0.3s ease;
            }
            
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 32px rgba(59, 130, 246, 0.5);
            }
            
            /* Form elements */
            .stSlider {
                padding: 1rem 0;
            }
            
            .stSelectbox {
                padding: 0.5rem 0;
            }
            
            .stRadio {
                padding: 0.5rem 0;
            }
            
            /* Text colors - Light Theme */
            .main h1, .main h2, .main h3, .main h4 {
                color: #1e293b !important;
            }
            
            .main p, .main span, .main div {
                color: #1e293b !important;
            }
            
            .main label {
                color: #475569 !important;
            }
            
            /* Metric styling */
            [data-testid="stMetricValue"] {
                color: #3b82f6 !important;
                font-size: 2rem !important;
                font-weight: 800 !important;
            }
            
            [data-testid="stMetricLabel"] {
                color: #64748b !important;
            }
            
            [data-testid="stMetricDelta"] {
                color: #64748b !important;
            }
            
            /* Fix Streamlit elements in light theme */
            .stMarkdown, .stMarkdown p {
                color: #1e293b !important;
            }
            
            /* Input labels */
            label[data-testid="stWidgetLabel"] {
                color: #475569 !important;
                font-weight: 500 !important;
            }
            
            /* Info box text */
            .stAlert p {
                color: #1e293b !important;
            }
        </style>
        """

# Apply theme CSS
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
        try:
            with open("model/training_report.json", "r") as f:
                report = json.load(f)
        except:
            report = None
        return model, scaler, report, None
    except Exception as e:
        return None, None, None, str(e)

model, scaler, training_report, error = load_model_and_scaler()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "🔵", "Consider gaining weight"
    elif 18.5 <= bmi < 25:
        return "Normal", "🟢", "Maintain current weight"
    elif 25 <= bmi < 30:
        return "Overweight", "🟡", "Weight management advised"
    else:
        return "Obese", "🔴", "Weight loss recommended"

def get_bp_category(systolic, diastolic):
    if systolic < 120 and diastolic < 80:
        return "Normal", "🟢"
    elif 120 <= systolic < 130 and diastolic < 80:
        return "Elevated", "🟡"
    elif 130 <= systolic < 140 or 80 <= diastolic < 90:
        return "Stage 1 High BP", "🟠"
    else:
        return "Stage 2 High BP", "🔴"

def get_risk_level(probability):
    if probability < 0.3:
        return "LOW RISK", "low", "🟢"
    elif probability < 0.7:
        return "MODERATE RISK", "moderate", "🟡"
    else:
        return "HIGH RISK", "high", "🔴"

def create_gauge_chart(probability, theme):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = probability * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Risk Probability (%)", 'font': {'size': 20, 'color': '#e2e8f0' if theme == 'dark' else '#1e293b'}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 2},
            'bar': {'color': "#3b82f6"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#cbd5e1",
            'steps': [
                {'range': [0, 30], 'color': '#d1fae5'},
                {'range': [30, 70], 'color': '#fef3c7'},
                {'range': [70, 100], 'color': '#fee2e2'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#e2e8f0' if theme == 'dark' else '#1e293b'},
        height=350,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

# ============================================================================
# NAVIGATION BAR
# ============================================================================
theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
theme_text = "Dark" if st.session_state.theme == 'light' else "Light"

# Create columns for theme toggle button in top-right
col_empty, col_theme = st.columns([9, 1])
with col_theme:
    if st.button(f"{theme_icon}", key="theme_btn", help=f"Switch to {theme_text} Mode"):
        toggle_theme()
        st.rerun()

st.markdown(f"""
<div class="navbar">
    <div class="navbar-container">
        <div class="navbar-brand">❤️ CardioGuard AI</div>
        <div class="navbar-menu">
            <span class="nav-link">Home</span>
            <span class="nav-link">Features</span>
            <span class="nav-link">Assessment</span>
            <span class="nav-link">About</span>
            <span class="nav-link">Stats</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# HERO SECTION
# ============================================================================
st.markdown("""
<div id="home" class="hero-section">
<div class="hero-content">
<h1 class="hero-title">CardioGuard AI</h1>
<p class="hero-subtitle">Advanced AI-Powered Cardiovascular Disease Risk Assessment</p>
<div class="stats-grid">
<div class="stat-card">
<div class="stat-number">73%</div>
<div class="stat-label">Accuracy</div>
</div>
<div class="stat-card">
<div class="stat-number">0.82</div>
<div class="stat-label">ROC-AUC Score</div>
</div>
<div class="stat-card">
<div class="stat-number">70K+</div>
<div class="stat-label">Training Samples</div>
</div>
<div class="stat-card">
<div class="stat-number">&lt;1ms</div>
<div class="stat-label">Prediction Time</div>
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# FEATURES SECTION
# ============================================================================
st.markdown("""
<div id="features" class="section">
<h2 class="section-title">Why Choose CardioGuard AI?</h2>
<p class="section-subtitle">Powered by advanced machine learning algorithms for accurate health predictions</p>

<div class="features-grid">
<div class="feature-card">
<div class="feature-icon">🤖</div>
<h3 class="feature-title">AI-Powered Analysis</h3>
<p class="feature-text">Sophisticated machine learning model trained on 70,000+ medical records for accurate predictions</p>
</div>

<div class="feature-card">
<div class="feature-icon">⚡</div>
<h3 class="feature-title">Instant Results</h3>
<p class="feature-text">Get comprehensive cardiovascular risk assessment in less than a second</p>
</div>

<div class="feature-card">
<div class="feature-icon">📊</div>
<h3 class="feature-title">Detailed Analytics</h3>
<p class="feature-text">Interactive charts and comprehensive health metrics dashboard</p>
</div>

<div class="feature-card">
<div class="feature-icon">🔒</div>
<h3 class="feature-title">Privacy First</h3>
<p class="feature-text">All data processed locally. No storage, no tracking, complete privacy</p>
</div>

<div class="feature-card">
<div class="feature-icon">💡</div>
<h3 class="feature-title">Personalized Insights</h3>
<p class="feature-text">Get tailored health recommendations based on your unique profile</p>
</div>

<div class="feature-card">
<div class="feature-icon">📥</div>
<h3 class="feature-title">Export Reports</h3>
<p class="feature-text">Download detailed health reports to share with your healthcare provider</p>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# ASSESSMENT SECTION
# ============================================================================
st.markdown('<div id="assessment" class="section">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Health Risk Assessment</h2>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">Complete the form below for a comprehensive cardiovascular risk evaluation</p>', unsafe_allow_html=True)

if error:
    st.error(f"❌ Error loading model: {error}")
else:
    # Create a container for the assessment form
    with st.container():
        st.markdown('<div class="assessment-container">', unsafe_allow_html=True)
        
        # Personal Information
        st.markdown('<h3 class="form-section-title">👤 Personal Information</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            age_years = st.slider("Age (years)", 18, 100, 45, key="age")
        with col2:
            gender = st.selectbox("Gender", ["Female", "Male"], key="gender")
        with col3:
            height = st.slider("Height (cm)", 120, 220, 165, key="height")
        
        col1, col2 = st.columns(2)
        with col1:
            weight = st.slider("Weight (kg)", 30, 200, 70, key="weight")
        with col2:
            BMI = weight / ((height / 100) ** 2)
            bmi_cat, bmi_emoji, bmi_advice = get_bmi_category(BMI)
            st.metric("Body Mass Index (BMI)", f"{BMI:.1f}", f"{bmi_emoji} {bmi_cat}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Health Metrics
        st.markdown('<h3 class="form-section-title">🩺 Health Metrics</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            ap_hi = st.slider("Systolic Blood Pressure (mmHg)", 80, 250, 120, key="systolic")
            ap_lo = st.slider("Diastolic Blood Pressure (mmHg)", 40, 150, 80, key="diastolic")
            bp_cat, bp_emoji = get_bp_category(ap_hi, ap_lo)
            st.info(f"{bp_emoji} Blood Pressure Status: **{bp_cat}**")
        
        with col2:
            cholesterol = st.selectbox(
                "Cholesterol Level",
                ["Normal", "Above Normal", "Well Above Normal"],
                key="cholesterol"
            )
            gluc = st.selectbox(
                "Glucose Level",
                ["Normal", "Above Normal", "Well Above Normal"],
                key="glucose"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Lifestyle Factors
        st.markdown('<h3 class="form-section-title">🏃 Lifestyle Factors</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            smoke = st.radio("Smoking", ["Non-smoker", "Smoker"], key="smoke")
        with col2:
            alco = st.radio("Alcohol Consumption", ["No", "Yes"], key="alcohol")
        with col3:
            active = st.radio("Physical Activity", ["No", "Yes"], key="activity")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Analyze Button
        if st.button("🔬 Analyze Cardiovascular Risk", type="primary", key="analyze_btn"):
            with st.spinner("🔄 Analyzing your health data..."):
                # Encode features
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
                prob = model.predict_proba(input_final)[0]
                pred = model.predict(input_final)[0]
                
                risk_text, risk_class, risk_emoji = get_risk_level(prob)
                
                st.session_state.show_results = True
                st.session_state.prediction_data = {
                    'prob': prob,
                    'pred': pred,
                    'risk_text': risk_text,
                    'risk_class': risk_class,
                    'risk_emoji': risk_emoji,
                    'BMI': BMI,
                    'bmi_cat': bmi_cat,
                    'bmi_emoji': bmi_emoji,
                    'ap_hi': ap_hi,
                    'ap_lo': ap_lo,
                    'bp_cat': bp_cat,
                    'bp_emoji': bp_emoji,
                    'cholesterol': cholesterol,
                    'gluc': gluc,
                    'age_years': age_years,
                    'gender': gender,
                    'height': height,
                    'weight': weight,
                    'smoke': smoke,
                    'alco': alco,
                    'active': active,
                    'smoke_encoded': smoke_encoded,
                    'alco_encoded': alco_encoded,
                    'active_encoded': active_encoded
                }
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================================================
    # RESULTS SECTION
    # ============================================================================
    if st.session_state.show_results:
        data = st.session_state.prediction_data
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">📋 Assessment Results</h2>', unsafe_allow_html=True)
        
        # Risk Badge
        st.markdown(f"""
        <div class="results-hero">
            <div class="risk-badge risk-{data['risk_class']}">
                {data['risk_emoji']} {data['risk_text']}
            </div>
            <h2 style="font-size: 2rem; margin-bottom: 0.5rem;">Disease Probability: {data['prob']*100:.1f}%</h2>
            <p style="font-size: 1.1rem; opacity: 0.8;">Based on comprehensive health metrics and lifestyle analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Gauge Chart
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            gauge_fig = create_gauge_chart(data['prob'], st.session_state.theme)
            st.plotly_chart(gauge_fig, use_container_width=True)
        
        # Health Metrics Dashboard
        st.markdown('<h3 class="section-title" style="font-size: 2rem; margin-top: 3rem;">📊 Your Health Dashboard</h3>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("BMI", f"{data['BMI']:.1f}", f"{data['bmi_emoji']} {data['bmi_cat']}")
        
        with col2:
            st.metric("Blood Pressure", f"{data['ap_hi']}/{data['ap_lo']}", f"{data['bp_emoji']} {data['bp_cat']}")
        
        with col3:
            chol_emoji = "🟢" if data['cholesterol'] == "Normal" else "🔴"
            st.metric("Cholesterol", chol_emoji, data['cholesterol'])
        
        with col4:
            gluc_emoji = "🟢" if data['gluc'] == "Normal" else "🔴"
            st.metric("Glucose", gluc_emoji, data['gluc'])
        
        # Risk Factors & Recommendations
        st.markdown('<h3 class="section-title" style="font-size: 2rem; margin-top: 3rem;">⚠️ Risk Analysis</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            with st.container():
                st.markdown('<div class="assessment-container">', unsafe_allow_html=True)
                st.markdown("#### 🎯 Identified Risk Factors")
                
                risk_factors = []
                if data['BMI'] >= 25:
                    risk_factors.append(f"• **High BMI**: {data['BMI']:.1f} (Target: <25)")
                if "High" in data['bp_cat']:
                    risk_factors.append(f"• **{data['bp_cat']}**: {data['ap_hi']}/{data['ap_lo']} mmHg")
                if data['cholesterol'] != "Normal":
                    risk_factors.append(f"• **{data['cholesterol']} Cholesterol**")
                if data['gluc'] != "Normal":
                    risk_factors.append(f"• **{data['gluc']} Glucose**")
                if data['smoke_encoded'] == 1:
                    risk_factors.append("• **Smoking** - Major cardiovascular risk")
                if data['alco_encoded'] == 1:
                    risk_factors.append("• **Alcohol consumption**")
                if data['active_encoded'] == 0:
                    risk_factors.append("• **Physical inactivity**")
                if data['age_years'] > 55:
                    risk_factors.append(f"• **Age factor**: {data['age_years']} years")
                
                if risk_factors:
                    for factor in risk_factors:
                        st.markdown(factor)
                else:
                    st.success("✅ No major risk factors identified")
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            with st.container():
                st.markdown('<div class="assessment-container">', unsafe_allow_html=True)
                st.markdown("#### 💡 Personalized Recommendations")
                
                if data['risk_class'] == "high":
                    st.error("🏥 **Immediate Action Required**")
                    st.markdown("• Schedule cardiologist appointment")
                    st.markdown("• Get comprehensive cardiac evaluation")
                    st.markdown("• Consider cardiac screening tests")
                elif data['risk_class'] == "moderate":
                    st.warning("⚠️ **Preventive Action Needed**")
                    st.markdown("• Regular health monitoring")
                    st.markdown("• Implement lifestyle modifications")
                    st.markdown("• Consult healthcare provider")
                else:
                    st.success("✅ **Maintain Healthy Habits**")
                    st.markdown("• Continue current lifestyle")
                    st.markdown("• Annual health check-ups")
                    st.markdown("• Stay physically active")
                
                if data['smoke_encoded'] == 1:
                    st.markdown("• **🚭 Quit smoking immediately**")
                if data['BMI'] >= 25:
                    st.markdown("• **🏃 Start weight management program**")
                if "High" in data['bp_cat']:
                    st.markdown("• **🧂 Reduce sodium intake**")
                    st.markdown("• **💊 Monitor blood pressure daily**")
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Download Report
        st.markdown("<br>", unsafe_allow_html=True)
        
        report_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "patient_info": {
                "age": data['age_years'],
                "gender": data['gender'],
                "height_cm": data['height'],
                "weight_kg": data['weight'],
                "bmi": round(data['BMI'], 2)
            },
            "health_metrics": {
                "systolic_bp": data['ap_hi'],
                "diastolic_bp": data['ap_lo'],
                "bp_category": data['bp_cat'],
                "cholesterol": data['cholesterol'],
                "glucose": data['gluc']
            },
            "lifestyle": {
                "smoking": data['smoke'],
                "alcohol": data['alco'],
                "physical_activity": data['active']
            },
            "results": {
                "risk_level": data['risk_text'],
                "disease_probability": round(data['prob'] * 100, 2),
                "prediction": "Positive" if data['pred'] == 1 else "Negative"
            },
            "risk_factors": risk_factors if risk_factors else ["None identified"]
        }
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="📥 Download Detailed Health Report (JSON)",
                data=json.dumps(report_data, indent=2),
                file_name=f"cardio_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# ABOUT SECTION
# ============================================================================
st.markdown("""
<div id="about" class="section">
<h2 class="section-title">About CardioGuard AI</h2>
<p class="section-subtitle">Advanced machine learning for cardiovascular health assessment</p>

<div class="features-grid">
<div class="feature-card">
<div class="feature-icon">🧠</div>
<h3 class="feature-title">Machine Learning Model</h3>
<p class="feature-text">Custom-built Logistic Regression algorithm trained from scratch on 70,000+ medical records with 12 key health features</p>
</div>

<div class="feature-card">
<div class="feature-icon">🎯</div>
<h3 class="feature-title">High Accuracy</h3>
<p class="feature-text">73% accuracy with 0.82 ROC-AUC score, providing reliable cardiovascular risk predictions</p>
</div>

<div class="feature-card">
<div class="feature-icon">🔬</div>
<h3 class="feature-title">Evidence-Based</h3>
<p class="feature-text">Built on clinical research data including age, BMI, blood pressure, cholesterol, glucose, and lifestyle factors</p>
</div>

<div class="feature-card">
<div class="feature-icon">🌐</div>
<h3 class="feature-title">Accessible Anywhere</h3>
<p class="feature-text">Web-based platform accessible 24/7 from any device with internet connection</p>
</div>

<div class="feature-card">
<div class="feature-icon">📚</div>
<h3 class="feature-title">Educational Resource</h3>
<p class="feature-text">Perfect for medical students, researchers, and healthcare professionals learning ML in healthcare</p>
</div>

<div class="feature-card">
<div class="feature-icon">⚡</div>
<h3 class="feature-title">Real-Time Processing</h3>
<p class="feature-text">Instant analysis with prediction time under 1 millisecond for immediate results</p>
</div>
</div>

<div class="assessment-container" style="margin-top: 4rem;">
<h3 style="font-size: 2rem; margin-bottom: 2rem; text-align: center;">⚠️ Important Medical Disclaimer</h3>
<div style="background: rgba(239, 68, 68, 0.1); padding: 2rem; border-radius: 16px; border-left: 6px solid #ef4444;">
<p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 1rem;">
    <strong>CardioGuard AI is a research and educational tool only.</strong> It is NOT FDA approved, clinically validated, 
    or suitable for medical diagnosis or treatment decisions. This tool cannot replace professional medical evaluation, 
    diagnostic tests (ECG, echocardiogram, blood work), or consultations with qualified healthcare providers.
</p>
<p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 1rem;">
    <strong>🚨 Emergency Warning:</strong> If you experience chest pain, severe shortness of breath, 
    arm/jaw pain, or other cardiac symptoms, call 911 or your local emergency services immediately. 
    Do not rely on this application for emergency medical decisions.
</p>
<p style="font-size: 1.1rem; line-height: 1.8;">
    Always consult with qualified healthcare professionals for medical advice, diagnosis, and treatment. 
    Use this tool at your own risk. The developers assume no liability for health outcomes.
</p>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# STATS SECTION
# ============================================================================
st.markdown("""
<div id="stats" class="section">
<h2 class="section-title">Performance Metrics</h2>
<p class="section-subtitle">Transparent model performance evaluation</p>

<div class="stats-grid">
<div class="stat-card">
<div class="stat-number">73.1%</div>
<div class="stat-label">Test Accuracy</div>
</div>

<div class="stat-card">
<div class="stat-number">71.2%</div>
<div class="stat-label">Precision</div>
</div>

<div class="stat-card">
<div class="stat-number">75.0%</div>
<div class="stat-label">Recall</div>
</div>

<div class="stat-card">
<div class="stat-number">0.731</div>
<div class="stat-label">F1-Score</div>
</div>

<div class="stat-card">
<div class="stat-number">0.820</div>
<div class="stat-label">ROC-AUC</div>
</div>

<div class="stat-card">
<div class="stat-number">12</div>
<div class="stat-label">Features</div>
</div>
</div>

<div class="assessment-container" style="margin-top: 3rem;">
<h3 style="font-size: 1.8rem; margin-bottom: 2rem;">🔍 Model Features</h3>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
<div>
    <h4 style="color: #3b82f6; margin-bottom: 1rem;">📊 Numerical Features (Scaled)</h4>
    <p>• Age (18-100 years)</p>
    <p>• Height (120-220 cm)</p>
    <p>• Weight (30-200 kg)</p>
    <p>• Systolic BP (80-250 mmHg)</p>
    <p>• Diastolic BP (40-150 mmHg)</p>
    <p>• BMI (calculated)</p>
</div>
<div>
    <h4 style="color: #3b82f6; margin-bottom: 1rem;">🏷️ Categorical Features</h4>
    <p>• Gender (Male/Female)</p>
    <p>• Cholesterol Level (0/1/2)</p>
    <p>• Glucose Level (0/1/2)</p>
    <p>• Smoking Status (0/1)</p>
    <p>• Alcohol Consumption (0/1)</p>
    <p>• Physical Activity (0/1)</p>
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("""
<div class="footer">
    <h3 style="background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
               -webkit-background-clip: text;
               -webkit-text-fill-color: transparent;
               font-size: 2rem;
               margin-bottom: 1rem;">
        ❤️ CardioGuard AI
    </h3>
    <p class="footer-text">Advanced AI Technology • Built for Prevention • Smart Heart Care</p>
    <p class="footer-text">© 2024 CardioGuard AI | Educational Purpose Only</p>
    <p class="footer-text">Always Consult Healthcare Professionals for Medical Decisions</p>
</div>
""", unsafe_allow_html=True)