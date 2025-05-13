import joblib
import os
from datetime import datetime

def save_model(model, base_dir="models"):
    os.makedirs(base_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"model_{timestamp}.pkl"
    path = os.path.join(base_dir, filename)
    joblib.dump(model, path)
    return path
