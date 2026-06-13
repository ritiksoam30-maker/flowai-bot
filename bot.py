from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os
import google.generativeai as genai

# TOKENS
TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# GEMINI SETUP
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

user_state = {}

if not TOKEN:
    print("BOT_TOKEN missing!")
    exit()

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📝 Script Generator", callback_data="script")]
    ]

    await update.message.reply_text(
        "🚀 FlowAI Creator Bot\n\nSelect option 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# BUTTON CLICK
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "script":
        user_state[query.from_user.id] = "type"
        await query.message.reply_text(
            "🎭 Story type likho:\n(horror / tech / motivation / love / comedy)"
        )

# MESSAGE HANDLER
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    state = user_state.get(user_id)

    # STEP 1: TYPE
    if state == "type":
        user_state[user_id] = {"type": text.lower()}
        await update.message.reply_text("🌍 Language likho (Hindi ya English):")
        return

    # STEP 2: LANGUAGE
    if isinstance(state, dict) and "type" in state and "lang" not in state:
        state["lang"] = text
        user_state[user_id] = state
        await update.message.reply_text("✍️ Ab apna topic / idea likho:")
        return

    # STEP 3: GENERATE STORY (GEMINI AI)
    if isinstance(state, dict) and "lang" in state:
        story_type = state["type"]
        lang = state["lang"]
        topic = text

        prompt = f"""
Create a complete {story_type} story in {lang} language.

Topic: {topic}

Make it:
- Very engaging
- Cinematic
- Full detailed story
- No placeholders
- YouTube ready script
"""

        try:
            response = model.generate_content(prompt)
            script = response.text
        except Exception as e:
            script = "⚠️ AI error, try again later.\n\nError: " + str(e)

        await update.message.reply_text(script)
        user_state[user_id] = None


# APP SETUP
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("FlowAI Bot Running...")
app.run_polling()
