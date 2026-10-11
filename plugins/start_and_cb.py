from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from helper.database import db

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    user_id = message.from_user.id
    await db.add_user(user_id)
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🟢 Updates Channel", url="https://t.me/wzgram"), InlineKeyboardButton("🔵 Support Group", url="https://t.me/wzgram")],
        [InlineKeyboardButton("⚙️ Bot Settings", callback_data="settings"), InlineKeyboardButton("❓ Help Guide", callback_data="help")],
        [InlineKeyboardButton("🔴 Close Menu", callback_data="close")]
    ])
    
    await message.reply_text(
        f"👋 Hello **{message.from_user.first_name}**!\n\n"
        "⚡ Welcome to **Wzgram Auto Rename Bot**.\n"
        "Send me any file or video to test lightning-fast renaming!",
        reply_markup=keyboard
    )

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    data = query.data
    if data == "settings":
        settings = await db.get_user_settings(query.from_user.id)
        caption = settings.get("caption", "None")
        thumb = "Set" if settings.get("thumbnail") else "Not Set"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🖼️ View Thumbnail", callback_data="viewthumb"), InlineKeyboardButton("🗑️ Delete Thumbnail", callback_data="delthumb")],
            [InlineKeyboardButton("📝 See Caption", callback_data="seecaption"), InlineKeyboardButton("🔙 Back to Home", callback_data="start")]
        ])
        await query.message.edit_text(f"⚙️ **Wzgram User Settings:**\n\n• Thumbnail: `{thumb}`\n• Custom Caption: `{caption}`", reply_markup=keyboard)
        
    elif data == "help":
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Home", callback_data="start")]])
        await query.message.edit_text("❓ **Wzgram Help Menu:**\n\n• Send any file/video to auto-rename.\n• Use `/metadata` to set custom metadata.\n• Use `/set_caption` for custom captions.\n• Admins can use `/log` to download execution logs.", reply_markup=keyboard)
        
    elif data == "start":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🟢 Updates Channel", url="https://t.me/wzgram"), InlineKeyboardButton("🔵 Support Group", url="https://t.me/wzgram")],
            [InlineKeyboardButton("⚙️ Bot Settings", callback_data="settings"), InlineKeyboardButton("❓ Help Guide", callback_data="help")],
            [InlineKeyboardButton("🔴 Close Menu", callback_data="close")]
        ])
        await query.message.edit_text(f"👋 Welcome back! Send me any file or video to auto-rename.", reply_markup=keyboard)
    elif data == "close":
        await query.message.delete()
    elif data == "viewthumb":
        await query.answer("Thumbnail feature active.", show_alert=True)
    elif data == "delthumb":
        await db.update_user_settings(query.from_user.id, "thumbnail", None)
        await query.answer("Thumbnail deleted successfully!", show_alert=True)
    elif data == "seecaption":
        settings = await db.get_user_settings(query.from_user.id)
        await query.answer(f"Caption: {settings.get('caption', 'None')}", show_alert=True)
