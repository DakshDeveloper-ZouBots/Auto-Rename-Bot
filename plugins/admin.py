import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from config import ADMINS

logger = logging.getLogger("WzgramBot")

@Client.on_message(filters.command("status") & filters.private)
async def status_handler(client: Client, message: Message):
    if ADMINS and message.from_user.id not in ADMINS:
        return
    await message.reply_text("🤖 **Wzgram Status:** All systems operational and running smoothly.")

@Client.on_message(filters.command("restart") & filters.private)
async def restart_handler(client: Client, message: Message):
    if ADMINS and message.from_user.id not in ADMINS:
        return
    await message.reply_text("🔄 Restarting Wzgram bot server...")
    import sys
    os.execv(sys.executable, ['python'] + sys.argv)

@Client.on_message(filters.command("log") & filters.private)
async def send_log_file(client: Client, message: Message):
    if ADMINS and message.from_user.id not in ADMINS:
        return
        
    log_file_path = "wzgram_bot.log"
    if not os.path.exists(log_file_path):
        await message.reply_text("⚠️ No `wzgram_bot.log` file found on disk yet. Send some files or interact with the bot first!")
        return
        
    logger.info(f"Admin {message.from_user.id} requested the bot log file via /log.")
    await message.reply_document(
        document=log_file_path,
        caption="📋 **Wzgram Bot Execution Logs**\nLive activity stream & file renaming logs."
    )
