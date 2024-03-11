#!/usr/bin/env python

import logging
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


# Enable logging
logging.basicConfig(
    format='timestamp=%(asctime)s logger=%(name)s level=%(levelname)s msg="%(message)s"',
    datefmt='%Y-%m-%dT%H:%M:%S',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("./logs/bot.log"),
        logging.StreamHandler()
    ]
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Set your OpenAI API key
# Replace None with your OpenAI API key


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


# 2024-02-28T11:48:14.892862627Z ChatCompletion(id='chatcmpl-8xChybGg2uRWPk0hagGRIdHvjoaAX', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='Hello! How can I assist you today?', role='assistant', function_call=None, tool_calls=None))], created=1709120894, model='gpt-3.5-turbo-0125', object='chat.completion', system_fingerprint='fp_86156a94a0', usage=CompletionUsage(completion_tokens=9, prompt_tokens=18, total_tokens=27))
async def gpt_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    
    logger.info("Пользователь написал сообщение {0}".format(user_message))
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are comrade ho chi minh"},
                {"role": "user", "content": user_message}
            ]
        )
        # Access text content from "message" within the first "Choice"
        ai_response = response.choices[0].message.content
        await update.message.reply_text(ai_response.strip())
    except Exception as e:
        logger.error(f"Error generating AI response: {e}")
        await update.message.reply_text("Sorry, I couldn't process your message at the moment.")
        
        
        

        
        
        
    


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    application = Application.builder().token(telegram_bot_token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    application.add_handler(CommandHandler("image", generate_image))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gpt_prompt))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
