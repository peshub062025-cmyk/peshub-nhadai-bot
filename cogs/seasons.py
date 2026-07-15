import discord

from discord import app_commands
from discord.ext import commands

from utils.checks import check_admin
from utils.checks import check_channel

from ui.season_modal import SeasonModal


class Seasons(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="muamoi",
        description="Thêm mùa giải"
    )
    async def muamoi(
        self,
        interaction: discord.Interaction
    ):

        if not await check_channel(interaction):
            return

        if not await check_admin(interaction):
            return

        await interaction.response.send_modal(
            SeasonModal()
        )


async def setup(bot):
    await bot.add_cog(
        Seasons(bot)
    )
