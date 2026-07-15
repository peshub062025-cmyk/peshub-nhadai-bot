import discord
from sqlalchemy.orm import Session

from database.db import SessionLocal
from database.models import Season


class SeasonModal(discord.ui.Modal, title="🏆 Thêm mùa giải"):

    ten = discord.ui.TextInput(
        label="Tên mùa",
        placeholder="Ví dụ: Mùa 8",
        required=True,
        max_length=100
    )

    async def on_submit(self, interaction: discord.Interaction):

        db: Session = SessionLocal()

        try:
            season_name = self.ten.value.strip().title()

            season = db.query(Season).filter(
                Season.name == season_name
            ).first()

            if season:
                await interaction.response.send_message(
                    "⚠ Mùa này đã tồn tại.",
                    ephemeral=True
                )
                return

            new_season = Season(
                name=season_name
            )

            db.add(new_season)
            db.commit()

            await interaction.response.send_message(
                f"✅ Đã thêm **{season_name}**",
                ephemeral=True
            )

        except Exception as e:
            import traceback
            traceback.print_exc()

            await interaction.response.send_message(
                f"❌ Lỗi: {e}",
                ephemeral=True
            )

        finally:
            db.close()
