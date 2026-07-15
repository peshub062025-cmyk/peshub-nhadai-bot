import discord

from discord import app_commands
from discord.ext import commands

from utils.checks import check_channel

from ui.search_view import SearchView


class Search(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="timkiem",
        description="Tìm kiếm trận đấu"
    )
    async def timkiem(
        self,
        interaction: discord.Interaction
    ):

        if not await check_channel(interaction):
            return

        # Nếu muốn tất cả mọi người đều dùng được thì bỏ đoạn này.
        # Nếu chỉ Admin được dùng thì giữ lại.

        # if not await check_admin(interaction):
        #     return

        embed = discord.Embed(
            title="🎥 NHÀ ĐÀI PESHUB",
            description=(
                "🏆 Chọn mùa giải\n"
                "👤 Chọn Người chơi 1\n"
                "👤 Chọn Người chơi 2 (không bắt buộc)\n\n"
                "Sau đó bấm **🔍 Tìm kiếm**"
            ),
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(
            embed=embed,
            view=SearchView()
        )


async def setup(bot):
    await bot.add_cog(Search(bot))
