from telegram.ext import (ApplicationBuilder,
                          CommandHandler,
                          MessageHandler,
                          filters,
                          ConversationHandler,
                          CallbackQueryHandler)
from bot_logic.handler_help import help_command
from bot_logic.handler_start import start_command
from bot_logic.handler_location import (ASK_FOR_DESCRIPTION,
                                        ASK_FOR_TYPE,
                                        ASK_FOR_IMAGE,
                                        handle_location,
                                        ask_for_image,
                                        ask_for_type,
                                        ask_for_description)
from bot_logic.handler_cancel import cancel_callback, cancel_command
import settings

BOT_TOKEN = settings.BOT_TOKEN

def bot_start() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).arbitrary_callback_data(True).build()

    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("start", start_command))

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.LOCATION, handle_location)],
        states={
            ASK_FOR_IMAGE: [
                MessageHandler(filters.PHOTO, ask_for_image),
                CallbackQueryHandler(cancel_callback, pattern="^cancel$"),
            ],
            ASK_FOR_TYPE:[
                CallbackQueryHandler(ask_for_type),
                CallbackQueryHandler(cancel_callback, pattern="^cancel$"),
            ],
            ASK_FOR_DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_for_description),
                CommandHandler("cancel", cancel_command),
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
    )

    app.add_handler(conv_handler)

    print("Bot started successfully.")
    app.run_polling()