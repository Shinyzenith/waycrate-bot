import logging
from typing import Literal
import os
import aiohttp
import coloredlogs
import disnake
from disnake.ext import commands, tasks
from disnake.enums import TextInputStyle

test_guilds = [int(os.getenv("test_guild"))]

log = logging.getLogger("Github cog")
coloredlogs.install(logger=log)

class Github(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.stats_task.start()

    @commands.Cog.listener()
    async def on_ready(self):
        log.warn(f"{self.__class__.__name__} Cog has been loaded")
        await self.bot.change_presence(status=disnake.Status.idle, activity=disnake.Game("Waycrate"))

    @tasks.loop(seconds=1800, reconnect=False)
    async def stats_task(self):
        await self.bot.wait_until_ready()
        res = await api_call(f"{os.getenv('API_BASE_URL')}repos/waycrate/swhkd")
        chan = self.bot.get_channel(int(os.getenv("STATS_CHANNEL")))
        await chan.edit(name=f"Stars: {res['stargazers_count']} ⭐")


    @commands.slash_command(description="Get stats about WayCrate")
    @commands.guild_only()
    async def info(self, inter: disnake.ApplicationCommandInteraction, field: Literal["stars", "forks", "total"]):
        """Get information about waycrate tools.

        Parameters
        ----------
        field: The type of information you're looking for.
        """
        res = await api_call(f"{os.getenv('API_BASE_URL')}repos/waycrate/swhkd")
        if field == "stars":
            stars_embed = disnake.Embed(
                title="Stars", description=f"{res['stargazers_count']} stars", color=disnake.Color.from_rgb(221, 161, 4))
            await inter.response.send_message(embed=stars_embed)
        elif field == "forks":
            forks_embed = disnake.Embed(
                title="Forks", description=f"{res['forks_count']} forks", color=disnake.Color.from_rgb(221, 161, 4))
            await inter.response.send_message(embed=forks_embed)
        elif field == "total":
            res2 = await api_call(f"{os.getenv('API_BASE_URL')}orgs/waycrate/repos")
            embed = disnake.Embed(title="Total Stats", color=disnake.Color.from_rgb(221, 161, 4))
            embed.set_thumbnail(url="https://waycrate.github.io/assets/img/waycrate-logo.png")
            for x in res2:
             embed.add_field(name=x["name"], value=f"{x['stargazers_count']} stars")
            await inter.response.send_message(embed=embed)

    @commands.slash_command(description="Report a security vulnerability.")
    @commands.guild_only()
    async def security(self, inter: disnake.ApplicationCommandInteraction) -> None:
        await inter.response.send_modal(
            title="Report a Security Vunerability",
            custom_id="report1",
            components=[
                disnake.ui.TextInput(
                    label="Email",
                    placeholder="For Futher Contact",
                    custom_id="email",
                    style=TextInputStyle.short,
                    max_length=50,
                ),
                disnake.ui.TextInput(
                    label="Description Of The Bug",
                    placeholder="What does the bug do?",
                    custom_id="description",
                    style=TextInputStyle.paragraph,
                ),
                disnake.ui.TextInput(
                    label="How To Reproduce",
                    placeholder="How to reproduce the bug?",
                    custom_id="reproduce",
                    style=TextInputStyle.paragraph,
                ),
            ],
        )

        modal_inter: disnake.ModalInteraction = await self.bot.wait_for(
            "modal_submit",
            check=lambda i: i.custom_id == "report1" and i.author.id == inter.author.id,
        )

        embed = disnake.Embed(title="New Report", color=disnake.Colour.red())
        channel = self.bot.get_channel(int(os.getenv("VUNERABLE_CHANNEL")))
        for key, value in modal_inter.text_values.items():
            embed.add_field(name=key.capitalize(), value=value, inline=False)
        await modal_inter.response.send_message("Thanks for reporting!", empheral=True)
        await channel.send(embed=embed)  

async def api_call(call_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(call_url) as response:
            response = await response.json()
            return response


def setup(bot: commands.Bot):
    bot.add_cog(Github(bot))
