import io

from bot.data.config import (
    VK_LOGIN,
    VK_PASSWORD,
    VK_GROUP_ID,
    GUILD_ID,
    CHANNEL_ID
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
        self.vk: vk_api.VkApi = self.connect_to_vk()

        self.channel: discord.channel.TextChannel = 123
        self.vk_group = self.vk_group_id(VK_GROUP_ID)
        post = self.vk.wall.get(owner_id=VK_GROUP_ID, count=2)
        self.last_post = post.get('items')[1].get('hash')
        with open("file2.txt", 'w') as f:
            f.write(json.dumps(post))

        self.get_last_post.start()


    def connect_to_vk(self):
        vk_session: vk_api.VkApi = vk_api.VkApi(VK_LOGIN, VK_PASSWORD)
        vk_session.auth()
        return vk_session.get_api()
    
    def vk_group_id(self, vk_group_id):
        return self.bot.get_guild(vk_group_id)

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.bot.get_channel(CHANNEL_ID)

    @tasks.loop(seconds=5)
    async def get_last_post(self):

        if not self.bot.is_ready():
            return
   
        
        response = self.vk.wall.get(owner_id=VK_GROUP_ID, count=1).get('items')[0]
        if response.get('hash') == self.last_post:
          
            return
        
        self.last_post = response.get('hash')
        response_text = response.get('text')
        photo_urls = []
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
                        
        
    
        files = [1]
        
        if len(files) == 1:
            await self.get_file_by_url(photo_urls[0], response_text)
        else:
            pass
            #await self.channel.send(fcontent=response_text, files=files)

    async def get_file_by_url(self, url, response_text):
      
        async with aiohttp.ClientSession() as session:
           
            async with session.get(url) as r:
              
                if r.status == 200:
                  
                    rs = await r.read()
                    with io.BytesIO(rs) as file: # converts to file-like object
                        await self.channel.send(content=response_text, file=discord.File(file,  "testimage.png"))

                    

def setup(bot: commands.Bot):
    bot.add_cog(VkCog(bot))
    print(f"> Extension {__name__} is ready")