import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def train_and_save_model():
    # Generate dummy training data to simulate historical records
    np.random.seed(42)
    # Features: Water Level, Rainfall Rate, Soil Saturation, Temp
    X = np.random.rand(100, 4) * [100, 50, 100, 40]
    # Labels: 0 (Normal), 1 (Advisory), 2 (Warning), 3 (Severe Danger)
    y = np.random.choice([0, 1, 2, 3], 100)
    
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X, y)
    
    joblib.dump(model, "random_forest_flood_model.pkl")

if __name__ == "__main__":
    train_and_save_model()
