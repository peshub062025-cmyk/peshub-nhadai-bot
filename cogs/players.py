import discord
from discord import app_commands
from discord.ext import commands

from utils.checks import check_admin, check_channel
from ui.player_modal import PlayerModal


class Players(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="themnguoi",
        description="Thêm người chơi"
    )
    async def themnguoi(
        self,
        interaction: discord.Interaction
    ):

        if not await check_channel(interaction):
            return

        if not await check_admin(interaction):
            return

        await interaction.response.send_modal(
            PlayerModal()
        )


async def setup(bot):
    await bot.add_cog(
        Players(bot)
    )
