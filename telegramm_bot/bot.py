from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import os


application = Application.builder().token("TOKEN").build()
application.add_handler(CommandHandler("start", start))
application.run_polling(allowed_updates=Update.ALL_TYPES)