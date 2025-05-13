import os
from dotenv import load_dotenv

load_dotenv()

APP_TITLE = os.getenv("APP_TITLE", "Pnömotoraks AI CDS")
APP_VERSION = os.getenv("APP_VERSION", "2.0")
SESSION_SECRET = os.getenv("SESSION_SECRET", "very-secure-key")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploaded_videos")
LOG_DIR = os.getenv("LOG_PATH", "logs")
