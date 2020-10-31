import os
from pathlib import Path

import dotenv
from nlogic.logger import init_logger
from pydantic import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent
FILES_DIR = Path(BASE_DIR, 'files')
FILES_DIR.mkdir(parents=True, exist_ok=True)

PAGES_DIR = Path(BASE_DIR, 'pages')
PAGES_DIR.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    DEBUG: bool = False
    DEV: bool = True

    ER_URL: str

    NLOGIC_LOGIN: str
    NLOGIC_PASSWORD: str
    SERVICE_NAME: str

    PG_HOST: str = 'localhost'
    PG_PORT: int = 5432
    PG_USER: str
    PG_DATABASE: str
    PG_PASSWORD: str

    def _pg_conn(self):
        return {
            'host': self.PG_HOST,
            'port': self.PG_PORT,
            'user': self.PG_USER,
            'database': self.PG_DATABASE,
            'password': self.PG_PASSWORD,
        }

    def db_conn(self):
        return {
            'connections': {
                'default': {
                    'engine': 'tortoise.backends.asyncpg',
                    'credentials': {**self._pg_conn()},
                }
            },
            'apps': {
                'models': {
                    'models': ['app.database.models'],
                    'default_connection': 'default'
                }
            }
        }

    class Config:
        os.environ['FASTAPI_TITLE'] = 'Nlogic-Site API'
        os.environ['FASTAPI_DESCRIPTION'] = 'nlogic site for hackaton'
        env_file = Path(BASE_DIR, 'settings', 'env')
        dotenv.load_dotenv(env_file)


settings = Settings()
init_logger(is_debug=settings.DEBUG)
