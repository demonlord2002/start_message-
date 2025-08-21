import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# ---------------- Bot Info ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token_here")
BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID", "123456789"))  # Your Telegram ID
BOT_DEVELOPER = os.getenv("BOT_DEVELOPER", "YourName")
BOT_LINK = os.getenv("BOT_LINK", "https://t.me/yourusername")
REGISTER_LINK = os.getenv("REGISTER_LINK", "https://t.me/your_registration_link")

# ---------------- MongoDB ----------------
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
