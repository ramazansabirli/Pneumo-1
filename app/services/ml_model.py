import os
import csv
import joblib
from sklearn.ensemble import RandomForestClassifier
from app.services.video_processing import extract_video_features

DATA_FILE = "training_data.csv"
MODEL_FILE = "pnömotoraks_model.pkl"
UPLOAD_DIR = "uploaded_videos"

def train_model_from_csv():
    if not os.path.exists(DATA_FILE):
        return {"status": "error", "message": "Veri dosyası yok."}

    X, y = [], []
    with open(DATA_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            hasta_id = row["HastaID"]
            video_path = os.path.join(UPLOAD_DIR, f"{hasta_id}.avi")
            if not os.path.exists(video_path):
                continue
            try:
                video_feats = extract_video_features(video_path)
                vital_feats = [float(row[col]) for col in ["SpO2", "RR", "HR", "BP", "Bilinç", "Yaş"]]
                X.append(vital_feats + video_feats)
                y.append(row["Tedavi"])
            except Exception:
                continue

    if len(X) < 10:
        return {"status": "error", "message": "Yeterli eğitim verisi yok."}

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    joblib.dump(model, MODEL_FILE)
    return {"status": "success", "message": "Model eğitildi."}

def predict_treatment_from_input(hasta_id, spo2, rr, hr, bp, bilinc, yas):
    if not os.path.exists(MODEL_FILE):
        return {"status": "error", "message": "Model bulunamadı."}

    video_path = os.path.join(UPLOAD_DIR, f"{hasta_id}.avi")
    if not os.path.exists(video_path):
        return {"status": "error", "message": "Video bulunamadı."}

    video_feats = extract_video_features(video_path)
    vital_feats = [spo2, rr, hr, bp, bilinc, yas]
    full_input = [vital_feats + video_feats]

    model = joblib.load(MODEL_FILE)
    prediction = model.predict(full_input)

    return {"status": "success", "tedavi_önerisi": prediction[0]}
