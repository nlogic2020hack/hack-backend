import uvicorn
from nlogic.logger.configs import UVICORN_LOGGING_CONFIG
from tortoise import run_async

from settings.config import settings
from app.app import app
from app.database.models import Pages

uvicorn.Config(
    app=app,
    proxy_headers=True,
    access_log=False,
    use_colors=False,
    log_config=UVICORN_LOGGING_CONFIG,
)

if __name__ == '__main__':
    # run_async(Pages.create_index())
    uvicorn.run(app=app, port=7999, debug=settings.DEBUG, log_config=UVICORN_LOGGING_CONFIG)
