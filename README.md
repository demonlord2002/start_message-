# TFGPL Broadcast Bot

A **Telegram Broadcast Bot** built with `python-telegram-bot` and `MongoDB`. This bot consists of two main files: `bot.py`, which contains the main logic for `/start` and `/broadcast` commands, user/chat saving, and message sending with flags like `-pin`, `-pinloud`, `-user`, and `-nobot`; and `config.py`, which stores all your configuration such as `BOT_TOKEN`, `BOT_OWNER_ID`, `BOT_DEVELOPER`, `BOT_LINK`, `REGISTER_LINK`, and `MONGO_URL`. Together, these files allow you to broadcast messages to group chats and users, store persistent data in MongoDB, and manage bot settings easily.

---

## Deploy to Heroku

Click the red button below to deploy your bot instantly on Heroku:

[![Deploy](https://www.herokucdn.com/deploy/button-red.svg)](https://heroku.com/deploy?template=https://github.com/demonlord2002/start_message-)
