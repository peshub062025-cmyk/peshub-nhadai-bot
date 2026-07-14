import discord

from discord import app_commands
from discord.ext import commands

from sqlalchemy.orm import Session

from database.db import SessionLocal
from database.models import Player

from utils.checks import check_admin
from utils.checks import check_channel


class Players(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


    @app_commands.command(
        name="themnguoi",
        description="Thêm người chơi mới"
    )

    async def themnguoi(
        self,
        interaction: discord.Interaction,
        ten: str
    ):

        if not await check_channel(interaction):
            return

        if not await check_admin(interaction):
            return

        db: Session = SessionLocal()

        try:

            player = db.query(Player).filter(
                Player.name == ten
            ).first()

            if player:

                await interaction.response.send_message(
                    "⚠ Người chơi đã tồn tại.",
                    ephemeral=True
                )

                return

            new_player = Player(
                name=ten
            )

            db.add(new_player)

            db.commit()

            await interaction.response.send_message(

                f"""🎥 **NHÀ ĐÀI PESHUB**

✅ Đã thêm người chơi:

**{ten}**
                """

            )

        finally:

            db.close()


async def setup(bot):

    await bot.add_cog(
        Players(bot)
    )
