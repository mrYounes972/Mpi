from telegram import Bot
from custom_inputfile import CustomInputFile

bot = Bot(token="8368339297:AAG9ENmzSHLk4AIkSKlr8w0EUgQTlpZwvYs")
chat_id = "8142467049"

file = CustomInputFile("image.jpg")
bot.send_photo(
    chat_id,
    photo=file.read(),
    filename=file.filename,
    mime_type=file.get_mime_type()
)
from custom_inputfile import CustomInputFile

file = CustomInputFile("image.jpg")
bot.send_photo(chat_id, file.read(), filename=file.filename, mime_type=file.get_mime_type())
from custom_inputfile import InputFile
import logging
import mimetypes
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 💡 فعال‌سازی لاگ‌ها برای دیباگ دقیق‌تر
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 📢 هندلر دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام یونس! باتت با موفقیت اجرا شد 🤖🔥")

# 📸 تابع تشخیص نوع عکس (جایگزین imghdr)
def get_image_type(path):
    return mimetypes.guess_type(path)[0]

# 🚀 اجرای اصلی بات
def main():
    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
