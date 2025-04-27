from telegram import BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from bot_logic.handler_help import help_command
from bot_logic.handler_start import start_command
from bot_logic.handler_share_location import handle_share_location
from bot_logic.handler_image import handle_image
from bot_logic.handler_socket_type import handle_socket_type
from bot_logic.handler_description import handle_description
from bot_logic.handler_cancel import cancel_callback, cancel_command
from bot_logic.handler_location import handle_location
from bot_logic.handler_save_location import handle_save_location
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
        entry_points=[CommandHandler('add_socket', handle_share_location)],
        states={
            rs.ASK_FOR_LOCATION: [
                MessageHandler(filters.LOCATION, handle_location),
                CallbackQueryHandler(cancel_callback, pattern="^CANCEL$"),
                CommandHandler("cancel", cancel_command),
            ],
            rs.ASK_FOR_IMAGE: [
                MessageHandler(filters.PHOTO, handle_image),
                CallbackQueryHandler(cancel_callback, pattern="^CANCEL$"),
            ],
            rs.ASK_FOR_TYPE:[
                CallbackQueryHandler(handle_socket_type),
                CallbackQueryHandler(cancel_callback, pattern="^CANCEL$"),
            ],
            rs.ASK_FOR_DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_description),
                CallbackQueryHandler(handle_description, pattern="^SKIP$"),
                CallbackQueryHandler(cancel_callback, pattern="^CANCEL$"),
                CommandHandler("cancel", cancel_command),
            ],
            rs.CONFIRM_SAVE: [
                CallbackQueryHandler(handle_save_location, pattern="^CONFIRM$"),
                CallbackQueryHandler(cancel_callback, pattern="^CANCEL$")
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
    )

    app.add_handler(conv_handler)

    print("Bot started successfully.")
    