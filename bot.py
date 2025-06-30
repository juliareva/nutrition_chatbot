import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from telegram import File
from gpt import get_macros_from_gpt, get_macros_from_image


load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    reply_text = get_macros_from_gpt(user_input)
    await update.message.reply_text(reply_text)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    file_bytes = await file.download_as_bytearray()
    reply_text = get_macros_from_image(file_bytes)
    await update.message.reply_text(reply_text)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

print("MacroMate is running!")

app.run_polling()

