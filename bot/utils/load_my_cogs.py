import os
import logging

from bot.data.config import COGS_FOLDER
from bot.data.loader import bot


def load_cogs(ROOT_DIR):
    logging.exception(os.listdir(os.path.join(ROOT_DIR, 'bot', 'cogs')))
    dir = os.path.join(ROOT_DIR, COGS_FOLDER)
    print(dir)
    for name in os.listdir(os.path.join(ROOT_DIR, 'bot', 'cogs')):
        print(name, 'name1')
        print(os.path.join(COGS_FOLDER, name), 'name2')
        print(os.path.isfile(os.path.join(COGS_FOLDER, name)), 'name3')
        if name.endswith(".py") and os.path.isfile(os.path.join(COGS_FOLDER, name)):
            print(name)
            print(f"bot.cogs.{name[:-3]}")
            bot.load_extension(f"bot.cogs.{name[:-3]}")
