import shap
import joblib
import numpy as np
import pandas as pd
import os

MODEL_FILE = "pnömotoraks_model.pkl"

def explain_prediction(instance_features: list, feature_names: list = None):
    """
    SHAP ile açıklama döndürür (özellik katkıları)
    """
    if not os.path.exists(MODEL_FILE):
        return {"status": "error", "message": "Model dosyası yok."}

    model = joblib.load(MODEL_FILE)
    explainer = shap.Explainer(model)
    shap_values = explainer([instance_features])

    return {
        "status": "success",
        "shap_values": shap_values[0].values.tolist(),
        "base_value": shap_values[0].base_values,
        "feature_names": feature_names or [f"f{i}" for i in range(len(instance_features))]
    }
