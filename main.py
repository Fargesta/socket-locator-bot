import os
from dotenv import load_dotenv
import db_context.pg_context as pg_context
from tortoise import run_async
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main() -> None:
    run_async(pg_context.init_db())
    print("Database initialized successfully.")

if __name__ == "__main__":
    main()