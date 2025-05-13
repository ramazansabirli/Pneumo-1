import pandas as pd
import os

def save_case_to_csv(data: dict, file_path: str = "prediction_results.csv"):
    df = pd.DataFrame([data])
    if os.path.exists(file_path):
        df.to_csv(file_path, mode="a", index=False, header=False)
    else:
        df.to_csv(file_path, index=False)
