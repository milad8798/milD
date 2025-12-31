import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام DORX! لینک پست اینستاگرام رو بفرست تا ویدیو رو برات دانلود کنم 🎥🔥")

async def handle_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "instagram.com" not in url:
        await update.message.reply_text("لطفاً یک لینک معتبر اینستاگرام بفرست.")
        return

    await update.message.reply_text("⏳ در حال دانلود ویدیو... لطفاً صبر کن.")

    try:
        api_url = f"https://api.ryzendesu.vip/instadl?url={url}"
        response = requests.get(api_url).json()

        video_url = response["result"]["url"]

        await update.message.reply_video(video_url)
    except Exception as e:
        await update.message.reply_text("❌ خطا در دانلود ویدیو. دوباره تلاش کن.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_instagram))

app.run_polling()





