import numpy as np

def sigmoid(x):
    x = np.clip(x, -20, 20)
    return 1 / (1 + np.exp(-x))

class LogisticRegression():

    def __init__(self, lr=0.005, n_iters=3000):
        self.lr = lr
        self.n_iters = n_iters
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.n_iters):
            linear_pred = np.dot(X, self.weights) + self.bias
            predictions = sigmoid(linear_pred)

            dw = (1/n_samples) * np.dot(X.T, (predictions - y))
            db = (1/n_samples) * np.sum(predictions - y)

            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict_proba(self, X):
        linear_pred = np.dot(X, self.weights) + self.bias
        return sigmoid(linear_pred)

    def predict(self, X):
        probs = self.predict_proba(X)
        return (probs >= 0.5).astype(int)
