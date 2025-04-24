from telegram.ext import (ApplicationBuilder,
                          CommandHandler,
                          MessageHandler,
                          filters,
                          ConversationHandler,
                          CallbackQueryHandler)
from bot_logic.handler_help import help_command
from bot_logic.handler_start import start_command
import bot_logic.handler_location as hl
from bot_logic.handler_cancel import cancel_callback, cancel_command
import settings

BOT_TOKEN = settings.BOT_TOKEN

def bot_start() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).arbitrary_callback_data(True).build()

    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("start", start_command))

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.LOCATION, hl.handle_location)],
        states={
            hl.ASK_FOR_IMAGE: [
                MessageHandler(filters.PHOTO, hl.ask_for_image),
                CallbackQueryHandler(cancel_callback, pattern="^CANCEL$"),
            ],
            hl.ASK_FOR_TYPE:[
                CallbackQueryHandler(hl.ask_for_type),
                CallbackQueryHandler(cancel_callback, pattern="^CANCEL$"),
            ],
            hl.ASK_FOR_DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, hl.handle_description_input),
                CallbackQueryHandler(hl.handle_description_input, pattern="^SKIP$"),
                CallbackQueryHandler(cancel_callback, pattern="^CANCEL$"),
                CommandHandler("cancel", cancel_command),
            ],
            hl.CONFIRM_SAVE: [
                CallbackQueryHandler(hl.confirm_save, pattern="^CONFIRM$"),
                CallbackQueryHandler(cancel_callback, pattern="^CANCEL$")
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
    )

    app.add_handler(conv_handler)

    print("Bot started successfully.")
    app.run_polling()