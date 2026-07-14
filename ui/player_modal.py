import discord
from sqlalchemy.orm import Session

from database.db import SessionLocal
from database.models import Player


class PlayerModal(discord.ui.Modal, title="🎥 Thêm người chơi"):

    ten = discord.ui.TextInput(
        label="Tên người chơi",
        placeholder="Ví dụ: Trung Phan",
        required=True,
        max_length=100
    )

    async def on_submit(self, interaction: discord.Interaction):

    db: Session = SessionLocal()

    try:

        player = db.query(Player).filter(
            Player.name == self.ten.value.strip()
        ).first()

        if player:
            await interaction.response.send_message(
                "⚠ Người chơi đã tồn tại.",
                ephemeral=True
            )
            return

        new_player = Player(
            name=self.ten.value.strip()
        )

        db.add(new_player)
        db.commit()

        await interaction.response.send_message(
            f"✅ Đã thêm người chơi **{self.ten.value.strip()}**",
            ephemeral=True
        )

    except Exception as e:
        import traceback
        traceback.print_exc()

        if not interaction.response.is_done():
            await interaction.response.send_message(
                f"❌ {type(e).__name__}: {e}",
                ephemeral=True
            )

    finally:
        db.close()
