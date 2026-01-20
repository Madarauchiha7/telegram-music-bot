import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import yt_dlp

# =====================
# BOT TOKEN (from Render Environment Variable)
# =====================
TOKEN = os.environ.get("8415764096:AAEs8tNIZFqCJyuePfsRIm2067V8xJbDOqc")

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
# Telegram Bot Functions
# =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 Search your favorite music and enjoy 🎶\n\n"
        "Just type the song name."
    )

async def search_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text("🔍 Searching...")

    ydl_opts = {
        "quiet": True,
        "default_search": "ytsearch1",
        "skip_download": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            video = info["entries"][0]

        title = video.get("title")
        url = video.get("webpage_url")

        await update.message.reply_text(
            f"🎶 {title}\n▶️ Watch / Listen:\n{url}"
        )

    except Exception:
        await update.message.reply_text(
            "❌ Song not found.\nPlease try another song name."
        )

# =====================
# Start Bot
# =====================
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_music))

application.run_polling()
