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
    "💥✨ 𝗧𝗙𝗚𝗣𝗟 ２𝟶２５ – 𝗧𝗛𝗘 𝗣𝗥𝗘𝗠𝗜𝗘𝗥 𝗟𝗘𝗔𝗚𝗨𝗘 𝗢𝗙 𝗙𝗥𝗜𝗘𝗡𝗗𝗦𝗛𝗜𝗣 ✨💥\n\n"
    "⭐️ Tamil Friendship Group Premier League ⭐️\n\n"
    "╔═════════════════════════╗\n"
    "   🔥 𝔾𝕝𝕠𝕣𝕪 • 𝐔𝐧𝐢𝐭𝐲 • ℂ𝕣𝕚𝕔𝕜𝕖𝕥 𝐏𝐚𝐬𝐬𝐢𝐨𝐧 🔥\n"
    "╚═════════════════════════╝\n\n"
    "📅 Registration Opens: *22 Aug 2025*\n"
    "📅 Closes On: *30 Aug 2025*\n"
    "📍 Venue: [𝗧𝗮𝗺𝗶𝗹 𝗙𝗿𝗶𝗲𝗻𝗱𝘀𝗵𝗶𝗽 𝗚𝗿𝗼𝘂𝗽🛍🆒](https://t.me/group_friendship_tamil)\n\n"
    "━━━━━━━━━━━━━━━━━━━\n"
    "📝 *How to Register*\n"
    "✅ Fill Google Form\n"
    "✅ Enter Captain & Vice Captain usernames\n"
    "✅ Submit Team Name\n"
    "✅ Add Squad List (9–16 Players)\n"
    "✅ Tick confirmation before submit\n"
    "⚠️ Late entries will *NOT* be accepted!\n\n"
    "━━━━━━━━━━━━━━━━━━━\n"
    "👥 *Team Guidelines*\n"
    "😵 Minimum: 9 | Maximum: 16 Players\n"
    "😵 No Substitutes (All 16 = Official Squad)\n"
    "😵 Rotation allowed only within squad\n"
    "😵 Squad Names will be recorded in *Stumps*\n\n"
    "━━━━━━━━━━━━━━━━━━━\n"
    "💬 Official Committee:\n"
    "_“Cricket is the game, Friendship is the crown,\nＴＦＧＰＬ ２𝟶２５ is where legends are born!”_\n\n"
    "╔═════════════════════╗\n"
    "   Registration ➡️ 🔥 [Click here](https://docs.google.com/forms/d/e/1FAIpQLSfGyaA74UQdjftO-Qje70odt0HCkW4Bs9FLftpjBO1EQZ92OA/viewform?usp=dialog) 🔥\n"
    "╚═════════════════════╝\n\n"
    "🔗 #TFGPL2025 #PremierFriendshipLeague #CricketUnites\n\n"
    f"👨‍💻 Developed by [{BOT_DEVELOPER}]({BOT_LINK})"
)

    
    keyboard = [
        [InlineKeyboardButton("📝 Click Here to Register", url=REGISTER_LINK)],
        [
            InlineKeyboardButton("WS × BST", url="https://t.me/BeastPaiyan"),
            InlineKeyboardButton("WS × Doraemon", url="https://t.me/Rubesh_official_18")
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
