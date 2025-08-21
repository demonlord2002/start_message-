import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# ---------------- Bot Info ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN", "8365258721:AAG47_D-GLCKMoiakwf0ONUFMVlRck-jwmw")
BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID", "7049074888"))  # Your Telegram ID
BOT_DEVELOPER = os.getenv("BOT_DEVELOPER", "𝙈𝙖𝙧𝙬𝙞𝙣")
BOT_LINK = os.getenv("BOT_LINK", "https://t.me/SunsetOfMe")
REGISTER_LINK = os.getenv("REGISTER_LINK", "https://docs.google.com/forms/d/e/1FAIpQLSfGyaA74UQdjftO-Qje70odt0HCkW4Bs9FLftpjBO1EQZ92OA/viewform?usp=dialog")

# ---------------- MongoDB ----------------
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://rubesh08virat:rubesh08virat@cluster0.d33p1rm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
