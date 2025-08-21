# TFGPL Broadcast Bot

A **Telegram Broadcast Bot** built with `python-telegram-bot` and `MongoDB`. This bot has two main files: 

- **`bot.py`** – Contains the main logic for `/start` and `/broadcast` commands, saving users/chats, and broadcasting messages with flags like `-pin`, `-pinloud`, `-user`, and `-nobot`.  
- **`config.py`** – Stores your configuration variables such as `BOT_TOKEN`, `BOT_OWNER_ID`, `BOT_DEVELOPER`, `BOT_LINK`, `REGISTER_LINK`, and `MONGO_URL`.  

Together, these files allow you to broadcast messages to users and group chats, manage persistent data in MongoDB, and control bot settings easily.

---

## Features

- Broadcast messages to group chats and users
- Optional pinning: `-pin`, `-pinloud`
- User-only broadcast: `-user`
- Skip group chat broadcast: `-nobot`
- Persistent MongoDB storage for chats and users
- Easy configuration via `config.py` and `.env`

---

## Deploy to Heroku

Click the button below to deploy your bot instantly:

[![Deploy](https://www.herokucdn.com/deploy/button-red.svg)](https://heroku.com/deploy?template=https://github.com/demonlord2002/start_message-)

---

## Usage

1. Fill your `.env` file with `BOT_TOKEN`, `BOT_OWNER_ID`, `MONGO_URL`, and other settings.  
2. Start the bot: `/start`  
3. Broadcast messages using `/broadcast [message] [-flags]`. Example:  
   - `/broadcast Hello everyone! -pin`  
   - `/broadcast -user Announcement for users only!`

---

## Requirements

- Python 3.10+
- `python-telegram-bot>=20.3`
- `pymongo`
- `python-dotenv`

---

## License

MIT License. Free to use and modify.
