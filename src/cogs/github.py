import logging
from typing import Literal
import os
import aiohttp
import coloredlogs
import disnake
from disnake.ext import commands, tasks
from pydantic import Field

test_guilds=[int(os.getenv("test_guild"))]

log = logging.getLogger("Github cog")
coloredlogs.install(logger=log)

            
class Github(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.warn(f"{self.__class__.__name__} Cog has been loaded")

    @tasks.loop(seconds=3000, reconnect=False)
    async def notify_task(self):
        await self.bot.wait_until_ready()
        res = await api_call(f"{os.getenv('API_BASE_URL')}repos/waycrate/swhkd")
        chan = self.bot.get_channel(int(os.getenv("STATS_CHANNEL")))
        chan.edit(name=f"Stars: {res['stargazers_count']} ⭐")

            




    @commands.slash_command(guild_ids=test_guilds)
    @commands.cooldown(10, 60, commands.BucketType.guild)
    @commands.guild_only()
    async def get_info(self, inter: disnake.ApplicationCommandInteraction, field:Literal["stars", "forks"]):
        """Get information about waycrate tools.

        Parameters
        ----------
        field: The type of information you're looking for.
        """
        res = await api_call(f"{os.getenv('API_BASE_URL')}repos/waycrate/swhkd")
        if field == "stars":
            await inter.response.send_message(f"{res['stargazers_count']}", ephemeral=True)
        elif field == "forks":
            await inter.response.send_message(f"{res['forks']}", ephemeral=True)

async def api_call(call_url):
    async with aiohttp.ClientSession() as session:
            async with session.get(call_url) as response:
                response = await response.json()
                return response


def setup(bot: commands.Bot):
    bot.add_cog(Github(bot))
