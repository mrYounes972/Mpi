import mimetypes

class InputFile

    def __init__(self, file_path):
        self.file_path = file_path
        self.mime_type = mimetypes.guess_type(file_path)[0]

    def read(self):
        with open(self.file_path, "rb") as f:
            return f.read()

    def get_mime_type(self):
        return self.mime_type or "application/octet-stream"
import telegram, logging
from scanner import run_scan
from report import generate_report

# ⚙️ Bot Token و Setup
BOT_TOKEN = "8368339297:AAG9ENmzSHLk4AIkSKlr8w0EUgQTlpZwvYs"
bot = telegram.Bot(token=BOT_TOKEN)
updater = telegram.ext.Updater(BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# 🧠 دستور /scan برای شروع اسکن
def scan_handler(update, context):
    try:
        args = context.args
        if not args:
            update.message.reply_text("❌ لطفاً آیدی هدف را بده: /scan @username")
            return
        target = args[0].replace("@", "")
        update.message.reply_text(f"🛰️ در حال اسکن @{target}...")

        results = run_scan(target, BOT_TOKEN)
        report_text = generate_report(results, output_type="text")

        update.message.reply_text(f"📄 نتیجه اسکن:\n{report_text[:4000]}")
    except Exception as e:
        update.message.reply_text(f"⚠️ خطا در اسکن: {e}")

# 🧩 ثبت دستور
dispatcher.add_handler(telegram.ext.CommandHandler("scan", scan_handler))

# 🎬 شروع بات
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    updater.start_polling()
