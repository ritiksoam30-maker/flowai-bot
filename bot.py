from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

user_state = {}

if not TOKEN:
    print("BOT_TOKEN missing!")
    exit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📝 Script Generator", callback_data="script")]
    ]

    await update.message.reply_text(
        "🚀 FlowAI Creator Bot Ready!\n\nChoose option 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "script":
        user_state[query.from_user.id] = "script"
        await query.message.reply_text("✍️ Script ka topic likho (example: motivation, love story, tech)")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_state.get(user_id) == "script":
        topic = update.message.text

        script = f"""
🔥 VIRAL YOUTUBE SCRIPT 🔥

Topic: {topic}

Intro:
Aaj hum baat karenge ek aise topic par jo aapki soch badal dega...

Main Content:
{topic} par detail explanation aur engaging story flow...

Ending:
Agar aapko ye video pasand aaya to like aur subscribe zarur karein 🚀
"""

        await update.message.reply_text(script)
        user_state[user_id] = None

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("FlowAI Bot Running...")
app.run_polling()
