import io

from bot.data.config import (
    VK_LOGIN,
    VK_PASSWORD,
    VK_GROUP_ID,
    VK_TOKEN,
    CHANNEL_ID,
    APP_ID
)
import aiohttp
import json
import discord
import vk_api
from discord.ext import (
    commands,
    tasks
)



    
class VkCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channel: discord.channel.TextChannel = 123

        self.vk: vk_api.VkApi = self.connect_to_vk()
        self.vk_group = self.vk_group_id(VK_GROUP_ID)

        post = self.vk.wall.get(owner_id=VK_GROUP_ID, count=2)
        self.last_post = post.get('items')[1].get('hash')
        with open("file2.txt", 'w') as f:
            f.write(json.dumps(post))

        self.get_last_post.start()


    def connect_to_vk(self):
        vk_session: vk_api.VkApi = vk_api.VkApi(login=VK_LOGIN, 
                                                token=VK_TOKEN, 
                                                password=VK_PASSWORD, 
                                                app_id=APP_ID, 
                                                scope=73728)
        #vk_session: vk_api.VkApi = vk_api.VkApi(
        #    login=VK_LOGIN, 
        #    password=VK_PASSWORD, 
        #    captcha_handler=captcha_handler
        #)
        vk_session.auth()
        return vk_session.get_api()
    
    def vk_group_id(self, vk_group_id):
        return self.bot.get_guild(vk_group_id)

    @commands.Cog.listener()
    async def on_ready(self):
        print("ready")
        self.channel = self.bot.get_channel(CHANNEL_ID)

    @tasks.loop(seconds=5)
    async def get_last_post(self):
        print('a1')
        if not self.bot.is_ready():
            return
        print('a2')
        response = self.vk.wall.get(owner_id=VK_GROUP_ID, count=1).get('items')[0]
        if response.get('hash') == self.last_post:
            return
        print('a3')
        self.last_post = response.get('hash')
        response_text = response.get('text')
        photo_urls = []
        attachment_list = response.get('attachments')
        print('a4', response_text)
        for i, attachment in enumerate(attachment_list):
            if attachment.get('type') == 'photo':
                max_size = 0
                for photo in attachment.get('photo').get('sizes'):
                  
                    if photo.get('width') > max_size:
                        if not len(photo_urls) == i+1:
                            photo_urls.append(photo.get('url'))
                        photo_urls[i] = photo.get('url')
                        max_size = photo.get('width')
        files = [1]
        print('a5')
        if len(files) == 1:
            print('a6')
            await self.get_file_by_url(photo_urls[0], response_text)
        else:
            print('a6.1')
            pass
            #await self.channel.send(fcontent=response_text, files=files)

    async def get_file_by_url(self, url, response_text):
        print('a7')
        async with aiohttp.ClientSession() as session:
            print('a8')
            async with session.get(url) as r:
                print('a9')
                if r.status == 200:
                    print('a10')
                    rs = await r.read()
                    with io.BytesIO(rs) as file: # converts to file-like object
                        print('a11')
                        await self.channel.send(content=response_text, file=discord.File(file,  "testimage.png"))

def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)

def setup(bot: commands.Bot):
    bot.add_cog(VkCog(bot))
    print(f"> Extension {__name__} is ready")