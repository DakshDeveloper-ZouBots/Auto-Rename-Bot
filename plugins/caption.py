from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import db

@Client.on_message(filters.command("set_caption") & filters.private)
async def set_caption_handler(client: Client, message: Message):
    user_id = message.from_user.id
    await db.add_user(user_id)
    
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text("❌ Please provide a caption! Example:\n`/set_caption File: {filename}`")
        return
        
    caption = args[1]
    await db.update_user_settings(user_id, "caption", caption)
    await message.reply_text("✅ Custom caption saved successfully!")

@Client.on_message(filters.command("see_caption") & filters.private)
async def see_caption_handler(client: Client, message: Message):
    user_id = message.from_user.id
    settings = await db.get_user_settings(user_id)
    caption = settings.get("caption", "No custom caption set.")
    await message.reply_text(f"📝 **Your Custom Caption:**\n\n`{caption}`")

@Client.on_message(filters.command("del_caption") & filters.private)
async def del_caption_handler(client: Client, message: Message):
    user_id = message.from_user.id
    await db.update_user_settings(user_id, "caption", None)
    await message.reply_text("🗑️ Custom caption deleted successfully!")
