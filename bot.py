import logging
import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from pymongo import MongoClient
import os

from config import BOT_DEVELOPER, BOT_LINK, REGISTER_LINK, BOT_OWNER_ID, MONGO_URL, BOT_TOKEN

# ---------------- Logging ----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------- MongoDB ----------------
client = MongoClient(MONGO_URL)
db = client["broadcast_bot"]
chats_col = db["served_chats"]
users_col = db["served_users"]

# ---------------- Helper ----------------
def save_user_and_chat(user_id, chat_id):
    if chat_id:
        chats_col.update_one({"chat_id": chat_id}, {"$set": {"chat_id": chat_id}}, upsert=True)
    if user_id:
        users_col.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

# ---------------- /start ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    save_user_and_chat(user.id, chat.id)

    # -------- "ᴅιиg ᴅσиg" Animation --------
    vip = await update.message.reply_text("ᴅιиg ᴅσиg ꨄ︎❣️.....")
    await asyncio.sleep(0.2)
    await vip.edit_text("ᴅιиg ᴅσиg ꨄ︎.❣️....")
    await asyncio.sleep(0.2)
    await vip.edit_text("ᴅιиg ᴅσиg ꨄ︎..❣️...")
    await asyncio.sleep(0.2)
    await vip.edit_text("ᴅιиg ᴅσиg ꨄ︎...❣️..")
    await asyncio.sleep(0.2)
    await vip.edit_text("ᴅιиg ᴅσиg ꨄ︎....❣️.")
    await asyncio.sleep(0.2)
    await vip.edit_text("ᴅιиg ᴅσиg ꨄ︎.....❣️")
    await asyncio.sleep(0.3)

    # Delete the first animation message
    await vip.delete()

    # -------- START Animation --------
    start_msg = await update.message.reply_text("⚡ S")
    await asyncio.sleep(0.2)
    await start_msg.edit_text("⚡ 𝑆𝑇")
    await asyncio.sleep(0.2)
    await start_msg.edit_text("⚡ 𝑆𝑇𝐴")
    await asyncio.sleep(0.2)
    await start_msg.edit_text("⚡ 𝑆𝑇𝐴𝑅")
    await asyncio.sleep(0.2)
    await start_msg.edit_text("⚡ 𝑆𝑇𝐴𝑅𝑇")
    await asyncio.sleep(0.3)

    # Delete the START animation message as well
    await start_msg.delete()

    # -------- Welcome Video & Caption --------
    video_source = "https://envs.sh/F59.mp4"  # Replace with your valid video URL

    caption = (
    "╔══════════════════════╗\n"
    "   🎉🔥 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 🔥🎉\n"
    "        🌟 𝗧𝗙𝗚𝗣𝗟 𝟮𝟬𝟮𝟱 🌟\n"
    "╚══════════════════════╝\n\n"
    "⚡ *Tamil Friendship Group Premier League* ⚡\n\n"
    "📅 *22 – 30 Aug 2025*\n"
    "📍 Venue: [Tamil Friendship Group](https://t.me/group_friendship_tamil)\n\n"
    "🏏 Squad Size: *9–16 Players*\n"
    "✨ Captain + Vice Captain *Required*\n\n"
    "💬 *Play with 💖 Spirit 💖*\n"
    "🏆 *Win with Pride* 🏆\n"
    "🎊 *Celebrate with Friendship* 🎊\n\n"
    "⚡ Organization by [WhistleSquad](https://t.me/WhistleSquad)\n\n"
    f"👨‍💻 Developed by [{BOT_DEVELOPER}]({BOT_LINK})"
)

    keyboard = [
    [InlineKeyboardButton("📝 Click Here to Register", url=REGISTER_LINK)],
    [
        InlineKeyboardButton("WS × BST", url="https://t.me/BeastPaiyan"),
        InlineKeyboardButton("TFG × Doraemon", url="https://t.me/Rubesh_official_18")
    ],
    [InlineKeyboardButton("WhistleSquad", url="https://t.me/WhistleSquad")]
]

    try:
        await update.message.reply_video(
            video=video_source,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        logger.error(f"Failed to send video: {e}")
        await update.message.reply_text(
            f"{caption}\n\n⚠️ Could not send video. Please check your video source.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ---------------- /broadcast ----------------
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != BOT_OWNER_ID:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return

    if not context.args and not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ Usage: /broadcast [message or reply]\n\n"
            "Options:\n"
            "-pin → Pin message\n"
            "-pinloud → Pin with notification\n"
            "-user → Broadcast only to users\n"
            "-group → Broadcast only to groups\n"
            "-nobot → Skip sending to group chats"
        )
        return

    text = " ".join(context.args)
    flags = [w for w in text.split() if w.startswith("-")]
    message_text = " ".join([w for w in text.split() if not w.startswith("-")])

    if update.message.reply_to_message and not message_text:
        message_text = update.message.reply_to_message.text

    if not message_text:
        await update.message.reply_text("⚠️ No message to broadcast.")
        return

    results = []

    # Broadcast to groups
    if "-group" in flags:
        for chat in chats_col.find():
            chat_id = chat["chat_id"]
            try:
                sent = await context.bot.send_message(chat_id=chat_id, text=message_text)
                if "-pinloud" in flags:
                    await context.bot.pin_chat_message(chat_id=chat_id, message_id=sent.message_id, disable_notification=False)
                elif "-pin" in flags:
                    await context.bot.pin_chat_message(chat_id=chat_id, message_id=sent.message_id, disable_notification=True)
                results.append(f"👥 Sent to group {chat_id}")
            except Exception as e:
                logger.warning(f"Failed to send to group {chat_id}: {e}")
                results.append(f"❌ Group {chat_id}")

    # Broadcast to users
    if "-user" in flags:
        for user in users_col.find():
            uid = user["user_id"]
            try:
                await context.bot.send_message(chat_id=uid, text=message_text)
                results.append(f"👤 Sent to user {uid}")
            except Exception as e:
                logger.warning(f"Failed to send to user {uid}: {e}")
                results.append(f"❌ User {uid}")

    # Default: send to all chats if neither -user nor -group
    if "-user" not in flags and "-group" not in flags and "-nobot" not in flags:
        for chat in chats_col.find():
            chat_id = chat["chat_id"]
            try:
                sent = await context.bot.send_message(chat_id=chat_id, text=message_text)
                if "-pinloud" in flags:
                    await context.bot.pin_chat_message(chat_id=chat_id, message_id=sent.message_id, disable_notification=False)
                elif "-pin" in flags:
                    await context.bot.pin_chat_message(chat_id=chat_id, message_id=sent.message_id, disable_notification=True)
                results.append(f"✅ Sent to chat {chat_id}")
            except Exception as e:
                logger.warning(f"Failed to send to chat {chat_id}: {e}")
                results.append(f"❌ Chat {chat_id}")

    await update.message.reply_text("\n".join(results) or "⚠️ Nothing sent.")

# ---------------- Main ----------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.run_polling()

if __name__ == "__main__":
    main()
