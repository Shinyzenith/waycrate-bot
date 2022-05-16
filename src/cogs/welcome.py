import logging
import os

import coloredlogs
import disnake
from disnake.ext import commands, tasks

test_guilds=[os.getenv("test_guild")]

log = logging.getLogger("Welcome cog")
coloredlogs.install(logger=log)


class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.warn(f"{self.__class__.__name__} Cog has been loaded")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(int(os.getenv("WELCOMECHANNEL")))
        await channel.send(f"<:crateway:970227529413693511> Welcome {member.mention}")

def setup(bot: commands.Bot):
    bot.add_cog(Welcome(bot))
