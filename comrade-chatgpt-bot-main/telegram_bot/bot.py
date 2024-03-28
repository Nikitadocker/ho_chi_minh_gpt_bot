#!/usr/bin/env python
import asyncio
import asyncpg
import logging
import os
import requests
from openai import OpenAI
from logfmter import Logfmter

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
IMAGE_PRICE = float(os.getenv("IMAGE_PRICE", 0.10))  # Default price per image
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

formatter = Logfmter(
    keys=["timestamp", "logger", "at", "process", "msq"],
    mapping={
        "timestamp": "asctime",
        "logger": "name",
        "at": "levelname",
        "process": "processName",
        "msg": "message",
    },
    datefmt="%Y-%m-%dT%H:%M:%S",
)

handler_stdout = logging.StreamHandler()
handler_file = logging.FileHandler("./logs/logfmter_bot.log")
handler_stdout.setFormatter(formatter)
handler_file.setFormatter(formatter)
logging.basicConfig(handlers=[handler_stdout, handler_file], level=logging.INFO)


# set higher logging level for httpx to avoid all GET and POST requests being logged
# logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Set your OpenAI API key
# Replace None with your OpenAI API key


async def db_connect():
    return await asyncpg.connect(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        database=os.getenv("POSTGRES_DB"),
        host=os.getenv("DB_HOST"),
    )


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    logging.info(f"User {user.id} ({user.username}) started the bot.")
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def is_user_allowed(user_id: int) -> bool:
    conn = await db_connect()
    try:
        existing_user = await conn.fetchval(
            "SELECT user_id FROM allowed_users WHERE user_id = $1", user_id
        )
        return existing_user is not None
    finally:
        await conn.close()


async def check_user_balance(user_id: int) -> (bool, float):
    """
    Checks if the user has enough balance to generate an image.
    Returns a tuple (bool, float) where bool indicates if the user has enough balance,
    and float represents the current balance of the user.
    """
    conn = await db_connect()
    try:
        balance = await conn.fetchval(
            "SELECT balance FROM user_balances WHERE user_id = $1", user_id
        )
        if (
            balance is None
        ):  # This means the user does not exist in the user_balances table
            return False, 0.0
        return balance >= IMAGE_PRICE, balance
    finally:
        await conn.close()


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


# This function will be used for generate image
async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    user = update.effective_user

    if not await is_user_allowed(user.id):
        logger.info(
            f"User {user.id} ({user.username}) tried to generate an image but is not allowed."
        )
        await update.message.reply_text(
            "Sorry, you are not allowed to generate images."
        )
        return

        # Check user's balance
    has_enough_balance, current_balance = await check_user_balance(user.id)
    if not has_enough_balance:
        await update.message.reply_text(
            f"Sorry, your current balance ({current_balance}₪) is not enough to generate an image. Price per image is {IMAGE_PRICE}₪."
        )
        return

    if not context.args:
        logger.error(
            f"User {user.id} ({user.username}) did not provide a prompt for the /image command."
        )
        await update.message.reply_text(
            "Please provide a description for the image after the /image command."
        )
        return

    prompt = " ".join(
        context.args
    )  # принимать в качестве promзt аргументы отпользователя
    logging.info(f"User {user.id} ({user.username}) requested to generate image")

    try:
        """Generate image when the command /image is issued"""
        response_image = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response_image.data[0].url
        responce_url = requests.get(image_url)
        with open("./images/image.png", "wb") as f:
            f.write(responce_url.content)
        await update.message.reply_photo(open("./images/image.png", "rb"))

        conn = await db_connect()
        try:
            await conn.execute(
                "UPDATE user_balances SET balance = balance - $1, images_generated = images_generated + 1 WHERE user_id = $2",
                IMAGE_PRICE,
                user.id,
            )
            logger.info(
                f"Image generated for user {user.id}. Balance deducted by {IMAGE_PRICE}."
            )
        finally:
            await conn.close()

    except Exception as e:
        logging.error(f"Error generating image for prompt: '{prompt}': {e}")
        await update.message.reply_text(
            "Sorry, there was an error generating your image."
        )

    # 2024-02-28T11:48:14.892862627Z ChatCompletion(id='chatcmpl-8xChybGg2uRWPk0hagGRIdHvjoaAX', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='Hello! How can I assist you today?', role='assistant', function_call=None, tool_calls=None))], created=1709120894, model='gpt-3.5-turbo-0125', object='chat.completion', system_fingerprint='fp_86156a94a0', usage=CompletionUsage(completion_tokens=9, prompt_tokens=18, total_tokens=27))


async def gpt_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    user = update.effective_user

    if not await is_user_allowed(user.id):
        logger.info(
            f"User {user.id} ({user.username}) tried to use GPT prompt but is not allowed."
        )
        await update.message.reply_text("Sorry, you are not allowed to text with me.")
        return

    # logger.info("Пользователь написал сообщение {0}".format(user_message))

    logging.info(
        f"User {user.id} ({user.username}) requested sent text: '{user_message}'"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are comrade ho chi minh"},
                {"role": "user", "content": user_message},
            ],
        )
        # Access text content from "message" within the first "Choice"
        ai_response = response.choices[0].message.content
        await update.message.reply_text(ai_response.strip())
    except Exception as e:
        logger.error(f"Error generating AI response: {e}")
        await update.message.reply_text(
            "Sorry, I couldn't process your message at the moment."
        )


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
