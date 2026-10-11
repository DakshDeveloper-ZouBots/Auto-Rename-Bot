import os
import re
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

@Client.on_message(filters.command("autorename") & filters.private)
async def set_autorename_format(client: Client, message: Message):
    user_id = message.from_user.id
    await db.add_user(user_id)
    
    format_text = message.text.split(" ", 1)
    if len(format_text) < 2:
        settings = await db.get_user_settings(user_id)
        current_format = settings.get("autorename_format", "Devilman Crybaby - [S{season}-E{episode}] [{quality}] [{audio}] @Anime_Kyoto")
        await message.reply_text(
            "» ꜱᴇᴛᴜᴘ ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ ꜰᴏʀᴍᴀᴛ\n\n"
            "ᴠᴀʀɪᴀʙʟᴇꜱ :\n"
            "➲ `{season}` - ᴛᴏ ʀᴇᴘʟᴀᴄᴇ ꜱᴇᴀꜱᴏɴ\n"
            "➲ `{episode}` - ᴛᴏ ʀᴇᴘʟᴀᴄᴇ ᴇᴘɪꜱᴏᴅᴇ ɴᴜᴍʙᴇʀ\n"
            "➲ `{quality}` - ᴛᴏ ʀᴇᴘʟᴀᴄᴇ ǫᴜᴀʟɪᴛʏ\n"
            "➲ `{audio}` - ᴛᴏ ʀᴇᴘʟᴀᴄᴇ ᴀᴜᴅɪᴏ/ʟᴀɴɢᴜᴀɢᴇ\n\n"
            "‣ ꜰᴏʀ ᴇx:- `/autorename Devilman Crybaby - [S{season}-E{episode}] [{quality}] [{audio}] @Anime_Kyoto`\n\n"
            f"current format: `{current_format}`"
        )
        return
        
    new_format = format_text[1]
    await db.update_user_settings(user_id, "autorename_format", new_format)
    await message.reply_text(f"✅ **Auto-Rename format successfully saved!**\n\n`{new_format}`")

def extract_file_metadata(filename):
    # Extract Season (e.g., S1, Season 1)
    season_match = re.search(r"(?i)(?:s|season)\s*(\d+)", filename)
    season = season_match.group(1).zfill(2) if season_match else "01"
    
    # Extract Episode (e.g., Ep03, E03, Episode 3)
    ep_match = re.search(r"(?i)(?:ep?|episode)\s*(\d+)", filename)
    if not ep_match:
        num_match = re.search(r"[\s._-]+(\d{1,3})[\s._-]", filename)
        episode = num_match.group(1).zfill(2) if num_match else "01"
    else:
        episode = ep_match.group(1).zfill(2)
        
    # Extract Quality
    quality_match = re.search(r"(?i)(480p|720p|1080p|2160p|4K)", filename)
    quality = quality_match.group(1) if quality_match else "720p"
    
    # Extract Audio
    audio_match = re.search(r"(?i)(Dual Audio|Multi Audio|Hindi|English|Japanese|Tamil|Telugu)", filename)
    audio = audio_match.group(1) if audio_match else "Sub"
    
    return season, episode, quality, audio

@Client.on_message(filters.document | filters.video | filters.audio & filters.private)
async def auto_rename_workflow(client: Client, message: Message):
    user_id = message.from_user.id
    await db.add_user(user_id)
    
    settings = await db.get_user_settings(user_id)
    template = settings.get("autorename_format", "Devilman Crybaby - [S{season}-E{episode}] [{quality}] [{audio}] @Anime_Kyoto")
    
    media = message.document or message.video or message.audio
    if not media:
        return
        
    original_name = getattr(media, "file_name", "Video_File.mkv")
    logger.info(f"Auto-rename triggered for user {user_id} with file: '{original_name}'")
    
    # Extract metadata using regex parser
    season, episode, quality, audio = extract_file_metadata(original_name)
    
    # Replace format variables safely
    custom_name = template
    custom_name = custom_name.replace("{season}", season)
    custom_name = custom_name.replace("{episode}", episode)
    custom_name = custom_name.replace("{quality}", quality)
    custom_name = custom_name.replace("{audio}", audio)
    
    _, file_ext = os.path.splitext(original_name)
    if not custom_name.endswith(file_ext):
        custom_name += file_ext
        
    msg = await message.reply_text(f"🔄 Auto-renaming to:\n`{custom_name}`")
    
    async with process_semaphore:
        download_path = None
        output_path = None
        try:
            start_time = time.time()
            
            # FIX: Do not pass directory string to file_name. Let Pyrogram download to default path first, or use a valid file path.
            download_path = await client.download_media(
                message,
                progress=progress_for_pyrogram,
                progress_args=("📥 Wzgram Downloading...", msg, start_time)
            )
            
            if not download_path or not os.path.exists(download_path) or os.path.getsize(download_path) == 0:
                await msg.edit("❌ Failed to download file or file size is 0 bytes.")
                return

            logger.info(f"Successfully downloaded to {download_path} (Size: {os.path.getsize(download_path)} bytes)")
            
            # Create output path in downloads directory
            os.makedirs("downloads", exist_ok=True)
            output_path = os.path.join("downloads", f"{int(time.time())}_{custom_name}")
            
            # Move/Rename downloaded file to output path
            os.replace(download_path, output_path)
            logger.info(f"RENAMED file: '{original_name}' -> '{output_path}'")

            up_start = time.time()
            await msg.edit("📤 Wzgram uploading renamed file...")
            await client.send_document(
                chat_id=message.chat.id,
                document=output_path,
                caption=f"**{custom_name}**\n⚡ Powered by **Wzgram**",
                progress=progress_for_pyrogram,
                progress_args=("🚀 Wzgram Uploading...", msg, up_start)
            )
            await msg.delete()

        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_text(f"⚠️ Rate limited. Resumed after {e.value}s.")
        except Exception as e:
            logger.error(f"Error in auto-rename for user {user_id}: {e}")
            await msg.edit(f"⚠️ Error occurred: `{str(e)}`")
        finally:
            if download_path and os.path.exists(download_path):
                try: os.remove(download_path)
                except: pass
            if output_path and os.path.exists(output_path):
                try: os.remove(output_path)
                except: pass
