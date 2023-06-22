import os

from dotenv import (
    load_dotenv,
    find_dotenv
)


load_dotenv(find_dotenv())
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

VK_TOKEN = os.getenv('VK_TOKEN')
VK_LOGIN = os.getenv('VK_LOGIN')
VK_PASSWORD = os.getenv('VK_PASSWORD')
VK_GROUP_ID = os.getenv('VK_GROUP_ID')
APP_ID = os.getenv('APP_ID')
USER_AGENT = os.getenv('USER_AGENT')
IP_TOKEN = os.getenv('IP_TOKEN')

COGS_FOLDER = os.getenv('COGS_FOLDER')
LOGS_FOLDER = os.getenv('LOGS_FOLDER')

GUILD_ID = int(os.getenv('GUILD_ID'))
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))




