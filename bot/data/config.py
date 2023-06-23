import os

from dotenv import (
    load_dotenv,
    find_dotenv
)


load_dotenv(find_dotenv())

VK_LOGIN = os.getenv('VK_LOGIN')
VK_PASSWORD = os.getenv('VK_PASSWORD')
VK_GROUP_ID = os.getenv('VK_GROUP_ID')


DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
if 0:
    CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
else:
    CHANNEL_ID = int(os.getenv('TEST_CHANNEL_ID'))
