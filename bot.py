import logging
import os
from dotenv import load_dotenv
from telegram import (
    Update, InlineKeyboardMarkup, InlineKeyboardButton,
    MessageEntity
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
)

from config import BOT_DEVELOPER, BOT_LINK, REGISTER_LINK

# Load .env for BOT_TOKEN and Developer ID
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID", "0"))  # Add your Telegram ID in .env

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage of chats/users
served_chats = set()
served_users = set()


# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    # Save chats and users for broadcasting later
    served_chats.add(chat.id)
    served_users.add(user.id)

    # Use your Telegram video file_id here
    video_file_id = "BAACAgUAAxkBAAE56u1opzyL_P6k0YSwiMPPw8nYyeGvWwAClxwAAgQ9QVWe9qeVrkf5WjYE"

    # Start message as caption
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

    # Inline buttons
    keyboard = [
        [InlineKeyboardButton("📝 Click Here to Register", url=REGISTER_LINK)],
        [InlineKeyboardButton("🦅 Whistle Squads", url="https://t.me/BeastPaiyan")],
        [InlineKeyboardButton("📢 Broadcasting", url="https://t.me/Rubesh_official_18")]
    ]

    # Send video + caption + buttons in one message
    await update.message.reply_video(
        video=video_file_id,
        caption=caption,
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# /broadcast command (only for bot owner)
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != BOT_OWNER_ID:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return

    if not context.args and not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Usage: /broadcast [message or reply] with optional flags (-pin, -pinloud, -user, -nobot)")
        return

    # Extract flags
    text = " ".join(context.args)
    flags = [w for w in text.split() if w.startswith("-")]
    message_text = " ".join([w for w in text.split() if not w.startswith("-")])

    # If reply used instead of message
    if update.message.reply_to_message and not message_text:
        message_text = update.message.reply_to_message.text

    results = []
    if "-nobot" not in flags:
        # Broadcast to chats
        for chat_id in served_chats:
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
        # Broadcast to direct users
        for user in served_users:
            try:
                await context.bot.send_message(chat_id=user, text=message_text)
                results.append(f"👤 Sent to user {user}")
            except Exception as e:
                logger.warning(f"Failed to send to user {user}: {e}")
                results.append(f"❌ User {user}")

    await update.message.reply_text("\n".join(results) or "⚠️ Nothing sent.")


# Start the bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))

    app.run_polling()


if __name__ == "__main__":
    main()
