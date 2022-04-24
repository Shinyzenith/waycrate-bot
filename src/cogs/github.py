import logging
from typing import Literal

import aiohttp
import coloredlogs
import disnake
from disnake.ext import commands, tasks

test_guilds=[870887565274808393]

log = logging.getLogger("Github cog")
coloredlogs.install(logger=log)

class Github(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.warn(f"{self.__class__.__name__} Cog has been loaded")

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
        await inter.response.send_message(f"{res['stargazers_count']}", ephemeral=True)

    async def api_call(self, call_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(call_url) as response:
                response = await response.json()
                return response

def setup(bot: commands.Bot):
    bot.add_cog(Github(bot))
