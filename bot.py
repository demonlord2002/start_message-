import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from pymongo import MongoClient

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

    # Save user and chat in DB
    save_user_and_chat(user.id, chat.id)

    video_file_id = "BAACAgUAAxkBAAE56u1opzyL_P6k0YSwiMPPw8nYyeGvWwAClxwAAgQ9QVWe9qeVrkf5WjYE"

    caption = (
        "╔═══════════════════════════════╗\n"
        "🎇 *ＷＥＬＣＯＭＥ ＴＯ ＴＦＧＰＬ ２𝟶２５* 🎇\n"
        "✨ *Tamil Friendship Group Premier League* ✨\n"
        "╚═══════════════════════════════╝\n\n"
        "📅 *Opens:* 22 Aug 2025\n"
        "📅 *Closes:* 30 Aug 2025\n"
        "📍 *Venue:* @group_friendship_tamil\n\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "📝 *Registration Steps*\n"
        "✔ Fill Google Form\n"
        "✔ Captain + Vice Captain\n"
        "✔ Team Name\n"
        "✔ 9–16 Players\n\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "👥 *Squad Rules*\n"
        "✔ 9 Min – 16 Max\n"
        "✔ No Substitutes\n"
        "✔ All 16 are main players\n\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "💬 *“Play with spirit, win with pride, celebrate with friendship.”*\n\n"
        f"👨‍💻 *Bot Developed by* [{BOT_DEVELOPER}]({BOT_LINK})"
    )

    keyboard = [
        [InlineKeyboardButton("📝 Click Here to Register", url=REGISTER_LINK)],
        [InlineKeyboardButton("🦅 Whistle Squads", url="https://t.me/BeastPaiyan")],
        [InlineKeyboardButton("📢 Broadcasting", url="https://t.me/Rubesh_official_18")]
    ]

    # ✅ Fixed: Removed 'disable_web_page_preview' because it's invalid for reply_video
    await update.message.reply_video(
        video=video_file_id,
        caption=caption,
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

    # ---------------- Broadcast to group chats ----------------
    if "-nobot" not in flags:
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

    # ---------------- Broadcast to users ----------------
    if "-user" in flags:
        for user in users_col.find():
            uid = user["user_id"]
            try:
                await context.bot.send_message(chat_id=uid, text=message_text)
                results.append(f"👤 Sent to user {uid}")
            except Exception as e:
                logger.warning(f"Failed to send to user {uid}: {e}")
                results.append(f"❌ User {uid}")

    await update.message.reply_text("\n".join(results) or "⚠️ Nothing sent.")

# ---------------- Main ----------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.run_polling()

if __name__ == "__main__":
    main()
