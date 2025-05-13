import os
import sys
from datetime import datetime
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from dotenv import load_dotenv
from loguru import logger
from app.routes import router

# === Load environment ===
load_dotenv()
APP_NAME = os.getenv("APP_TITLE", "Pnömotoraks AI CDS")
APP_VERSION = os.getenv("APP_VERSION", "2.0")
SESSION_SECRET = os.getenv("SESSION_SECRET", "very-secure-key")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploaded_videos")
LOG_DIR = os.getenv("LOG_PATH", "logs")

# === Logging with loguru ===
os.makedirs(LOG_DIR, exist_ok=True)
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add(
    os.path.join(LOG_DIR, f"runtime_{datetime.now().strftime('%Y%m%d')}.log"),
    rotation="1 week",
    retention="30 days",
    compression="zip",
    enqueue=True,
    backtrace=True,
    diagnose=True
)

# === Initialize FastAPI ===
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=(
        "Görüntü işleme, vital parametre ve yapay zeka destekli pnömotoraks "
        "tanısı ve tedavi yönlendirme sistemi. SHAP, NLP, Streamlit ve Docker desteklidir."
    ),
    contact={"name": "AI Medikal Takım", "email": "destek@aiproject.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    docs_url="/docs",
    redoc_url="/redoc"
)

# === Middleware Setup ===
app.add_middleware(GZipMiddleware, minimum_size=1024)
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)
app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

# === Static Directory for Uploaded Files ===
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

# === API Routing ===
app.include_router(router)

# === Startup & Shutdown Hooks ===
@app.on_event("startup")
async def startup_event():
    logger.info("🧠 Yapay Zeka Karar Destek Sistemi başlatılıyor...")
    try:
        from transformers import pipeline
        app.nlp_pipe = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        logger.success("🔠 NLP modeli başarıyla yüklendi (transformers)")
    except Exception as e:
        logger.warning(f"NLP yükleme hatası: {e}")

    try:
        import shap
        app.shap_explainer = "SHAP açıklama altyapısı hazır (placeholder)"
        logger.success("📊 SHAP altyapısı aktif")
    except Exception as e:
        logger.warning(f"SHAP yüklenemedi: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🔻 Sistem kapatılıyor... Oturumlar sonlandırıldı.")
