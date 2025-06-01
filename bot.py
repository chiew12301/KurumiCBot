import os
import os
import asyncio
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler

load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
GAME_URL = os.getenv("GAME_URL")
GAME_SHORT_NAME = "unlockme" 
GAME_UNLOCK_ME_URL = os.getenv("GAME_UNLOCK_ME_URL")
GAME_KULET_WADE_URL = os.getenv("GAME_KULET_WADE_URL")
ITCH_IO_URL = os.getenv("ITCH_IO_URL")
PACKAGES_URL = os.getenv("PACKAGES_URL")
PROFILE_URL = os.getenv("PROFILE_URL")
ABOUT_TEXT = os.getenv("ABOUT_TEXT", "KurumiC is a creative indie developer making casual web and mobile games with heart. 💜")

bot = Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

CALLBACK_GAME_LIST = "game_list"
CALLBACK_PACKAGES = "packages"
CALLBACK_PROFILE = "profile"

async def reply_and_auto_delete(context, chat_id, text, reply_markup=None, delay=10):
    message = await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    await asyncio.sleep(delay)
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    except Exception as e:
        print(f"Failed to delete message: {e}")

def start(update, context):
    args = context.args
    if args:
        return handle_deep_link(update, context, args[0].lower())

    keyboard = [
        [InlineKeyboardButton("🄹 Game List", callback_data="gamelist")],
        [InlineKeyboardButton("📦 KurumiC Packages", callback_data="packages")],
        [InlineKeyboardButton("👤 KurumiC Profile", callback_data="profile")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    asyncio.run(reply_and_auto_delete(context, update.effective_chat.id,
        "👋 *Welcome to KurumiC Bot Helper!*\nChoose an option below to get started:",
        reply_markup))

def button_handler(update, context):
    query = update.callback_query
    query.answer()
    data = query.data

    if data == "gamelist":
        text = (
            "🎮 *Game List:*\n"
            "• [Unlock Me](%s)\n"
            "• [Kulet Wade](%s)\n"
            "• [More on Itch.io](%s)"
        ) % (GAME_UNLOCK_ME_URL, GAME_KULET_WADE_URL, ITCH_IO_URL)
        query.edit_message_text(text=text, parse_mode="Markdown")
    elif data == "packages":
        query.edit_message_text("📦 [View KurumiC Packages](%s)" % PACKAGES_URL, parse_mode="Markdown")
    elif data == "profile":
        query.edit_message_text("👤 [View KurumiC Profile](%s)" % PROFILE_URL, parse_mode="Markdown")


def game_list_command(update, context):
    asyncio.run(reply_and_auto_delete(context, update.effective_chat.id,
        f"🎮 *Games by KurumiC:*\n"
        f"• [Unlock Me]({GAME_UNLOCK_ME_URL})\n"
        f"• [Kulet Wade]({GAME_KULET_WADE_URL})\n"
        f"• [More on Itch.io]({ITCH_IO_URL})"))

def packages_command(update, context):
    asyncio.run(reply_and_auto_delete(context, update.effective_chat.id,
        f"[📦 View KurumiC Packages]({PACKAGES_URL})"))

def profile_command(update, context):
    asyncio.run(reply_and_auto_delete(context, update.effective_chat.id,
        f"[👤 View KurumiC Profile]({PROFILE_URL})"))

def help_command(update, context):
    asyncio.run(reply_and_auto_delete(context, update.effective_chat.id,
        "📌 *Available Commands:*\n"
        "/start – Show welcome menu\n"
        "/gamelist – Show available games\n"
        "/packages – View KurumiC packages\n"
        "/profile – View KurumiC profile\n"
        "/help – Show this help message\n"
        "/about – About KurumiC"))

def about_command(update, context):
    asyncio.run(reply_and_auto_delete(context, update.effective_chat.id,
        f"ℹ️ *About KurumiC:*\n{ABOUT_TEXT}"))

def handle_deep_link(update, context, param):
    messages = {
        "unlockme": "🔓 Play *Unlock Me*:\n[Click here](%s)" % GAME_UNLOCK_ME_URL,
        "kuletwade": "🌊 Play *Kulet Wade*:\n[Click here](%s)" % GAME_KULET_WADE_URL,
        "itch": "🎮 Discover more games on Itch.io:\n[Click here](%s)" % ITCH_IO_URL,
        "packages": "📦 View KurumiC Packages:\n[Click here](%s)" % PACKAGES_URL,
        "profile": "👤 View KurumiC Profile:\n[Click here](%s)" % PROFILE_URL,
    }
    msg = messages.get(param)
    if msg:
        asyncio.run(reply_and_auto_delete(context, update.effective_chat.id, msg))
    else:
        asyncio.run(reply_and_auto_delete(context, update.effective_chat.id, "❓ Sorry, I don't recognize that link parameter."))

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(CommandHandler("about", about_command))
dispatcher.add_handler(CommandHandler("gamelist", game_list_command))
dispatcher.add_handler(CommandHandler("packages", packages_command))
dispatcher.add_handler(CommandHandler("profile", profile_command))
dispatcher.add_handler(CallbackQueryHandler(button_handler))

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