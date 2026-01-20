import urllib.parse

async def search_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()

    if not query:
        await update.message.reply_text("❌ Please type a song name.")
        return

    await update.message.reply_text("🔍 Searching on YouTube...")

    # YouTube search URL (SAFE, no block)
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://www.youtube.com/results?search_query={encoded_query}"

    await update.message.reply_text(
        f"🎵 Search results for:\n<b>{query}</b>\n\n"
        f"▶️ Open YouTube:\n{search_url}",
        parse_mode="HTML"
    )
