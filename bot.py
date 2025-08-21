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

    # -------- Animation Effect --------
    vip = await update.message.reply_text("**ᴅιиg ᴅσиg ꨄ︎❣️.....**")
    await vip.edit_text("**ᴅιиg ᴅσиg ꨄ︎.❣️....**")
    await vip.edit_text("**ᴅιиg ᴅσиg ꨄ︎..❣️...**")
    await vip.edit_text("**ᴅιиg ᴅσиg ꨄ︎...❣️..**")
    await vip.edit_text("**ᴅιиg ᴅσиg ꨄ︎....❣️.**")
    await vip.edit_text("**ᴅιиg ᴅσиg ꨄ︎.....❣️**")
    await vip.delete()

    vips = await update.message.reply_text("**⚡ѕ**")
    await asyncio.sleep(0.1)
    await vips.edit_text("**⚡ѕт**")
    await vips.edit_text("**⚡ѕтα**")
    await vips.edit_text("**⚡ѕтαя**")
    await vips.edit_text("**⚡ѕтαят**")
    await vips.edit_text("**⚡ѕтαятι**")
    await vips.edit_text("**⚡ѕтαятιи**")
    await vips.edit_text("**⚡ѕтαятιиg**")
    await vips.edit_text("**⚡ѕтαятιиg.**")
    await asyncio.sleep(0.1)
    await vips.edit_text("**⚡ѕтαятιиg....**")
    await asyncio.sleep(0.1)
    await vips.edit_text("**⚡ѕтαятιиg.**")
    await asyncio.sleep(0.1)
    await vips.edit_text("**⚡ѕтαятιиg....**")

    # -------- Welcome Video & Message --------
    video_source = "https://envs.sh/F59.mp4"  # Replace with your valid video URL

    caption = (
        "╔═══════════════════════════════╗\n"
        "🌌✨ ＷＥＬＣＯＭＥ ＴＯ 𝕿𝕱𝕲𝕻𝕷 ２０２５ ✨🌌\n"
        "⚡ 𝑻𝒂𝒎𝒊𝒍 𝐹𝓇𝒾𝑒𝓃𝒹𝓈𝒽𝒾𝓅 𝑮𝒓𝒐𝒖𝒑 𝑷𝒓𝒆𝒎𝒊𝒆𝒓 𝑳𝒆𝒂𝒈𝒖𝒆 ⚡\n"
        "╚═══════════════════════════════╝\n\n"
        "📆 𝗢𝗽𝗲𝗻𝘀: 22 Aug 2025 🌟\n"
        "📆 𝗖𝗹𝗼𝘀𝗲𝘀: 30 Aug 2025 🌟\n"
        "📍 𝗩𝗲𝗻𝘂𝗲: @group_friendship_tamil\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📝 𝗥𝗲𝗴𝗶𝘀𝘁𝗿𝗮𝘁𝗶𝗼𝗻 𝗦𝘁𝗲𝗽𝘀\n"
        "✅ Fill 𝗚𝗼𝗼𝗴𝗹𝗲 𝗙𝗼𝗿𝗺\n"
        "✅ Captain + Vice Captain ✨\n"
        "✅ Team Name 🌲\n"
        "✅ 9–16 Players 💥\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "👥 𝗦𝗾𝘂𝗮𝗱 𝗥𝘂𝗹𝗲𝘀\n"
        "✅ 9 Min – 16 Max ⚡\n"
        "✅ No Substitutes ❌\n"
        "✅ All 16 are Main Players 🏅\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "💬 “Play with ✨Spirit✨, Win with 🏆Pride🏆, Celebrate with 💖Friendship💖”\n\n"
        f"👨‍💻 *Bot Developed by* [{BOT_DEVELOPER}]({BOT_LINK})"
    )

    keyboard = [
        [InlineKeyboardButton("📝 Click Here to Register", url=REGISTER_LINK)],
        [
            InlineKeyboardButton("🦅 Whistle Squads", url="https://t.me/BeastPaiyan"),
            InlineKeyboardButton("📢 Broadcasting", url="https://t.me/Rubesh_official_18")
        ]
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
