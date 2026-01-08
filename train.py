import numpy as np
import pandas as pd
import pickle
from model.LogisticRegression import LogisticRegression

# -----------------------------------------
# Load already-scaled data
# -----------------------------------------
X_train = pd.read_csv("data/X_train_final.csv")
X_test = pd.read_csv("data/X_test_final.csv")
y_train = pd.read_csv("data/y_train_final.csv").values.ravel()
y_test = pd.read_csv("data/y_test_final.csv").values.ravel()

# -----------------------------------------
# Train Logistic Regression (SCRATCH)
# -----------------------------------------
model = LogisticRegression(lr=0.005, n_iters=3000)
model.fit(X_train.values, y_train)

# -----------------------------------------
# Evaluate
# -----------------------------------------
def accuracy(y_true, y_pred):
    return np.mean(y_true == y_pred)

train_acc = accuracy(y_train, model.predict(X_train.values))
test_acc = accuracy(y_test, model.predict(X_test.values))

print(f"Train Accuracy: {train_acc:.4f}")
print(f"Test Accuracy: {test_acc:.4f}")

# -----------------------------------------
# Save Model
# -----------------------------------------
with open("model/logistic_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model and scaler saved successfully")
