from telegram import BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from bot_logic.handler_help import help_command
from bot_logic.handler_start import start_command
from bot_logic.handler_share_location import share_location_command
import bot_logic.handler_location as hl
from bot_logic.handler_cancel import cancel_callback, cancel_command
import settings
import bot_logic.return_states as rs

BOT_TOKEN = settings.BOT_TOKEN

async def tg_bot_start(app: Application) -> None:

    await app.bot.set_my_commands([
        BotCommand('add_socket', 'Add a socket location'),
        #BotCommand('search', 'Search for a socket location'),
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Get help"),
    ])

    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("start", start_command))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add_socket', share_location_command)],
        states={
            rs.ASK_FOR_LOCATION: [
                MessageHandler(filters.LOCATION, hl.handle_location),
                CallbackQueryHandler(cancel_callback, pattern="^CANCEL$"),
                CommandHandler("cancel", cancel_command),
            ],
            rs.ASK_FOR_IMAGE: [
                MessageHandler(filters.PHOTO, hl.ask_for_image),
                CallbackQueryHandler(cancel_callback, pattern="^CANCEL$"),
            ],
            rs.ASK_FOR_TYPE:[
                CallbackQueryHandler(hl.ask_for_type),
                CallbackQueryHandler(cancel_callback, pattern="^CANCEL$"),
            ],
            rs.ASK_FOR_DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, hl.handle_description_input),
                CallbackQueryHandler(hl.handle_description_input, pattern="^SKIP$"),
                CallbackQueryHandler(cancel_callback, pattern="^CANCEL$"),
                CommandHandler("cancel", cancel_command),
            ],
            rs.CONFIRM_SAVE: [
                CallbackQueryHandler(hl.confirm_save, pattern="^CONFIRM$"),
                CallbackQueryHandler(cancel_callback, pattern="^CANCEL$")
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
    )

    app.add_handler(conv_handler)

    print("Bot started successfully.")
    