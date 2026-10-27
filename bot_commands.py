import discord
from discord import app_commands
from discord.ext import commands
from views import PaginationView
import os

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Testowa komenda")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")

    @app_commands.command(name="tickets", description="Get user tickets")
    async def tickets(self, interaction: discord.Interaction, user: discord.User):
        view = PaginationView(user)
        generated_embed = view.generate_embed()
        await interaction.user.send(embed=generated_embed, view=view)
        await interaction.response.send_message("Tickety użytkownika wysłane w wiadomości prywatnej", ephemeral=True)

    @app_commands.command(name="invite", description="Get bot invite link")
    async def invite(self, interaction: discord.Interaction):
        await interaction.response.send_message(os.getenv('INVITE_URL'),ephemeral=True)

    @app_commands.command(name="set_prefix", description="Configure server side command prefix")
    async def setPrefix(self, interaction: discord.Interaction, prefix: str):
        new_nickname = f"Nugget [{prefix}]"
        try:
            await interaction.guild.me.edit(nick=new_nickname)
            await interaction.response.send_message(f"Server prefix is now: {prefix}")
        except:
            await interaction.response.send_message(f"Server prefix is now: {prefix}")

async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))