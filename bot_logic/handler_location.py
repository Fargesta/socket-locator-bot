from telegram import Update
from telegram.ext import ContextTypes
import db_context.pg_context as pg_context

async def location_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = None
    try:
        user = await pg_context.get_tg_user(update.effective_user.id)
        if not user:
            raise Exception("User not found in the database.")
        
        await pg_context.create_tg_location(
            latitude=update.message.location.latitude,
            longitude=update.message.location.longitude,
            name="Test",
            socket_type="220",
            description="First location",
            layer="Test",
            created_by=user
        )
        
    except Exception as e:
        print(f"Something went wrong: {e}")
    finally:
        await pg_context.close_db()