import io
import requests


from bot.data.config import (
    VK_LOGIN,
    VK_PASSWORD,
    VK_GROUP_ID,
    VK_TOKEN,
    CHANNEL_ID,
    APP_ID,
    IP_TOKEN,
    USER_AGENT
)
import aiohttp
import json
import discord
import vk_api
from discord.ext import (
    commands,
    tasks
)
from bs4 import BeautifulSoup


    
class VkCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channel: discord.channel.TextChannel | discord.TextChannel = 123

        self.vk: vk_api.VkApi = self.connect_to_vk()
        self._count = 0
        self.vk_group = self.vk_group_id(VK_GROUP_ID)
        post = self.vk.wall.get(owner_id=VK_GROUP_ID, count=self._count+2)
        self.last_post = post.get('items')[self._count+1].get('hash')
        with open("file2.txt", 'w') as f:
            f.write(json.dumps(post))

        self.get_last_post.start()


    def connect_to_vk(self):
        proxies = {
            'http': 'http://31.44.82.2:3128',
            'https': 'http://31.44.82.2:3128'
        }
        headers = {
            'User-Agent': USER_AGENT    
        }
        session = requests.Session()
        session.proxies.update(proxies)
        session.proxies.update(headers)
        vk_session: vk_api.VkApi = vk_api.VkApi(login=VK_LOGIN, 
                                                password=VK_PASSWORD
                                                )

        vk_session.http.headers['User-agent'] = USER_AGENT
        vk_session.http.proxies['http'] = 'http://195.19.250.2:3126'
        vk_session.http.proxies['https'] = 'http://195.19.250.2:3126'

            
        
        response_1 = vk_session.http.get(f'https://ipinfo.io/json?token={IP_TOKEN}')
        print(response_1.text)
        #response = requests.get(url="https://api.ipify.org", headers=headers, proxies=proxies)
       
        
        
        #vk_session: vk_api.VkApi = vk_api.VkApi(
        #    login=VK_LOGIN, 
        #    password=VK_PASSWORD, 
        #    captcha_handler=captcha_handler
        #)
        vk_session.auth(token_only=True)
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
        response = self.vk.wall.get(owner_id=VK_GROUP_ID, count=self._count+1).get('items')[self._count]
        if response.get('hash') == self.last_post:
            return
        print('a3')
        print(response)
        self.last_post = response.get('hash')
        if response.get('copy_history'):
            return 
        response_text = response.get('text')
        photo_urls = []
        video_urls = []
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
            if attachment.get('type') == 'video':
                video_obj = attachment.get('video')
                owner_id = video_obj.get('owner_id')
                video_id = video_obj.get('id')
                access_key = video_obj.get('access_key')
                video = self.vk.video.get(videos=f'{owner_id}_{video_id}_{access_key}')
                print(video)
                print(video.get('items')[0])
                print(video.get('items')[0].get('player'))
                video_urls.append(video.get('items')[0].get('player'))
        print('a5')
        files = 1
        flag = 1
        photo_files = []
        while photo_urls or video_urls:
            if video_urls:
                await self.channel.send(content=response_text, video=video_urls.pop())
            if photo_urls:
                photo = await self.send_photo_by_url(photo_urls.pop())
                photo_files.append(photo)
        
        if len(photo_files) == 1:
            await self.channel.send(content=response_text, file=photo_files[0])
        elif len(photo_files) > 1:
            await self.channel.send(content=response_text, files=photo_files)
        else:
            print(photo_files, photo_files, response_text)
        return
        if len(files) == 1:
            print('a6')
            await self.get_file_by_url(photo_urls[0], response_text)
        else:
            print('a6.1')
            pass
            #await self.channel.send(fcontent=response_text, files=files)

    async def send_photo_by_url(self, url, response_text=None):
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
                        return discord.File(file,  "testimage.png")
                        await self.channel.send(content=response_text, file=discord.File(file,  "testimage.png"))
                        #if response_text:
                        #    await self.channel.send(content=response_text, file=discord.File(file,  "testimage.png"))
                        #else:
                        #    await self.channel.send(file=discord.File(file,  "testimage.png"))

def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)

def setup(bot: commands.Bot):
    bot.add_cog(VkCog(bot))
    print(f"> Extension {__name__} is ready")