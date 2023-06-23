import logging
import io

from bot.data.config import (
    VK_LOGIN,
    VK_PASSWORD,
    VK_GROUP_ID,
    CHANNEL_ID
)

import aiohttp
import vk_api
import discord
from discord.ext import (
    commands,
    tasks
)


logger = logging.getLogger(__name__)

class VkCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channel: discord.channel.TextChannel | discord.TextChannel = 123

        self.vk: vk_api.VkApi = self.connect_to_vk()
        self.vk_group_id = VK_GROUP_ID

        self._post_id = 0
        self._last_post = '0'

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.bot.get_channel(CHANNEL_ID)
        self.get_last_post.start()
        self.handle_pinned.start()
        
    @tasks.loop(hours=3)
    async def handle_pinned(self):
        response = self.vk.wall.get(owner_id=self.vk_group_id, count=1).get('items')[0]
        if response.get('is_pinned'):
            self._post_id = 1
        else:
            self._post_id = 0

    @tasks.loop(minutes=5)
    async def get_last_post(self):
        count = self._post_id
        response = self.vk.wall.get(owner_id=self.vk_group_id, count=count+1).get('items')[count]

        if response.get('hash') == self._last_post:
            return
        self._last_post = response.get('hash')
        response_text = response.get('text')
        if response.get('copy_history'):
            return 
        
        photo_urls, video_urls = self.get_urls_from_response(response=response)
        photo_files = []
        # this flag is for sending text once
        while photo_urls or video_urls:
            if video_urls:
                if response_text:
                    await self.channel.send(content=response_text+video_urls.pop())
                    response_text = None
                else:
                    await self.channel.send(content=video_urls.pop())
            if photo_urls:
                photo = await self.send_photo_by_url(photo_urls.pop())
                photo_files.append(photo)

        if len(photo_files) == 1:
            await self.channel.send(content=response_text, file=photo_files[0])
        elif len(photo_files) > 1:
            await self.channel.send(content=response_text, files=photo_files)
        else:
            logger.warning(response)

    def connect_to_vk(self):
        vk_session: vk_api.VkApi = vk_api.VkApi(
            login=VK_LOGIN, 
            password=VK_PASSWORD,
            config_filename='bot/data/vk_config.v2.json'
        )
        vk_session.auth(token_only=True)
        return vk_session.get_api()

    def get_urls_from_response(self, response: dict):
        photo_urls = []
        video_urls = []
        attachment_list = response.get('attachments')
        for i, attachment in enumerate(attachment_list):
            if attachment.get('type') == 'photo':
                max_size = 0
                for photo in attachment.get('photo').get('sizes'):
                  
                    if photo.get('width') > max_size:
                        if not len(photo_urls) == i+1:
                            photo_urls.append(photo.get('url'))
                        photo_urls[i] = photo.get('url')
                        max_size = photo.get('width')
            if attachment.get('type') == 'video':
                video_obj = attachment.get('video')
                owner_id = video_obj.get('owner_id')
                video_id = video_obj.get('id')
                access_key = video_obj.get('access_key')
                video = self.vk.video.get(videos=f'{owner_id}_{video_id}_{access_key}')
                video_urls.append(video.get('items')[0].get('player'))
        return photo_urls, video_urls

    async def send_photo_by_url(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    rs = await r.read()
                    with io.BytesIO(rs) as file:
                        return discord.File(file,  "AlexIsAPrettyCoolGuy.png")
        

def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)

def setup(bot: commands.Bot):
    bot.add_cog(VkCog(bot))
    print(f"> Extension {__name__} is ready")