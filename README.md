# 🎮 UnlockMe Telegram Bot

This is a simple Telegram bot that sends users to a hosted WebGL game page via a hidden, secure link.

---

## 🚀 Features

- Built with Python using `python-telegram-bot`, `Flask`, and `dotenv`
- Uses **webhooks** for real-time interaction (no polling)
- Game link is **securely stored in a `.env` file**
- Deployable for **free** using platforms like [Render](https://render.com)
- Users interact via the `/start` command and are shown a **custom inline button** to launch the game

---
## 📦 How It Works

1. Bot is created using [@BotFather](https://t.me/BotFather)
2. When a user sends `/start`, the bot responds with a hidden button:
3. 3. The button opens the game hosted at [UnlockMe WebGL](https://chiew12301.github.io/UnlockMeWeb/)

> 🔒 The game URL and bot token are stored in the `.env` file for security.

---

## 🛠️ Setup

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/unlockme-telegram-bot.git
cd unlockme-telegram-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create a .env File
```bash
TOKEN=your-telegram-bot-token
WEBHOOK_URL=https://your-app-name.onrender.com
GAME_URL=https://chiew12301.github.io/UnlockMeWeb/
```

### 3. Create a .env File
```bash
TOKEN=your-telegram-bot-token
WEBHOOK_URL=https://your-app-name.onrender.com
GAME_URL=https://xxx.xxx.com
```
Never commit your .env file to GitHub

### 4. Run the Bot Locally (for testing)
```bash
python bot.py
```

### Notes
✅ This bot is free to use, but only maintained on the main branch
