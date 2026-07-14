from ui.player_modal import PlayerModal
@app_commands.command(
    name="themnguoi",
    description="Thêm người chơi"
)
async def themnguoi(
    self,
    interaction: discord.Interaction
):

    if not await check_channel(interaction):
        return

    if not await check_admin(interaction):
        return

    await interaction.response.send_modal(
        PlayerModal()
    )
