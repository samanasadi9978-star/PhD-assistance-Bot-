import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Pull credentials from Render's secure Environment Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.message.chat_id
    
    await context.bot.send_message(chat_id=chat_id, text="🔍 Position received. Analyzing with strict academic rules...")

    prompt = (
        f"You are Saman Asadi's autonomous academic assistant. A user just sent this PhD position details/text: \n\n"
        f"\"{user_text}\"\n\n"
        f"Please parse this position: extract the Institution, PI Name (if available), Research Focus, and whether it matches a DVM/Translational Oncology background. Keep it concise."
    )
    
    try:
        response = model.generate_content(prompt)
        await context.bot.send_message(chat_id=chat_id, text=response.text)
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"Error processing with AI: {str(e)}")

def main():
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        print("Error: TELEGRAM_TOKEN or GEMINI_API_KEY environment variables are missing!")
        return

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
