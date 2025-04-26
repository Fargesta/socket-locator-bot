import db_context.pg_context as pg_context
from tortoise import run_async
import logging
import settings
from telegram.ext import ApplicationBuilder
from file_context.g_drive import gdrive_bot_start
from bot_logic.tg_bot import tg_bot_start
import asyncio

BOT_TOKEN = settings.BOT_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).arbitrary_callback_data(True).build()

    await pg_context.init_db()
    await pg_context.setup_user_roles()
    print("Database initialized successfully.")

    await gdrive_bot_start(app)

    await tg_bot_start(app)
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        await asyncio.Future()
    except KeyboardInterrupt:
        pass
    finally:
        await app.updater.stop()
        await app.stop()


if __name__ == "__main__":
    asyncio.run(main())