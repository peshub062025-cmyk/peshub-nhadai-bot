import discord

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from database.db import SessionLocal
from database.models import Match, Player, Season
from ui.search_result_view import SearchResultView


# =========================
# Chọn mùa
# =========================

class SeasonSelect(discord.ui.Select):

    def __init__(self, seasons):

        options = [
            discord.SelectOption(
                label="Tất cả các mùa",
                value="0"
            )
        ]

        for season in seasons:
            options.append(
                discord.SelectOption(
                    label=season.name,
                    value=str(season.id)
                )
            )

        super().__init__(
            placeholder="🏆 Mùa giải",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        value = int(self.values[0])

        if value == 0:
            self.view.season_id = None
        else:
            self.view.season_id = value

        await interaction.response.defer()


# =========================
# Người chơi 1
# =========================

class Player1Select(discord.ui.Select):

    def __init__(self, players):

        options = [
            discord.SelectOption(
                label="Tất cả người chơi",
                value="0"
            )
        ]

        for player in players:
            options.append(
                discord.SelectOption(
                    label=player.name,
                    value=str(player.id)
                )
            )

        super().__init__(
            placeholder="👤 Người chơi 1",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        value = int(self.values[0])

        if value == 0:
            self.view.player1_id = None
        else:
            self.view.player1_id = value

        await interaction.response.defer()


# =========================
# Người chơi 2
# =========================

class Player2Select(discord.ui.Select):

    def __init__(self, players):

        options = [
            discord.SelectOption(
                label="Không chọn",
                value="0"
            )
        ]

        for player in players:
            options.append(
                discord.SelectOption(
                    label=player.name,
                    value=str(player.id)
                )
            )

        super().__init__(
            placeholder="👤 Người chơi 2 (không bắt buộc)",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        value = int(self.values[0])

        if value == 0:
            self.view.player2_id = 0
        else:
            self.view.player2_id = value

        await interaction.response.defer()


# =========================
# Nút tìm kiếm
# =========================

class SearchButton(discord.ui.Button):

    def __init__(self):

        super().__init__(
            label="🔍 Tìm kiếm",
            style=discord.ButtonStyle.green
        )

    async def callback(self, interaction: discord.Interaction):

        if self.view.season_id is None and self.view.player1_id is None:

            await interaction.response.send_message(
                "⚠ Hãy chọn ít nhất Mùa giải hoặc Người chơi 1.",
                ephemeral=True
            )
            return

        db: Session = SessionLocal()

        try:

            player1 = None
            player2 = None

            query = db.query(Match)

            # Lọc theo mùa
            if self.view.season_id is not None:
                query = query.filter(
                    Match.season_id == self.view.season_id
                )

            # Lấy người chơi 1
            if self.view.player1_id is not None:
                player1 = db.query(Player).filter(
                    Player.id == self.view.player1_id
                ).first()

            # Lấy người chơi 2
            if self.view.player2_id != 0:
                player2 = db.query(Player).filter(
                    Player.id == self.view.player2_id
                ).first()

            # Chỉ chọn 1 người
            if player1 and self.view.player2_id == 0:

                query = query.filter(
                    or_(
                        Match.player1_id == player1.id,
                        Match.player2_id == player1.id
                    )
                )

            # Chọn đủ 2 người
            elif player1 and player2:

                query = query.filter(
                    or_(

                        and_(
                            Match.player1_id == player1.id,
                            Match.player2_id == player2.id
                        ),

                        and_(
                            Match.player1_id == player2.id,
                            Match.player2_id == player1.id
                        )

                    )
                )

            matches = query.order_by(
                Match.id.desc()
            ).all()
            if not matches:

                await interaction.response.send_message(
                    "❌ Không tìm thấy trận đấu.",
                    ephemeral=True
                )
                return

            # Hiển thị kết quả bằng View phân trang
            view = SearchResultView(matches)

            await interaction.response.send_message(
                embed=view.build_embed(),
                view=view
            )

        except Exception as e:

            await interaction.response.send_message(
                f"❌ {e}",
                ephemeral=True
            )

        finally:
            db.close()


# =========================
# Search View
# =========================

class SearchView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=300)

        self.season_id = None
        self.player1_id = None
        self.player2_id = 0

        db: Session = SessionLocal()

        try:

            seasons = db.query(Season).order_by(
                Season.id.desc()
            ).all()

            players = db.query(Player).order_by(
                Player.name
            ).all()

        finally:
            db.close()

        self.add_item(
            SeasonSelect(seasons)
        )

        self.add_item(
            Player1Select(players)
        )

        self.add_item(
            Player2Select(players)
        )

        self.add_item(
            SearchButton()
        )
