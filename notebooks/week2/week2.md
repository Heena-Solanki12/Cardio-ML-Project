# Week 2 – Data Cleaning & Preprocessing

## Project Title
**Cardiovascular Disease Prediction using Machine Learning**

## Dataset
Cardiovascular Disease Dataset (Kaggle)

---

## Objective of Week 2
The objective of Week 2 is to prepare the raw healthcare dataset for machine learning model implementation. This includes data cleaning, handling outliers, feature engineering, categorical encoding, feature scaling, and creating train–test splits to ensure the dataset is clean, consistent, and model-ready.

---

## Step 1: Dataset Loading
The dataset is loaded using Pandas. Initial inspection is performed to understand the structure, columns, and data types.

**Outcome:**
- Dataset successfully loaded
- Initial shape and column names verified

---

## Step 2: Removal of Non-Predictive Features
The `id` column is removed (if present) as it does not contribute to prediction and may introduce noise.

**Reason:**
- `id` is only an identifier and has no predictive significance.

---

## Step 3: Age Transformation
The `age` feature is originally recorded in days.

**Actions Performed:**
- Converted age from days to years
- Dropped the original `age` column

**Reason:**
- Improves interpretability
- Suitable for feature scaling and modeling

---

## Step 4: Handling Invalid Blood Pressure Values
Blood pressure values are validated using medical constraints.

**Conditions Applied:**
- Systolic BP (`ap_hi`) between 50 and 250
- Diastolic BP (`ap_lo`) between 30 and 150
- Systolic BP greater than Diastolic BP

**Reason:**
- Removes medically impossible readings
- Improves model reliability

---

## Step 5: Handling Height and Weight Outliers
Extreme height and weight values are removed using logical boundaries.

**Ranges Applied:**
- Height: 120–220 cm
- Weight: 30–200 kg

**Reason:**
- Prevents distortion during feature scaling
- Removes data entry or measurement errors

---

## Step 6: Feature Engineering – BMI
Body Mass Index (BMI) is calculated using height and weight.

**Formula:**
BMI = weight (kg) / height² (m²)

**Actions Performed:**
- BMI feature added
- Extreme BMI values (<10 or >60) removed

**Reason:**
- BMI is a clinically important indicator for cardiovascular risk
- Enhances predictive performance

---

## Step 7: Encoding Categorical Variables

### Gender Encoding
- Female → 0
- Male → 1

### Cholesterol and Glucose Encoding
Ordinal encoding applied:
- Normal → 0
- Above Normal → 1
- Well Above Normal → 2

**Reason:**
- Converts categorical data into numeric form
- Preserves ordinal relationships

---

## Step 8: Binary Feature Validation
Lifestyle-related features (`smoke`, `alco`, `active`) are verified and retained as binary values (0/1).

---

## Step 9: Feature–Target Separation
The dataset is divided into:
- Features (X)
- Target variable (`cardio`)

**Reason:**
- Required for supervised learning

---

## Step 10: Train–Test Split
The dataset is split into training and testing sets.

**Configuration:**
- Training set: 80%
- Testing set: 20%
- Stratified split to preserve class distribution

**Reason:**
- Prevents data leakage
- Ensures fair evaluation

---

## Step 11: Feature Scaling
Numerical features are standardized using **StandardScaler**.

**Scaled Features:**
- Age (years)
- Height
- Weight
- Systolic BP
- Diastolic BP
- BMI

**Reason:**
- Required for gradient-based models like Logistic Regression
- Ensures stable and faster convergence

---

## Step 12: Saving Preprocessed Data
The final cleaned and preprocessed datasets are saved for:
- Model training (Week 3)
- Flask backend integration (Week 4–5)

**Files Generated:**
- `X_train_final.csv`
- `X_test_final.csv`
- `y_train_final.csv`
- `y_test_final.csv`

---

## Outcome of Week 2
By the end of Week 2:
- The dataset is free from invalid and noisy values
- Features are encoded and scaled
- Data is fully model-ready
- The preprocessing pipeline follows medical and academic standards

---

## Next Steps (Week 3)
- Implement Logistic Regression (from scratch)
- Train the model using preprocessed data
- Evaluate performance using accuracy, precision, recall, F1-score, and ROC curve
