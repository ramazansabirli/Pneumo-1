import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from dotenv import load_dotenv
from loguru import logger
from datetime import datetime
from app.routes import router

# === Load environment variables ===
load_dotenv()

# === Logging Setup ===
LOG_PATH = os.getenv("LOG_PATH", "logs")
os.makedirs(LOG_PATH, exist_ok=True)
logger.add(
    os.path.join(LOG_PATH, f"ai_logs_{datetime.now().strftime('%Y%m%d')}.log"),
    rotation="500 MB",
    retention="30 days",
    compression="zip"
)

# === FastAPI Application Initialization ===
app = FastAPI(
    title=os.getenv("APP_TITLE", "Pnömotoraks AI Karar Destek Sistemi"),
    version=os.getenv("APP_VERSION", "2.0"),
    description=(
        "Bu uygulama, toraks BT videoları, vital bulgular ve klinik parametrelerle "
        "pnömotoraks tanısı ve tedavi yönetimi için yapay zeka destekli öneriler sunar. "
        "Derin öğrenme, klasik ML, görüntü işleme, NLP, açıklanabilirlik ve dashboard entegrasyonları içerir."
    ),
    contact={"name": "AI Medikal Takım", "email": "destek@aiproject.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    docs_url="/docs",
    redoc_url="/redoc"
)

# === Middlewares ===
app.add_middleware(GZipMiddleware, minimum_size=1024)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "very-secure-key"))
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# === Upload Path Setup ===
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploaded_videos")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

# === Include API Router ===
app.include_router(router)

# === Startup & Shutdown Hooks ===
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Uygulama başlatıldı: Yapay zeka sistemleri yükleniyor...")
    # Örnek: Model, tokenizer, DICOM parser, NLP pipe, SHAP yükleme
    try:
        from transformers import pipeline
        app.nlp_pipe = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        logger.info("🤖 NLP pipeline yüklendi (transformers)")
    except Exception as e:
        logger.warning(f"NLP pipeline yüklenemedi: {e}")

    try:
        import shap
        app.shap_explainer = "Hazır SHAP açıklama sistemi (dummy)"  # Placeholder
        logger.info("🧠 SHAP açıklayıcı hazır (örnek)")
    except Exception as e:
        logger.warning(f"SHAP yüklenemedi: {e}")

    # Gelecekte: DICOM, LIME, AutoML, Gradio, Streamlit, ONNX yüklemeleri yapılabilir

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🔻 Uygulama kapatılıyor...")
