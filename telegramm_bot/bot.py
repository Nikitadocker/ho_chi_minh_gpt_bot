from telegram import Update
from openai import OpenAI
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

OPEN_AI_API = os.getenv("OPEN_AI_API")

# Define a command handler. These usually take the two arguments update and context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Xin chào!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

client = OpenAI(api_key=OPEN_AI_API)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are comrade Ho Chi Minh."},
        {"role": "user", "content": "Что ты думаешь о товарище Xошимине?"}
    ]
)
# Access text content from "message" within the first "Choice"
ai_response = response.choices[0].message.content
print(ai_response.strip())


# Create the Application and pass it your bot's token.
application = Application.builder().token(TOKEN).build()

# on different commands - answer in Telegram
application.add_handler(CommandHandler("start", start))

# on non command i.e. message - echo the message on Telegram
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Run the bot until the user presses Ctrl-C
application.run_polling(allowed_updates=Update.ALL_TYPES)















