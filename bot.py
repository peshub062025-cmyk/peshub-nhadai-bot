import discord
from discord.ext import commands
from discord import app_commands
from database.init_db import create_database
from config import TOKEN

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    create_database()
    print("=" * 40)
    print("🎥 NHÀ ĐÀI PESHUB")
    print(f"Đăng nhập thành công với tài khoản: {bot.user}")
    print("=" * 40)

    try:
        synced = await bot.tree.sync()
        print(f"✅ Đã đồng bộ {len(synced)} Slash Commands.")
    except Exception as e:
        print("❌ Lỗi đồng bộ Slash Commands:")
        print(e)


@bot.tree.command(
    name="ping",
    description="Kiểm tra trạng thái của NHÀ ĐÀI PESHUB"
)
async def ping(interaction: discord.Interaction):

    latency = round(bot.latency * 1000)

    embed = discord.Embed(
        title="🎥 NHÀ ĐÀI PESHUB",
        description="Bot đang hoạt động bình thường.",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="📡 Ping",
        value=f"{latency} ms",
        inline=False
    )

    embed.set_footer(text="PES Replay Bot v1.0")

    await interaction.response.send_message(
        embed=embed,
        ephemeral=True
    )


bot.run(TOKEN)
