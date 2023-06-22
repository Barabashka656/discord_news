import os
import logging

from bot.data.config import COGS_FOLDER
from bot.data.loader import bot


def load_cogs(ROOT_DIR):
    logging.exception(os.listdir(os.path.join(ROOT_DIR, 'bot', 'cogs')))
    dir = os.path.join(ROOT_DIR, COGS_FOLDER)
    print(dir)
    for name in os.listdir(os.path.join(ROOT_DIR, 'bot', 'cogs')):
        if name.endswith(".py") and os.path.isfile(os.path.join(COGS_FOLDER, name)):
            bot.load_extension(f"bot.cogs.{name[:-3]}")
