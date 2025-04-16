import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from bot_logic.handler_help import help_command

load_dotenv()
TOKEN = os.getenv("BOT_GIS_TOKEN")

def bot_start() -> None:
    app = ApplicationBuilder().token(TOKEN).arbitrary_callback_data(True).build()

    app.add_handler(CommandHandler("help", help_command))

    print("Bot started successfully.")
    app.run_polling()