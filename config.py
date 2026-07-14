import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

BOT_CHANNEL_ID = int(os.getenv("BOT_CHANNEL_ID"))

ADMIN_USER_IDS = [
    int(x.strip())
    for x in os.getenv("ADMIN_USER_IDS", "").split(",")
    if x.strip()
]

ADMIN_ROLE_ID = os.getenv("ADMIN_ROLE_ID")
if ADMIN_ROLE_ID:
    ADMIN_ROLE_ID = int(ADMIN_ROLE_ID)
