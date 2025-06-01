import os
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler

load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
GAME_URL = os.getenv("GAME_URL")
GAME_SHORT_NAME = "unlockme" 

bot = Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0)

def start(update, context):
    keyboard = [
        [InlineKeyboardButton("🎮 Play Unlock Me", callback_data=GAME_SHORT_NAME)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Try Unlock Me by KurumiC below!", reply_markup=reply_markup)

def game_callback(update, context):
    query = update.callback_query
    if query.game_short_name == GAME_SHORT_NAME:
        query.answer(url=f"https://t.me/{bot.username}?game={GAME_SHORT_NAME}")
    else:
        query.answer("Unknown game.")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(game_callback))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
