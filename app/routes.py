from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Optional
from app.services.video_processing import extract_video_features
from app.services.ml_model import train_model_from_csv, predict_treatment_from_input
import os
import shutil

router = APIRouter()

UPLOAD_DIR = "uploaded_videos"

@router.post("/upload/")
async def upload_video(hasta_id: str = Form(...), file: UploadFile = File(...)):
    """Video dosyasını hasta ID ile kaydet"""
    filename = f"{hasta_id}.avi"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"status": "success", "message": f"Video {filename} olarak kaydedildi."}

@router.post("/train/")
async def train():
    """CSV ve videolarla modeli eğit"""
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
    """Hasta verileriyle tedavi önerisi yap"""
    result = predict_treatment_from_input(hasta_id, spo2, rr, hr, bp, bilinc, yas)
    return JSONResponse(content=result)

@router.post("/explain/")
async def explain_ai(hasta_id: str = Form(...)):
    """SHAP/LIME ile açıklama yapılır (örnek/dummy)"""
    return JSONResponse(content={
        "status": "success",
        "explanation": f"{hasta_id} için SHAP açıklamaları burada gösterilecek (örnek)"
    })

@router.post("/classify-text/")
async def classify_text(input_text: str = Form(...), labels: str = Form(...)):
    """Transformers ile metin sınıflandırma"""
    try:
        candidate_labels = [l.strip() for l in labels.split(",")]
        result = router.app.nlp_pipe(input_text, candidate_labels)
        return {"status": "success", "labels": result["labels"], "scores": result["scores"]}
    except Exception as e:
        return {"status": "error", "message": f"NLP sınıflandırma başarısız: {e}"}

@router.get("/health/")
async def health_check():
    return {"status": "running", "message": "Pnömotoraks AI API aktif"}
