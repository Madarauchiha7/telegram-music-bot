import os
import threading
import urllib.parse
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =====================
# BOT TOKEN (Render Environment Variable)
# =====================
TOKEN = os.environ.get("TOKEN")

# =====================
# Web Server (Render needs PORT)
# =====================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_web():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()

# =====================
# Telegram Bot
# =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 Search your favorite music and enjoy 🎶\n\n"
        "Just type the song name.\n"
        "Example:\nkesariya arijit singh"
    )

async def search_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()

    if not query:
        await update.message.reply_text("❌ Please type a song name.")
        return

    # Create YouTube search URL (100% safe)
    encoded = urllib.parse.quote(query)
    search_url = f"https://www.youtube.com/results?search_query={encoded}"

    await update.message.reply_text(
        f"🎶 Search results for:\n<b>{query}</b>\n\n"
        f"▶️ Open YouTube:\n{search_url}",
        parse_mode="HTML"
    )

# =====================
# Start Bot
# =====================
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_music))

application.run_polling()
