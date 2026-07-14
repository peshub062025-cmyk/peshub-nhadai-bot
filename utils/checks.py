import discord

from config import BOT_CHANNEL_ID
from config import ADMIN_USER_IDS


async def check_channel(interaction: discord.Interaction):

    if interaction.channel.id != BOT_CHANNEL_ID:

        await interaction.response.send_message(
            "⛔ Bot chỉ hoạt động trong kênh đã chỉ định.",
            ephemeral=True
        )

        return False

    return True


async def check_admin(interaction: discord.Interaction):

    if interaction.user.id not in ADMIN_USER_IDS:

        await interaction.response.send_message(
            "⛔ Bạn không có quyền sử dụng lệnh này.",
            ephemeral=True
        )

        return False

    return True
