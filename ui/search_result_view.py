import math
import discord

from sqlalchemy.orm import Session

from database.db import SessionLocal
from database.models import Player, Season


class SearchResultView(discord.ui.View):

    def __init__(self, matches):

        super().__init__(timeout=300)

        self.matches = matches
        self.page = 0
        self.page_size = 10

        self.previous_button = PreviousButton()
        self.next_button = NextButton()

        self.add_item(self.previous_button)
        self.add_item(self.next_button)

        self.update_buttons()

    def update_buttons(self):

        total_pages = max(
            math.ceil(len(self.matches) / self.page_size),
            1
        )

        self.previous_button.disabled = self.page == 0
        self.next_button.disabled = self.page >= total_pages - 1

    def build_embed(self):

        self.update_buttons()

        embed = discord.Embed(
            title="🎥 NHÀ ĐÀI PESHUB",
            color=discord.Color.blue()
        )

        total_matches = len(self.matches)
        total_pages = max(
            math.ceil(total_matches / self.page_size),
            1
        )

        start = self.page * self.page_size
        end = start + self.page_size

        page_matches = self.matches[start:end]

        db: Session = SessionLocal()

        try:

            description = ""

            for match in page_matches:

                season = db.query(Season).filter(
                    Season.id == match.season_id
                ).first()

                player1 = db.query(Player).filter(
                    Player.id == match.player1_id
                ).first()

                player2 = db.query(Player).filter(
                    Player.id == match.player2_id
                ).first()

                description += (
                    f"🏆 {season.name}\n"
                    f"🥇 {match.round}\n"
                    f"⚔ **{player1.name}** 🆚 **{player2.name}**\n"
                    f"🎥 {match.youtube_link}\n\n"
                )

            if description == "":
                description = "Không có dữ liệu."

            embed.description = description

            embed.set_footer(
                text=(
                    f"Trang {self.page + 1}/{total_pages} • "
                    f"{total_matches} trận đấu"
                )
            )

            return embed

        finally:
            db.close()


class PreviousButton(discord.ui.Button):

    def __init__(self):

        super().__init__(
            label="⬅ Trang trước",
            style=discord.ButtonStyle.secondary
        )

    async def callback(self, interaction: discord.Interaction):

        if self.view.page > 0:
            self.view.page -= 1

        self.view.update_buttons()

        await interaction.response.edit_message(
            embed=self.view.build_embed(),
            view=self.view
        )


class NextButton(discord.ui.Button):

    def __init__(self):

        super().__init__(
            label="➡ Trang sau",
            style=discord.ButtonStyle.primary
        )

    async def callback(self, interaction: discord.Interaction):

        total_pages = max(
            math.ceil(
                len(self.view.matches) /
                self.view.page_size
            ),
            1
        )

        if self.view.page < total_pages - 1:
            self.view.page += 1

        self.view.update_buttons()

        await interaction.response.edit_message(
            embed=self.view.build_embed(),
            view=self.view
        )
