"""
This application contains a Telegram bot that uses OpenAI's GPT model to generate responses and images.
"""

import os
import logging
from threading import Thread
import asyncpg
import requests
from openai import OpenAI
from logfmter import Logfmter
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from flask import Flask, jsonify

app = Flask(__name__)
app.config["SERVER_NAME"] = f"{os.getenv('MY_POD_IP', '0.0.0.0')}:5000"

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
IMAGE_PRICE = float(os.getenv("IMAGE_PRICE", "0.10"))  # Default price per image

log_to_file = os.getenv("LOG_TO_FILE", "False") == "True"

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
handler_stdout.setFormatter(formatter)

enabled_handlers = [handler_stdout]


if log_to_file:
    handler_file = logging.FileHandler("./logs/logfmter_bot.log")
    handler_file.setFormatter(formatter)
    enabled_handlers.append(handler_file)

logging.basicConfig(handlers=enabled_handlers, level=logging.INFO)


# set higher logging level for httpx to avoid all GET and POST requests being logged
# logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Set your OpenAI API key
# Replace None with your OpenAI API key


def check_openai_connection(api_key=os.getenv("OPENAI_API_KEY")):
    """Check if the OpenAI API is reachable."""
    try:
        test_client = OpenAI(api_key=api_key)

        completion = test_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello!"},
            ],
        )

        logger.info(completion.choices[0].message)
        return True

    except Exception as e:
        logger.error("OpenAI connection check failed: %s", e)
        return False


@app.route("/healthcheck")
def healthcheck():
    """Check the health of the bot's dependencies."""
    # openai_ok = check_openai_connection()
    openai_ok = True

    status = "OK" if openai_ok else "ERROR"
    return jsonify({"status": status}), 200 if status == "OK" else 500


async def db_connect():
    """
    Connects to the database using the credentials from environment variables.
    Returns the connection object.
    """
    return await asyncpg.connect(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        database=os.getenv("POSTGRES_DB"),
        host=os.getenv("DB_HOST"),
    )


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    logger.info("User %s (%s) started the bot.", user.id, user.username)
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def is_user_allowed(user_id: int) -> bool:
    """Check user allow"""
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


async def help_command(
    update: Update, _: ContextTypes.DEFAULT_TYPE
) -> (
    None
):  # линтер ругается на неиспользуемый аргуементcontext но без него ломается handler
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


# This function will be used for generate image
async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate image when the command /image is issued"""
    # user_message = update.message.text
    logger.info(update)
    
    user = update.effective_user

    if not await is_user_allowed(user.id):
        logger.info(
            "User %s (%s) tried to generate an image but is not allowed.",
            user.id,
            user.username,
        )

        await update.message.reply_text(
            "Sorry, you are not allowed to generate images.",
            reply_to_message_id=update.message.message_id,
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
            "User %s (%s) did not provide a prompt for the /image command.",
            user.id,
            user.username,
        )
        await update.message.reply_text(
            "Please provide a description after the /image command.",
            reply_to_message_id=update.message.message_id,
        )
        return

    prompt = " ".join(
        context.args
    )  # принимать в качестве promзt аргументы отпользователя
    logger.info("User %s (%s) requested to generate image", user.id, user.username)
    try:
        response_image = client.images.generate(
            # model="dall-e-3",
            model="228",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response_image.data[0].url
        responce_url = requests.get(image_url, timeout=100)
        with open("/images/image.png", "wb") as f:
            f.write(responce_url.content)
        with open("/images/image.png", "rb") as f:
            await update.message.reply_photo(f)

        conn = await db_connect()
        try:
            await conn.execute(
                "UPDATE user_balances SET balance = balance - $1, images_generated = images_generated + 1 WHERE user_id = $2",
                IMAGE_PRICE,
                user.id,
            )
            logger.info(
                "Image generated for user %s. Balance deducted by %s.",
                user.id,
                IMAGE_PRICE,
            )
        finally:
            await conn.close()

    except Exception as e:
        logger.error("Error generating image for prompt: '%s': %s", prompt, e)
        await update.message.reply_text(
            "Sorry, there was an error generating your image.",
            reply_to_message_id=update.message.message_id,
        )


async def gpt_prompt(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate a response to the user's text message using GPT."""
    user_message = update.message.text
    user = update.effective_user

    if not await is_user_allowed(user.id):
        logger.info(
            "User %s (%s) tried to use GPT prompt but is not allowed.",
            user.id,
            user.username,
        )
        await update.message.reply_text(
            "Sorry, you are not allowed to text with me.",
            reply_to_message_id=update.message.message_id,
        )
        return

    # logger.info("Пользователь написал сообщение {0}".format(user_message))

    logger.info(
        "User %s (%s) requested sent text: '%s'", user.id, user.username, user_message
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are comrade ho chi minh"},
                {"role": "user", "content": user_message},
            ],
        )
        # Access text content from "message" within the first "Choice"
        ai_response = response.choices[0].message.content
        await update.message.reply_text(ai_response.strip())
    except Exception as e:
        logger.error("Error generating AI response: %s", e)
        await update.message.reply_text(
            "Sorry, I couldn't process your message at the moment.",
            reply_to_message_id=update.message.message_id,
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
    # application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    if os.getenv("MODE") == "prod":

        application.run_webhook(
            listen="0.0.0.0",
            port=80,
            secret_token=os.getenv("SECRET_TOKEN_FOR_WEB_HOOK"),
            allowed_updates=Update.ALL_TYPES,
            webhook_url="https://webhook.comrade-ho-chi-minh.space/",
            
        )
    else:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        


def run_flask():
    """Run the Flask app."""
    app.run(debug=False)


if __name__ == "__main__":
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    main()

#
