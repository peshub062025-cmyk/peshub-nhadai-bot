import discord

from database.db import SessionLocal
from database.models import Season, Player

from ui.match_modal import MatchModal


class MatchView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=300)

        db = SessionLocal()

        try:
            seasons = db.query(Season).order_by(Season.id.desc()).all()
            players = db.query(Player).order_by(Player.name).all()

        finally:
            db.close()

        self.season = None
        self.round = None
        self.player1 = None
        self.player2 = None

        # ===== MÙA =====
        season_options = [
            discord.SelectOption(
                label=s.name,
                value=str(s.id)
            )
            for s in seasons
        ]

        self.add_item(
            SeasonSelect(
                season_options,
                self
            )
        )

        # ===== VÒNG =====
        self.add_item(
            RoundSelect(self)
        )

        # ===== NGƯỜI 1 =====
        player_options = [
            discord.SelectOption(
                label=p.name,
                value=str(p.id)
            )
            for p in players
        ]

        self.add_item(
            Player1Select(
                player_options,
                self
            )
        )

        # ===== NGƯỜI 2 =====
        self.add_item(
            Player2Select(
                player_options,
                self
            )
        )

        # ===== BUTTON =====
        self.add_item(
            ContinueButton()
        )


class SeasonSelect(discord.ui.Select):

    def __init__(self, options, parent):
        self.parent_view = parent

        super().__init__(
            placeholder="🏆 Chọn mùa",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        self.parent_view.season = int(self.values[0])

        await interaction.response.defer()


class RoundSelect(discord.ui.Select):

    def __init__(self, parent):

        self.parent_view = parent

        super().__init__(
            placeholder="🥇 Chọn vòng",
            options=[
                discord.SelectOption(label="Vòng bảng"),
                discord.SelectOption(label="Tứ kết"),
                discord.SelectOption(label="Bán kết"),
                discord.SelectOption(label="Chung kết"),
            ]
        )

    async def callback(self, interaction: discord.Interaction):

        self.parent_view.round = self.values[0]

        await interaction.response.defer()


class Player1Select(discord.ui.Select):

    def __init__(self, options, parent):

        self.parent_view = parent

        super().__init__(
            placeholder="👤 Người 1",
            options=options
        )

    async def callback(self, interaction):

        self.parent_view.player1 = int(self.values[0])

        await interaction.response.defer()


class Player2Select(discord.ui.Select):

    def __init__(self, options, parent):

        self.parent_view = parent

        super().__init__(
            placeholder="👤 Người 2",
            options=options
        )

    async def callback(self, interaction):

        self.parent_view.player2 = int(self.values[0])

        await interaction.response.defer()


class ContinueButton(discord.ui.Button):

    def __init__(self):

        super().__init__(
            label="➡ Tiếp tục",
            style=discord.ButtonStyle.green
        )

    async def callback(self, interaction: discord.Interaction):

        view = self.view

        if (
            view.season is None
            or view.round is None
            or view.player1 is None
            or view.player2 is None
        ):
            await interaction.response.send_message(
                "⚠ Vui lòng chọn đầy đủ thông tin.",
                ephemeral=True
            )
            return

        if view.player1 == view.player2:
            await interaction.response.send_message(
                "⚠ Người 1 và Người 2 phải khác nhau.",
                ephemeral=True
            )
            return

        await interaction.response.send_modal(
            MatchModal(
                season_id=view.season,
                round_name=view.round,
                player1_id=view.player1,
                player2_id=view.player2,
            )
        )
