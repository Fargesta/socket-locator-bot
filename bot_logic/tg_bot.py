from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot_logic.handler_help import help_command
from bot_logic.handler_start import start_command
from bot_logic.handler_location import location_command
import settings

BOT_TOKEN = settings.BOT_TOKEN

def bot_start() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).arbitrary_callback_data(True).build()

    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.LOCATION, location_command))

    print("Bot started successfully.")
    app.run_polling()