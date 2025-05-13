import os
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.routes import router
from dotenv import load_dotenv
from loguru import logger
from datetime import datetime

# === Load environment variables ===
load_dotenv()

# === Logging Setup ===
log_path = os.getenv("LOG_PATH", "logs")
os.makedirs(log_path, exist_ok=True)
log_file = os.path.join(log_path, f"app_{datetime.now().strftime('%Y%m%d')}.log")
logger.add(log_file, rotation="1 day", retention="7 days", compression="zip")

# === App Initialization ===
app = FastAPI(
    title=os.getenv("APP_TITLE", "Pnömotoraks AI Modüler Sistem"),
    version=os.getenv("APP_VERSION", "2.0"),
    description="""Pnömotoraks tanısı ve tedavi yönetimi için video + vital veriye dayalı yapay zeka destekli karar sistemi.""",
    contact={
        "name": "AI Medikal Takım",
        "email": "destek@aiproject.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc"
)

# === Middleware Setup ===
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "dev-secret"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Upload Directory for Static Access ===
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploaded_videos")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

# === API Routes ===
app.include_router(router)

# === Lifecycle Events ===
@app.on_event("startup")
async def on_startup():
    logger.info("✅ Pnömotoraks AI sistemi başarıyla başlatıldı.")
    # Future: preload model, initialize cache, etc.

@app.on_event("shutdown")
async def on_shutdown():
    logger.info("🛑 Pnömotoraks AI sistemi durduruluyor...")
