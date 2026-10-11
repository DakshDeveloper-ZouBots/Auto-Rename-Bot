from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import db

@Client.on_message(filters.command("metadata") & filters.private)
async def metadata_handler(client: Client, message: Message):
    user_id = message.from_user.id
    await db.add_user(user_id)
    
    command_args = message.text.split(" ", 1)
    if len(command_args) < 2:
        settings = await db.get_user_settings(user_id)
        current_meta = settings.get("metadata", "Not Set")
        await message.reply_text(
            f"🏷️ **Wzgram Metadata Title:** `{current_meta}`\n\n"
            "To set custom metadata, use:\n`/metadata Your_Metadata_Title`"
        )
        return
        
    new_meta = command_args[1]
    await db.update_user_settings(user_id, "metadata", new_meta)
    await message.reply_text(f"✅ Wzgram metadata successfully updated to: `{new_meta}`")
