import os
import time
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackGame
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
    chat_id = update.effective_chat.id

    context.bot.send_game(
        chat_id=chat_id,
        game_short_name="unlockme"
    )

    time.sleep(2)

    keyboard = [
        [InlineKeyboardButton("▶️ Click here to play", url=GAME_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=chat_id,
        text="⚠️ If the Play button above doesn’t work, click the button below to start the game:",
        reply_markup=reply_markup
    )

def game_callback(update, context):
    query = update.callback_query
    print(f"Callback data: {query.data}, GAME_URL: {GAME_URL}")
    query.answer()

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
