import numpy as np
from sklearn.ensemble import IsolationForest
import joblib  # For saving/loading model

def train_model(X_train):
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(X_train)
    joblib.dump(model, 'models/isolation_forest.pkl')
    return model

def load_model():
    return joblib.load('models/isolation_forest.pkl')

def predict(model, transaction_features):
    score = model.decision_function([transaction_features])[0]
    return score


if __name__ == "__main__":
    # Example synthetic feature vectors: [amount, velocity, hour]
    X_train = np.array([
        [100, 1, 10],
        [150, 2, 11],
        [120, 1, 14],
        [130, 3, 9],
        [90, 1, 13]
    ])
    model = train_model(X_train)
    test_tx = [4000, 5, 3]
    print("Anomaly score:", predict(model, test_tx))
