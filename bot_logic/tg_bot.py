from telegram.ext import (ApplicationBuilder,
                          CommandHandler,
                          MessageHandler,
                          filters,
                          ConversationHandler,
                          CallbackQueryHandler)
from bot_logic.handler_help import help_command
from bot_logic.handler_start import start_command
from bot_logic.handler_location import (ADD_DESCRIPTION,
                                        WAITNG_FOR_TYPE,
                                        ask_type,
                                        ask_type_callback,
                                        handle_description)
from bot_logic.handler_cancel import cancel_callback, cancel_command
import settings

BOT_TOKEN = settings.BOT_TOKEN

def bot_start() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).arbitrary_callback_data(True).build()

    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("start", start_command))

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.LOCATION, ask_type)],
        states={
            WAITNG_FOR_TYPE: [
                CallbackQueryHandler(ask_type_callback)
            ],
            ADD_DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_description),
                CommandHandler("cancel", cancel_command),
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
    )

    app.add_handler(conv_handler)

    print("Bot started successfully.")
    app.run_polling()