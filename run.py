from bot.data.config import DISCORD_TOKEN
from bot.data.loader import bot
from bot.utils.load_my_cogs import load_cogs
from bot.utils.my_logger import configure_logger


def main():
    configure_logger()
    load_cogs()
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
