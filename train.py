import numpy as np
import pandas as pd
import pickle
import json
from datetime import datetime
from model.LogisticRegression import LogisticRegression

# ============================================================================
# PERFORMANCE METRICS FUNCTIONS
# ============================================================================

def accuracy(y_true, y_pred):
    """Calculate accuracy score"""
    return np.mean(y_true == y_pred)

def precision(y_true, y_pred):
    """Calculate precision (positive predictive value)"""
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    return tp / (tp + fp) if (tp + fp) > 0 else 0.0

def recall(y_true, y_pred):
    """Calculate recall (sensitivity, true positive rate)"""
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    return tp / (tp + fn) if (tp + fn) > 0 else 0.0

def f1_score(y_true, y_pred):
    """Calculate F1 score (harmonic mean of precision and recall)"""
    prec = precision(y_true, y_pred)
    rec = recall(y_true, y_pred)
    return 2 * (prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

def specificity(y_true, y_pred):
    """Calculate specificity (true negative rate)"""
    tn = np.sum((y_true == 0) & (y_pred == 0))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    return tn / (tn + fp) if (tn + fp) > 0 else 0.0

def confusion_matrix(y_true, y_pred):
    """Calculate confusion matrix"""
    tp = np.sum((y_true == 1) & (y_pred == 1))
    tn = np.sum((y_true == 0) & (y_pred == 0))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    return {"TP": int(tp), "TN": int(tn), "FP": int(fp), "FN": int(fn)}

def roc_auc_score(y_true, y_proba):
    """Calculate ROC AUC score"""
    # Sort by predicted probability
    desc_score_indices = np.argsort(y_proba)[::-1]
    y_true_sorted = y_true[desc_score_indices]
    
    # Calculate TPR and FPR at different thresholds
    tpr_list = []
    fpr_list = []
    
    n_pos = np.sum(y_true == 1)
    n_neg = np.sum(y_true == 0)
    
    tp = 0
    fp = 0
    
    for i in range(len(y_true_sorted)):
        if y_true_sorted[i] == 1:
            tp += 1
        else:
            fp += 1
        
        tpr = tp / n_pos if n_pos > 0 else 0
        fpr = fp / n_neg if n_neg > 0 else 0
        
        tpr_list.append(tpr)
        fpr_list.append(fpr)
    
    # Calculate AUC using trapezoidal rule
    auc = 0.0
    for i in range(1, len(fpr_list)):
        auc += (fpr_list[i] - fpr_list[i-1]) * (tpr_list[i] + tpr_list[i-1]) / 2
    
    return auc

def classification_report(y_true, y_pred, y_proba=None):
    """Generate comprehensive classification report"""
    report = {
        "accuracy": accuracy(y_true, y_pred),
        "precision": precision(y_true, y_pred),
        "recall": recall(y_true, y_pred),
        "f1_score": f1_score(y_true, y_pred),
        "specificity": specificity(y_true, y_pred),
        "confusion_matrix": confusion_matrix(y_true, y_pred)
    }
    
    if y_proba is not None:
        report["roc_auc"] = roc_auc_score(y_true, y_proba)
    
    return report

def check_overfitting(train_metrics, test_metrics, threshold=0.05):
    """
    Check for overfitting by comparing train and test metrics
    
    Returns:
        status: 'good', 'overfitting', or 'underfitting'
        analysis: detailed explanation
    """
    train_acc = train_metrics['accuracy']
    test_acc = test_metrics['accuracy']
    
    diff = train_acc - test_acc
    
    if diff > threshold:
        status = 'overfitting'
        severity = 'High' if diff > 0.15 else 'Moderate' if diff > 0.10 else 'Mild'
        analysis = {
            "status": status,
            "severity": severity,
            "train_test_gap": float(diff),
            "explanation": f"Model shows {severity.lower()} overfitting. Training accuracy ({train_acc:.4f}) "
                          f"is significantly higher than test accuracy ({test_acc:.4f}). "
                          f"The model may be memorizing training data rather than learning general patterns.",
            "recommendations": [
                "Consider reducing model complexity",
                "Add regularization (L1 or L2)",
                "Increase training data if possible",
                "Use cross-validation for more robust evaluation",
                "Apply early stopping during training"
            ]
        }
    elif train_acc < 0.65 and test_acc < 0.65:
        status = 'underfitting'
        analysis = {
            "status": status,
            "severity": "High",
            "train_test_gap": float(diff),
            "explanation": f"Model shows underfitting. Both training ({train_acc:.4f}) and test "
                          f"accuracy ({test_acc:.4f}) are low. The model is too simple to capture "
                          f"the underlying patterns in the data.",
            "recommendations": [
                "Increase model complexity",
                "Add more relevant features",
                "Try polynomial features or feature engineering",
                "Increase number of training iterations",
                "Check if learning rate is appropriate",
                "Consider more sophisticated algorithms"
            ]
        }
    else:
        status = 'good'
        analysis = {
            "status": status,
            "severity": "None",
            "train_test_gap": float(diff),
            "explanation": f"Model shows good generalization. Training accuracy ({train_acc:.4f}) "
                          f"and test accuracy ({test_acc:.4f}) are similar, indicating the model "
                          f"has learned meaningful patterns without overfitting.",
            "recommendations": [
                "Model is performing well",
                "Continue monitoring on new data",
                "Consider ensemble methods for improvement",
                "Fine-tune hyperparameters for marginal gains"
            ]
        }
    
    return analysis

def print_metrics(metrics, dataset_name):
    """Pretty print metrics"""
    print(f"\n{'='*60}")
    print(f"{dataset_name.upper()} METRICS")
    print(f"{'='*60}")
    print(f"Accuracy:    {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
    print(f"Precision:   {metrics['precision']:.4f} ({metrics['precision']*100:.2f}%)")
    print(f"Recall:      {metrics['recall']:.4f} ({metrics['recall']*100:.2f}%)")
    print(f"F1-Score:    {metrics['f1_score']:.4f}")
    print(f"Specificity: {metrics['specificity']:.4f} ({metrics['specificity']*100:.2f}%)")
    
    if 'roc_auc' in metrics:
        print(f"ROC-AUC:     {metrics['roc_auc']:.4f}")
    
    print(f"\nConfusion Matrix:")
    cm = metrics['confusion_matrix']
    print(f"  True Positives:  {cm['TP']:>6}")
    print(f"  True Negatives:  {cm['TN']:>6}")
    print(f"  False Positives: {cm['FP']:>6}")
    print(f"  False Negatives: {cm['FN']:>6}")
    print(f"{'='*60}\n")

# ============================================================================
# MAIN TRAINING SCRIPT
# ============================================================================

def main():
    print("\n" + "="*70)
    print("CARDIOVASCULAR DISEASE PREDICTION - MODEL TRAINING")
    print("="*70)
    print(f"Training started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Load data
    print("📂 Loading preprocessed data...")
    try:
        X_train = pd.read_csv("data/X_train_final.csv")
        X_test = pd.read_csv("data/X_test_final.csv")
        y_train = pd.read_csv("data/y_train_final.csv").values.ravel()
        y_test = pd.read_csv("data/y_test_final.csv").values.ravel()
        
        print(f"✅ Data loaded successfully")
        print(f"   Training samples: {len(X_train)}")
        print(f"   Test samples: {len(X_test)}")
        print(f"   Features: {X_train.shape[1]}")
        print(f"   Training class distribution: {np.sum(y_train==0)} negative, {np.sum(y_train==1)} positive")
        print(f"   Test class distribution: {np.sum(y_test==0)} negative, {np.sum(y_test==1)} positive")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return
    
    # Initialize and train model
    print("\n🤖 Initializing Logistic Regression model...")
    print("   Hyperparameters:")
    print("   - Learning Rate: 0.005")
    print("   - Iterations: 3000")
    print("   - Algorithm: Gradient Descent")
    
    model = LogisticRegression(lr=0.005, n_iters=3000)
    
    print("\n🔄 Training model...")
    print("   This may take a few minutes...\n")
    
    model.fit(X_train.values, y_train)
    
    print("✅ Model training completed!\n")
    
    # Make predictions
    print("📊 Generating predictions...")
    train_pred = model.predict(X_train.values)
    test_pred = model.predict(X_test.values)
    
    train_proba = model.predict_proba(X_train.values)[:, 1]
    test_proba = model.predict_proba(X_test.values)[:, 1]
    
    # Calculate metrics
    print("📈 Calculating performance metrics...\n")
    train_metrics = classification_report(y_train, train_pred, train_proba)
    test_metrics = classification_report(y_test, test_pred, test_proba)
    
    # Print metrics
    print_metrics(train_metrics, "Training Set")
    print_metrics(test_metrics, "Test Set")
    
    # Analyze overfitting/underfitting
    print("🔍 Analyzing Model Fit...")
    fit_analysis = check_overfitting(train_metrics, test_metrics)
    
    print(f"\n{'='*60}")
    print("MODEL FIT ANALYSIS")
    print(f"{'='*60}")
    print(f"Status: {fit_analysis['status'].upper()}")
    print(f"Severity: {fit_analysis['severity']}")
    print(f"Train-Test Gap: {fit_analysis['train_test_gap']:.4f}")
    print(f"\n{fit_analysis['explanation']}")
    print(f"\nRecommendations:")
    for i, rec in enumerate(fit_analysis['recommendations'], 1):
        print(f"  {i}. {rec}")
    print(f"{'='*60}\n")
    
    # Save model
    print("💾 Saving model...")
    try:
        with open("model/logistic_model.pkl", "wb") as f:
            pickle.dump(model, f)
        print("✅ Model saved to: model/logistic_model.pkl")
    except Exception as e:
        print(f"❌ Error saving model: {e}")
    
    # Save comprehensive report
    report = {
        "training_info": {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "algorithm": "Logistic Regression (Custom Implementation)",
            "learning_rate": 0.005,
            "iterations": 3000,
            "training_samples": int(len(X_train)),
            "test_samples": int(len(X_test)),
            "n_features": int(X_train.shape[1])
        },
        "training_metrics": {
            "accuracy": float(train_metrics['accuracy']),
            "precision": float(train_metrics['precision']),
            "recall": float(train_metrics['recall']),
            "f1_score": float(train_metrics['f1_score']),
            "specificity": float(train_metrics['specificity']),
            "roc_auc": float(train_metrics['roc_auc']),
            "confusion_matrix": train_metrics['confusion_matrix']
        },
        "test_metrics": {
            "accuracy": float(test_metrics['accuracy']),
            "precision": float(test_metrics['precision']),
            "recall": float(test_metrics['recall']),
            "f1_score": float(test_metrics['f1_score']),
            "specificity": float(test_metrics['specificity']),
            "roc_auc": float(test_metrics['roc_auc']),
            "confusion_matrix": test_metrics['confusion_matrix']
        },
        "model_analysis": fit_analysis,
        "feature_info": {
            "numerical_features": [
                "age (scaled)",
                "height (scaled)",
                "weight (scaled)",
                "systolic_bp (scaled)",
                "diastolic_bp (scaled)",
                "bmi (scaled)"
            ],
            "categorical_features": [
                "gender",
                "cholesterol",
                "glucose",
                "smoking",
                "alcohol",
                "physical_activity"
            ]
        }
    }
    
    print("\n📄 Saving comprehensive report...")
    try:
        with open("model/training_report.json", "w") as f:
            json.dump(report, f, indent=2)
        print("✅ Report saved to: model/training_report.json")
    except Exception as e:
        print(f"❌ Error saving report: {e}")
    
    # Summary
    print(f"\n{'='*70}")
    print("TRAINING SUMMARY")
    print(f"{'='*70}")
    print(f"✅ Model training completed successfully")
    print(f"✅ Test Accuracy: {test_metrics['accuracy']:.4f} ({test_metrics['accuracy']*100:.2f}%)")
    print(f"✅ Test ROC-AUC: {test_metrics['roc_auc']:.4f}")
    print(f"✅ Model Status: {fit_analysis['status'].upper()}")
    print(f"✅ Files saved:")
    print(f"   - model/logistic_model.pkl")
    print(f"   - model/training_report.json")
    print(f"\n🎉 All operations completed successfully!")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()