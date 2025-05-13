from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import numpy as np
import json

def evaluate_model(model, X_test, y_test, labels=None, save_path="evaluation_report.json"):
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    conf_matrix = confusion_matrix(y_test, y_pred).tolist()
    roc_score = None
    try:
        if len(set(y_test)) == 2:
            y_prob = model.predict_proba(X_test)[:, 1]
            roc_score = roc_auc_score(y_test, y_prob)
    except:
        pass

    result = {
        "classification_report": report,
        "confusion_matrix": conf_matrix,
        "roc_auc_score": roc_score
    }
    with open(save_path, "w") as f:
        json.dump(result, f, indent=4)
    return result
