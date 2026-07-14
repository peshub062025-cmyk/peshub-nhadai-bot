import discord

from discord import app_commands
from discord.ext import commands

from sqlalchemy.orm import Session

from database.db import SessionLocal
from database.models import Player

from utils.checks import check_admin
from utils.checks import check_channel

from ui.player_modal import PlayerModal
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
