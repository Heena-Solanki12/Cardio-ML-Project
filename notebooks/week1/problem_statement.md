# Cardiovascular Disease Prediction – Problem Definition

## 1. Introduction
Cardiovascular disease (CVD) is one of the leading causes of death worldwide. Early detection can significantly improve patient outcomes and reduce healthcare costs. Machine Learning models can analyze patient health parameters and provide early risk prediction, enabling timely medical intervention.

This project aims to build a Machine Learning model that predicts whether a patient is likely to have cardiovascular disease based on medical and lifestyle attributes.

---

## 2. Objective
The objective of this project is to:
- Analyze the Cardiovascular Disease dataset.
- Perform data cleaning, preprocessing, exploratory data analysis (EDA).
- Train and evaluate ML models to predict the presence of cardiovascular disease.
- Deploy the trained ML model using Flask with a simple web-based UI.

This Week-1 covers:
- Understanding the problem
- Dataset exploration
- Identifying data issues

---

## 3. Dataset Description
Dataset Source: Kaggle  
Dataset Name: **Cardiovascular Disease Dataset**  
Link: https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset

### **Dataset Size**
- **70,000 samples**
- **12 input features + target label**

### **Features**
| Feature        | Description                                      |
|----------------|--------------------------------------------------|
| age            | Age in days                                      |
| gender         | 1 – Female, 2 – Male                             |
| height         | Height in cm                                     |
| weight         | Weight in kg                                     |
| ap_hi          | Systolic blood pressure                          |
| ap_lo          | Diastolic blood pressure                         |
| cholesterol    | 1 – Normal, 2 – Above normal, 3 – Well above     |
| gluc           | 1 – Normal, 2 – Above normal, 3 – Well above     |
| smoke          | Binary (0/1)                                     |
| alco           | Alcohol consumption (0/1)                        |
| active         | Physical activity (0/1)                          |
| cardio         | Target variable (0 = No CVD, 1 = CVD)            |

---

## 4. Week-1 Exploration Summary
After exploring the dataset, the following observations were made:

### **1. Dataset contains 70k samples**
A large dataset improves model performance and reduces overfitting.

### **2. No missing values**
The dataset is clean and does not require imputation.

### **3. Some features have outliers**
Unrealistic values found in:
- Height  
- Weight  
- Blood pressure (ap_hi, ap_lo)

These outliers will be handled in Week-2.

### **4. Target is slightly imbalanced**
Class distribution for `cardio` is not perfectly equal.  
Handling imbalance may be required during model training.

### **5. Numerical features need scaling**
Different ranges (age in days vs blood pressure) require scaling.

### **6. Many categorical features**
Categorical columns (gender, cholesterol, glucose, smoke, alco, active)  
must be encoded properly for ML models.

---

## 5. Conclusion
Week-1 successfully provides:
- Problem definition  
- Dataset understanding  
- Initial EDA  
- Data issues identification  

In **Week-2**, we will perform:
- Data cleaning  
- Outlier handling  
- Encoding  
- Scaling  
- Full EDA visualizations  

---
