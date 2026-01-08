# Week 1: Problem Definition & Dataset Exploration

## Problem Statement
Predict presence of cardiovascular disease (binary classification) using patient health metrics.

## Dataset Summary
- Source: Kaggle Cardiovascular Disease Dataset
- Size: 70,000 records × 12 features
- Target: cardio (0=healthy, 1=disease) - 45% positive cases
- Key features: age, height, weight, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active

## Initial Observations
- No missing values detected
- Age range: 29-65 years
- Height outliers: <100cm (likely data entry errors)
- Strong age-cholesterol correlation (0.25)
- Cardio patients older with higher cholesterol
