import discord

from discord import app_commands
from discord.ext import commands

from utils.checks import check_channel

from ui.match_view import MatchView


class Matches(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="themtran",
        description="Thêm trận đấu"
    )
    async def themtran(
        self,
        interaction: discord.Interaction
    ):

        if not await check_channel(interaction):
            return

        embed = discord.Embed(
            title="🎥 NHÀ ĐÀI PESHUB",
            description=(
                "Chọn đầy đủ thông tin trận đấu bên dưới.\n\n"
                "🏆 Mùa\n"
                "🥇 Vòng\n"
                "👤 Người 1\n"
                "👤 Người 2"
            ),
            color=discord.Color.red()
        )

        embed.set_footer(
            text="PESHUB • Lưu trữ trận đấu"
        )

        await interaction.response.send_message(
            embed=embed,
            view=MatchView(),
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Matches(bot))
