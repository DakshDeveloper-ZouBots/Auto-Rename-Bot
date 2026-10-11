import os
import time
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from helper.database import db
from helper.utils import progress_for_pyrogram

logger = logging.getLogger("WzgramBot")
process_semaphore = asyncio.Semaphore(2)

@Client.on_message(filters.document | filters.video | filters.audio & filters.private)
async def auto_rename_files(client: Client, message: Message):
    user_id = message.from_user.id
    await db.add_user(user_id)
    
    media = message.document or message.video or message.audio
    if not media:
        return
        
    original_name = getattr(media, "file_name", "Downloaded_File")
    logger.info(f"Incoming media from user {user_id}. Filename: '{original_name}'")
    
    msg = await message.reply_text("🔄 Wzgram processing file download & rename workflow...")
    
    async with process_semaphore:
        download_path = None
        output_path = None
        try:
            start_time = time.time()
            download_path = await client.download_media(
                message,
                file_name="downloads/",
                progress=progress_for_pyrogram,
                progress_args=("📥 Wzgram Downloading...", msg, start_time)
            )
            
            if not download_path or not os.path.exists(download_path):
                logger.error(f"Failed to download file for user {user_id}")
                await msg.edit("❌ Failed to download file.")
                return

            logger.info(f"Successfully downloaded to {download_path}")
            dir_name, file_ext = os.path.splitext(download_path)
            custom_name = f"[Wzgram] {original_name}"
            output_path = os.path.join("downloads", f"Renamed_{int(time.time())}{file_ext}")
            
            os.rename(download_path, output_path)
            logger.info(f"RENAMED file: '{original_name}' -> '{output_path}'")

            up_start = time.time()
            await msg.edit("📤 Wzgram uploading renamed file...")
            await client.send_document(
                chat_id=message.chat.id,
                document=output_path,
                caption=f"**File:** `{original_name}`\n⚡ Powered by **Wzgram**",
                progress=progress_for_pyrogram,
                progress_args=("🚀 Wzgram Uploading...", msg, up_start)
            )
            logger.info(f"Successfully uploaded renamed file to chat {message.chat.id}")
            await msg.delete()

        except FloodWait as e:
            logger.warning(f"Telegram FloodWait encountered: sleeping for {e.value}s")
            await asyncio.sleep(e.value)
            await message.reply_text(f"⚠️ Rate limited. Resumed after {e.value}s.")
        except Exception as e:
            logger.error(f"Error processing file for user {user_id}: {e}")
            await msg.edit(f"⚠️ Error occurred: `{str(e)}`")
        finally:
            if download_path and os.path.exists(download_path):
                try: 
                    os.remove(download_path)
                    logger.info(f"Cleaned up temp download: {download_path}")
                except: pass
            if output_path and os.path.exists(output_path):
                try: 
                    os.remove(output_path)
                    logger.info(f"Cleaned up temp output: {output_path}")
                except: pass
