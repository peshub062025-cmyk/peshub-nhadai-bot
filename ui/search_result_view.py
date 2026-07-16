import discord


class SearchResultView(discord.ui.View):

    def __init__(self, matches):

        super().__init__(timeout=300)

        self.matches = matches

        self.page = 0

        self.page_size = 10
