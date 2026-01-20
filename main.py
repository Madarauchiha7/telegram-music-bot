import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp
from flask import Flask
import threading

TOKEN = os.environ.get("8415764096:AAEs8tNIZFqCJyuePfsRIm2067V8xJbDOqc")

# Web server (Render requirement)
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

threading.Thread(target=run_web).start()

# Telegram bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 Search your favorite music and enjoy 🎶\n\nType song name only."
    )

async def search_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text("🔍 Searching...")

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "default_search": "ytsearch1",
        "format": "bestaudio",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        video = info["entries"][0]
        url = video["url"]
        title = video["title"]

    await update.message.reply_text(
        f"🎶 {title}\n▶️ Play here:\n{url}"
    )

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_music))

application.run_polling()
