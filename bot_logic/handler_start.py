from telegram import Update
from telegram.ext import ContextTypes
import db_context.pg_context as pg_context

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE ) -> None:
    # Check if the user is already in the database if not create a new user
    user = None
    try:
        user = await pg_context.get_tg_user(update.effective_user.id)
        if not user:
            user = await pg_context.create_tg_user(
                id=update.effective_user.id,
                first_name=update.effective_user.first_name,
                last_name=update.effective_user.last_name,
                username=update.effective_user.username,
                language_code=update.effective_user.language_code
            )
    except Exception as e:
        print(f"Error getting user: {e}")
    finally:
        await pg_context.close_db()
    
    if user:
        await update.message.reply_text(f'Hello {user.first_name}, welcome to the Free Energy bot!')
    else:
        update.message.reply_text("Something went wrong while getting user data. Please type /start again.")