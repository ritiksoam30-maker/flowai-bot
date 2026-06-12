from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Welcome to FlowAI Creator Bot!\n\n"
        "📝 Script Generator\n"
        "🎨 Thumbnail Generator\n"
        "📚 Documentary Mode\n"
        "🎤 Voice Generator\n"
        "🎥 Video Creator"
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
