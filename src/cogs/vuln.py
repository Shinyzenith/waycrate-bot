import logging
import os
from typing import List, Literal

import coloredlogs
import disnake
from disnake.enums import TextInputStyle
from disnake.ext import commands

test_guilds = [os.getenv("test_guild")]

log = logging.getLogger("Vulnerability cog")
coloredlogs.install(logger=log)

class Vulnerability(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.warn(f"{self.__class__.__name__} Cog has been loaded")

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

def setup(bot: commands.Bot):
    bot.add_cog(Vulnerability(bot))
