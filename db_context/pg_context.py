from tortoise import Tortoise
from db_context.models import TG_user, TG_location, TG_image
import settings


async def init_db() -> None:
    await Tortoise.init(
        db_url=f'postgres://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@'
               f'{settings.POSTGRES_HOST}:{int(settings.POSTGRES_PORT)}/{settings.POSTGRES_DB}',
        modules={'models': ['db_context.models', 'aerich.models']}
    )

async def close_db() -> None:
    await Tortoise.close_connections()

async def create_tg_user(
        id: int,
        first_name: str,
        last_name: str | None = None,
        username: str | None = None,
        language_code: str | None = None,
) -> TG_user:
    user = await TG_user.create(
        id=id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        language_code=language_code,
    )
    return user

async def create_tg_location(
        latitude: float,
        longitude: float,
        name: str | None = None,
        socket_type: str | None = None,
        description: str | None = None,
        layer: str | None = None,
        created_by: TG_user | None = None,
) -> TG_location:
    location = await TG_location.create(
        latitude=latitude,
        longitude=longitude,
        name=name,
        socket_type=socket_type,
        description=description,
        layer=layer,
        updated_by=created_by,
        created_by=created_by
    )
    return location

async def get_tg_user(user_id: int) -> TG_user | None:
    user = await TG_user.get_or_none(id=user_id)
    return user

async def get_tg_location(location_id: int) -> TG_location | None:
    location = await TG_location.get_or_none(id=location_id)
    return location