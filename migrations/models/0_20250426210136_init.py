from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "tg_user" (
    "id" BIGINT NOT NULL PRIMARY KEY,
    "first_name" VARCHAR(255) NOT NULL,
    "last_name" VARCHAR(255),
    "username" VARCHAR(255),
    "language_code" VARCHAR(10),
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_active" BOOL NOT NULL DEFAULT True
);
CREATE TABLE IF NOT EXISTS "tg_location" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "latitude" DOUBLE PRECISION NOT NULL,
    "longitude" DOUBLE PRECISION NOT NULL,
    "name" VARCHAR(255),
    "socket_type" VARCHAR(4) NOT NULL,
    "description" VARCHAR(2000),
    "layer" VARCHAR(500),
    "is_active" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "created_by_id" BIGINT NOT NULL REFERENCES "tg_user" ("id") ON DELETE CASCADE,
    "updated_by_id" BIGINT NOT NULL REFERENCES "tg_user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "tg_image" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "url" VARCHAR(10000) NOT NULL,
    "file_name" VARCHAR(1000),
    "file_id" VARCHAR(1000) NOT NULL,
    "file_size" INT NOT NULL DEFAULT 0,
    "description" VARCHAR(1000),
    "is_active" BOOL NOT NULL DEFAULT False,
    "file_saved" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "created_by_id" BIGINT NOT NULL REFERENCES "tg_user" ("id") ON DELETE CASCADE,
    "location_id" INT NOT NULL REFERENCES "tg_location" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
