import discord
from discord.ext import commands


class MyBot(discord.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Im logged in as {self.user}")
        print(f'Bot is ready!{self.is_ready()}')
        print(f"In {len(self.guilds)} guilds")
        print("-----------------------------")
