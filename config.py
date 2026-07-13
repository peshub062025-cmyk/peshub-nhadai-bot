import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

DATABASE_URL = os.getenv("DATABASE_URL")

GUILD_ID = int(os.getenv("GUILD_ID"))
