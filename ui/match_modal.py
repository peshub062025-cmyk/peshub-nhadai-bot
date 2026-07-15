import discord
from sqlalchemy.orm import Session

from database.db import SessionLocal
from database.models import Match, Player, Season


class MatchModal(discord.ui.Modal, title="🎥 Thêm trận đấu"):

    youtube_link = discord.ui.TextInput(
        label="🔗 Link Youtube",
        placeholder="https://www.youtube.com/watch?v=...",
        required=True,
        max_length=500
    )

    def __init__(
        self,
        season_id: int,
        round_name: str,
        player1_id: int,
        player2_id: int
    ):

        super().__init__()

        self.season_id = season_id
        self.round_name = round_name
        self.player1_id = player1_id
        self.player2_id = player2_id

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        db: Session = SessionLocal()

        try:

            new_match = Match(
                season_id=self.season_id,
                round=self.round_name,
                player1_id=self.player1_id,
                player2_id=self.player2_id,
                youtube_link=self.youtube_link.value.strip()
            )

            db.add(new_match)
            db.commit()

            await interaction.response.send_message(
                "✅ Đã lưu trận đấu thành công!",
                ephemeral=True
            )

        except Exception as e:

            db.rollback()

            await interaction.response.send_message(
                f"❌ Có lỗi xảy ra:\n```{e}```",
                ephemeral=True
            )

        finally:

            db.close()
