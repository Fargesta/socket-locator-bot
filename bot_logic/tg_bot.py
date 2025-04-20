from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler
from bot_logic.handler_help import help_command
from bot_logic.handler_start import start_command
from bot_logic.handler_location import ask_type, save_location, WAITNG_FOR_TYPE
from bot_logic.handler_cancel import cancel_callback, cancel_command
import settings

BOT_TOKEN = settings.BOT_TOKEN

def bot_start() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).arbitrary_callback_data(True).build()

    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("cancel", cancel_command))

    conv_handler = ConversationHandler(
        
    )

    print("Bot started successfully.")
    app.run_polling()