import discord

from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from database.db import SessionLocal
from database.models import Match, Player, Season


class SeasonSelect(discord.ui.Select):

    def __init__(self, seasons):

        options = []

        for season in seasons:
            options.append(
                discord.SelectOption(
                    label=season.name,
                    value=str(season.id)
                )
            )

        super().__init__(
            placeholder="🏆 Chọn mùa giải",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        self.view.season_id = int(self.values[0])

        await interaction.response.defer()


class Player1Select(discord.ui.Select):

    def __init__(self, players):

        options = []

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

    async def callback(self, interaction):

        self.view.player1_id = int(self.values[0])

        await interaction.response.defer()


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

    async def callback(self, interaction):

        self.view.player2_id = int(self.values[0])

        await interaction.response.defer()

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

            season = db.query(Season).filter(
                Season.id == self.view.season_id
            ).first()

            player1 = db.query(Player).filter(
                Player.id == self.view.player1_id
            ).first()

            player2 = None

            if self.view.player2_id != 0:
                player2 = db.query(Player).filter(
                    Player.id == self.view.player2_id
                ).first()

          # ==========================
          # Truy vấn
          # ==========================

          # Chỉ chọn mùa
if self.view.season_id is not None and self.view.player1_id is None:

         matches = db.query(Match).filter(
        Match.season_id == self.view.season_id
    ).all()

         # Chỉ chọn Người 1
        elif self.view.season_id is None and self.view.player2_id == 0:

         matches = db.query(Match).filter(
        or_(
            Match.player1_id == self.view.player1_id,
            Match.player2_id == self.view.player1_id
        )
        ).all()

        # Mùa + Người 1
        elif self.view.season_id is not None and self.view.player2_id == 0:

        matches = db.query(Match).filter(
        Match.season_id == self.view.season_id,
        or_(
            Match.player1_id == self.view.player1_id,
            Match.player2_id == self.view.player1_id
        )
        ).all()

       # Hai người (có hoặc không có mùa)
       else:

      query = db.query(Match)

    if self.view.season_id is not None:
        query = query.filter(
            Match.season_id == self.view.season_id
        )

       matches = query.filter(
        or_(
            and_(
                Match.player1_id == self.view.player1_id,
                Match.player2_id == self.view.player2_id
            ),
            and_(
                Match.player1_id == self.view.player2_id,
                Match.player2_id == self.view.player1_id
            )
        )
        ).all()

            if not matches:

                await interaction.response.send_message(
                    "❌ Không tìm thấy trận đấu nào.",
                    ephemeral=True
                )
                return

            embed = discord.Embed(
                title="🎥 NHÀ ĐÀI PESHUB",
                color=discord.Color.blue()
            )

            embed.add_field(
                name="🏆 Mùa",
                value=season.name,
                inline=False
            )

            if player2:

                embed.add_field(
                    name="👥 Người chơi",
                    value=f"{player1.name} 🆚 {player2.name}",
                    inline=False
                )

            else:

                embed.add_field(
                    name="👤 Người chơi",
                    value=player1.name,
                    inline=False
                )

            text = ""

            for match in matches:

                p1 = db.query(Player).filter(
                    Player.id == match.player1_id
                ).first()

                p2 = db.query(Player).filter(
                    Player.id == match.player2_id
                ).first()

                text += (
                    f"🥇 {match.round}\n"
                    f"⚔ {p1.name} 🆚 {p2.name}\n"
                    f"🎥 {match.youtube_link}\n\n"
                )

            embed.description = text

            embed.set_footer(
                text=f"Tìm thấy {len(matches)} trận đấu"
            )

            await interaction.response.send_message(
                embed=embed
            )

        except Exception as e:

            await interaction.response.send_message(
                f"❌ {e}",
                ephemeral=True
            )

        finally:
            db.close()
class SearchView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=300)

        self.season_id = None
        self.player1_id = None
        self.player2_id = 0

        db: Session = SessionLocal()

        try:

            seasons = db.query(Season).order_by(
                Season.name
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
