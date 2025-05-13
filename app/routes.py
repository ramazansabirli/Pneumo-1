from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.services.video_processing import extract_video_features
from app.services.ml_model import train_model_from_csv, predict_treatment_from_input
import os
import shutil

router = APIRouter()

UPLOAD_DIR = "uploaded_videos"

@router.post("/upload/")
async def upload_video(hasta_id: str = Form(...), file: UploadFile = File(...)):
    filename = f"{hasta_id}.avi"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"message": f"Video {filename} olarak kaydedildi."}

@router.post("/train/")
async def train():
    result = train_model_from_csv()
    return JSONResponse(content=result)

@router.post("/predict/")
async def predict(
    hasta_id: str = Form(...),
    spo2: float = Form(...),
    rr: float = Form(...),
    hr: float = Form(...),
    bp: float = Form(...),
    bilinc: float = Form(...),
    yas: float = Form(...)
):
    result = predict_treatment_from_input(hasta_id, spo2, rr, hr, bp, bilinc, yas)
    return JSONResponse(content=result)
