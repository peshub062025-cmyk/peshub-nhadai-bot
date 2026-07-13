import discord
from discord.ext import commands

from config import TOKEN

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():

    print("---------------------------")
    print("🎥 NHÀ ĐÀI PESHUB")
    print(f"Đăng nhập: {bot.user}")
    print("---------------------------")

bot.run(TOKEN)
