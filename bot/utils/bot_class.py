

import vk_api
import discord
from discord.ext import commands




########### response = vk.wall.get(owner_id=-123456789, count=10)
########### 
########### for post in response['items']:
###########     print(post['text'])


class MyBot(discord.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self._activity = set_status_activity()
        
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Im logged in as {self.user}")
        print(f'Bot is ready!{self.is_ready()}')
        print(f"In {len(self.guilds)} guilds")
        print("-----------------------------")
