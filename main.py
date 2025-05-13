from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
import uvicorn
import csv
import joblib
from sklearn.ensemble import RandomForestClassifier
import numpy as np

app = FastAPI()

UPLOAD_DIR = "uploaded_videos"
DATA_FILE = "training_data.csv"
MODEL_FILE = "pnömotoraks_model.pkl"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
async def main_form():
    content = """
    <html>
        <head>
            <title>BT ve Vital Veri Yükleme</title>
        </head>
        <body>
            <h2>Toraks BT (AVI) Yükle ve Vital Verileri Gir</h2>
            <form action="/upload/" enctype="multipart/form-data" method="post">
                Video Dosyası: <input type="file" name="file"><br><br>
                SpO₂: <input type="text" name="spo2"><br>
                RR: <input type="text" name="rr"><br>
                HR: <input type="text" name="hr"><br>
                BP: <input type="text" name="bp"><br>
                Bilinç: <input type="text" name="bilinc"><br>
                Yaş: <input type="text" name="yas"><br>
                Cinsiyet: <input type="text" name="cinsiyet"><br>
                Uygulanan Tedavi (etiket): <input type="text" name="tedavi"><br><br>
                <input type="submit" value="Veriyi Kaydet">
            </form>
            <br>
            <form action="/train/" method="post">
                <input type="submit" value="Modeli Eğit">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=content)

@app.post("/upload/")
async def upload(
    file: UploadFile = File(...),
    spo2: str = Form(...),
    rr: str = Form(...),
    hr: str = Form(...),
    bp: str = Form(...),
    bilinc: str = Form(...),
    yas: str = Form(...),
    cinsiyet: str = Form(...),
    tedavi: str = Form(...)
):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(DATA_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([spo2, rr, hr, bp, bilinc, yas, cinsiyet, tedavi])

    return {"message": "Vaka ve video kaydedildi."}

@app.post("/train/")
async def train_model():
    if not os.path.exists(DATA_FILE):
        return {"message": "Henüz eğitim verisi bulunmuyor."}

    X, y = [], []
    with open(DATA_FILE, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                X.append([float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5])])
                y.append(row[7])
            except:
                continue

    model = RandomForestClassifier()
    model.fit(X, y)
    joblib.dump(model, MODEL_FILE)
    return {"message": "Model başarıyla eğitildi."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
