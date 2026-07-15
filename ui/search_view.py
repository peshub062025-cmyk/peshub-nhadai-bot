import discord

from sqlalchemy.orm import Session

from database.db import SessionLocal
from database.models import Season, Player


class SearchView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=300)

        db: Session = SessionLocal()

        try:

            # ===== Mùa giải =====
            season_options = []

            seasons = db.query(Season).order_by(Season.name).all()

            for season in seasons:
                season_options.append(
                    discord.SelectOption(
                        label=season.name,
                        value=str(season.id)
                    )
                )

            if not season_options:
                season_options.append(
                    discord.SelectOption(
                        label="Chưa có mùa giải",
                        value="0"
                    )
                )

            # ===== Người chơi =====
            player_options = [
                discord.SelectOption(
                    label="Không chọn",
                    value="0"
                )
            ]

            players = db.query(Player).order_by(Player.name).all()

            for player in players:
                player_options.append(
                    discord.SelectOption(
                        label=player.name,
                        value=str(player.id)
                    )
                )

        finally:
            db.close()

        # =========================
        # Mùa giải
        # =========================

        self.add_item(
            discord.ui.Select(
                placeholder="🏆 Chọn mùa giải",
                custom_id="season",
                options=season_options
            )
        )

        # =========================
        # Người chơi 1
        # =========================

        self.add_item(
            discord.ui.Select(
                placeholder="👤 Chọn Người chơi 1",
                custom_id="player1",
                options=player_options[1:]
            )
        )

        # =========================
        # Người chơi 2
        # =========================

        self.add_item(
            discord.ui.Select(
                placeholder="👤 Chọn Người chơi 2 (không bắt buộc)",
                custom_id="player2",
                options=player_options
            )
        )

        # =========================
        # Nút tìm kiếm
        # =========================

        self.add_item(
            discord.ui.Button(
                label="🔍 Tìm kiếm",
                style=discord.ButtonStyle.green,
                custom_id="search"
            )
        )
