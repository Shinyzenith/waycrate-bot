import logging
from typing import Literal
import os
import aiohttp
import coloredlogs
import disnake
from disnake.ext import commands, tasks

test_guilds=[int(os.getenv("test_guild"))]

log = logging.getLogger("Github cog")
coloredlogs.install(logger=log)

            
class Github(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.stats_task.start()

    @commands.Cog.listener()
    async def on_ready(self):
        log.warn(f"{self.__class__.__name__} Cog has been loaded")

    @tasks.loop(seconds=1800, reconnect=False)
    async def stats_task(self):
        await self.bot.wait_until_ready()
        res = await api_call(f"{os.getenv('API_BASE_URL')}repos/waycrate/swhkd")
        chan = self.bot.get_channel(int(os.getenv("STATS_CHANNEL")))
        await chan.edit(name=f"Stars: {res['stargazers_count']} ⭐")


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
            await inter.response.send_message(f"{res['stargazers_count']} stars")
        elif field == "forks":
            await inter.response.send_message(f"{res['forks']} forks")
            
    @commands.slash_command(guild_ids=test_guilds)
    @commands.cooldown(10, 60, commands.BucketType.guild)
    @commands.guild_only()
    async def report(self, inter: disnake.ApplicationCommandInteraction):
        """Report a security vunerability.

        Parameters
        ----------
        field: The type of information you're looking for.
        """
        await inter.response.send_modal(modal=ReportModal())
        
        
class ReportModal(disnake.ui.Modal):
    def __init__(self) -> None:
        components = [
                disnake.ui.TextInput(
                label="Email",
                placeholder="Your email for futher communication",
                custom_id="email",
                style=disnake.TextInputStyle.short,
                min_length=5,
                max_length=30,
            ),
            disnake.ui.TextInput(
                label="Description",
                placeholder="The description of the bug",
                custom_id="description",
                style=disnake.TextInputStyle.paragraph,
                min_length=20,
                max_length=1024,
            ),
            disnake.ui.TextInput(
                label="How to reproduce",
                placeholder="How to reproduce the bug",
                custom_id="content",
                style=disnake.TextInputStyle.paragraph,
                min_length=30,
                max_length=1024,
            ),
        ]
        super().__init__(title="Report a Security Vunerability", custom_id="create_tag", components=components)

    async def callback(self, inter: disnake.ModalInteraction) -> None:
        embed = disnake.Embed(title="New Vunerability", color=0xFF0000)
        for key, value in inter.text_values.items():
            embed.add_field(name=key.capitalize(), value=value, inline=False)
        await inter.response.send_message(embed=embed)



async def api_call(call_url):
    async with aiohttp.ClientSession() as session:
            async with session.get(call_url) as response:
                response = await response.json()
                return response


def setup(bot: commands.Bot):
    bot.add_cog(Github(bot))
