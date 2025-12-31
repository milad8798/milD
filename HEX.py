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

    await update.message.reply_text("⏳ در حال پردازش لینک... لطفاً صبر کن.")

    try:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest"
        }
        data = {
            "q": url,
            "t": "media",
        }

        response = requests.post("https://save-insta.app/api/ajaxSearch", headers=headers, data=data)
        result = response.json()

        media_list = result.get("media", [])
        if not media_list:
            await update.message.reply_text("❌ ویدیویی پیدا نشد. شاید لینک خصوصی باشه.")
            return

        for media in media_list:
            if media.endswith(".mp4"):
                await update.message.reply_video(media)
            elif media.endswith(".jpg") or media.endswith(".jpeg") or media.endswith(".png"):
                await update.message.reply_photo(media)
            else:
                await update.message.reply_text(f"🔗 لینک فایل: {media}")

    except Exception as e:
        await update.message.reply_text("❌ خطا در پردازش لینک. دوباره تلاش کن.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_instagram))

app.run_polling()






