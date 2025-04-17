from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from bot_logic.handler_help import help_command
from bot_logic.handler_start import start_command
from bot_logic.handler_location import SOCKET_TYPE, handle_location_entry, handle_selection
from bot_logic.handler_cancel import cancel_command
import settings

BOT_TOKEN = settings.BOT_TOKEN

def bot_start() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).arbitrary_callback_data(True).build()

    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("start", start_command))
    #app.add_handler(MessageHandler(filters.LOCATION, location_command))

    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.LOCATION, handle_location_entry)
        ],
        states={
            SOCKET_TYPE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_selection)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
    )
    app.add_handler(conv_handler)

    print("Bot started successfully.")
    app.run_polling()