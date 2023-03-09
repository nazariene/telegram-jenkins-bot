#!/usr/bin/env python
import logging

from telegram import __version__ as TG_VER

from handlers.run_handlers import run_handler
from service.config import config

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram.ext import (
    Application,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    token = config.get('telegram', 'token')
    application = Application.builder().token(token).build()
    application.add_handler(run_handler())
    application.run_polling()


if __name__ == "__main__":
    main()
