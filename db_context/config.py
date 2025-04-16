import settings

TORTOISE_ORM = {
    'connections': {'default': 'postgres://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@'
               f'{settings.POSTGRES_HOST}:{int(settings.POSTGRES_PORT)}/{settings.POSTGRES_DB}'},
    'apps': {
        'models': {
            'models': ['db_context.models', 'aerich.models'],
            'default_connections': 'default'
        },
    },
}