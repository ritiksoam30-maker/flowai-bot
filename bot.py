from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("BOT_TOKEN missing!")
    exit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📝 Script Generator", callback_data="script")],
        [InlineKeyboardButton("🎬 Documentary Idea", callback_data="doc")],
        [InlineKeyboardButton("🎨 Thumbnail Idea", callback_data="thumb")],
        [InlineKeyboardButton("🎤 Voice Script", callback_data="voice")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🚀 Welcome to FlowAI Creator Bot!\n\nChoose what you want to create 👇",
        reply_markup=reply_markup
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("FlowAI Bot is running...")
app.run_polling()
