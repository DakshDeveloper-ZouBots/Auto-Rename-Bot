import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("API_ID", "36428426"))
API_HASH = os.environ.get("API_HASH", "30cba30aa38699e77ce264365e327528")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8793705801:AAHUin2Y9oI6Up8_fos4_O5RmNsVIeWIpV8")

if not API_ID or not API_HASH or not BOT_TOKEN:
    raise ValueError("❌ CRITICAL ERROR: API_ID, API_HASH, or BOT_TOKEN is missing in environment variables!")

ADMINS = [int(x) for x in os.environ.get("ADMINS", "7957802698").split()] if os.environ.get("ADMINS") else []
DB_URL = os.environ.get("DB_URL", "mongodb+srv://animekyoto:W5Itr6v2bZ3KpQF8@cluster0.trg5dtc.mongodb.net/?appName=Cluster0")
DB_NAME = os.environ.get("DB_NAME", "WzgramAutoRename")
PORT = int(os.environ.get("PORT", "8090"))
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1003912488328")) if os.environ.get("LOG_CHANNEL") else 0
