import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

if not API_ID or not API_HASH or not BOT_TOKEN:
    raise ValueError("❌ CRITICAL ERROR: API_ID, API_HASH, or BOT_TOKEN is missing in environment variables!")

ADMINS = [int(x) for x in os.environ.get("ADMINS", "").split()] if os.environ.get("ADMINS") else []
DB_URL = os.environ.get("DB_URL", "")
DB_NAME = os.environ.get("DB_NAME", "WzgramAutoRename")
PORT = int(os.environ.get("PORT", "8080"))
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0")) if os.environ.get("LOG_CHANNEL") else 0
