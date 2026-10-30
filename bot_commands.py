import discord
from discord import app_commands
from discord.ext import commands
from views import PaginationView, DiscordUi
import os
import sqlite3

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Ping pong")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")

    @app_commands.default_permissions(administrator=True)
    @app_commands.command(name="tickets", description="Get user tickets")
    async def tickets(self, interaction: discord.Interaction, user: discord.User):
        view = PaginationView(user)
        generated_embed = view.generate_embed()
        await interaction.user.send(embed=generated_embed, view=view)
        await interaction.response.send_message("Tickety użytkownika wysłane w wiadomości prywatnej", ephemeral=True)

    @app_commands.command(name="invite", description="Get bot invite link")
    async def invite(self, interaction: discord.Interaction):
        await interaction.response.send_message(os.getenv('INVITE_URL'),ephemeral=True)

    @app_commands.default_permissions(administrator=True)
    @app_commands.command(name="set_prefix", description="Configure server side command prefix")
    async def setPrefix(self, interaction: discord.Interaction, prefix: str):
        new_nickname = f"Nugget [{prefix}]"
        try:
            await interaction.guild.me.edit(nick=new_nickname)
            await interaction.response.send_message(f"Server prefix is now: {prefix}")
        except:
            await interaction.response.send_message(f"Server prefix is now: {prefix}")

        self.bot.db.update_command_prefix(interaction.guild_id, prefix)
        self.bot.guild_prefixes[interaction.guild_id] = prefix

    @app_commands.default_permissions(manage_channels=True)
    @app_commands.command(name="prepare", description="Prepares ticket channel")
    async def prepare(self, interaction: discord.Interaction, ticket_channel: discord.TextChannel, support_role: discord.Role):
        if interaction.guild is None:
            await interaction.response.send_message("This is guild command only")
            return

        self.bot.db.save_config(interaction.guild_id, support_role_id=support_role.id, ticket_channel_id=ticket_channel.id)

        embed = discord.Embed(
                color=discord.Color.red(),
                title="Create ticket",
                type="rich",
                description="Have an issue? Create ticket and let us know"
            )
        
        btn = DiscordUi()

        await ticket_channel.send(embed=embed, view=btn)
        await interaction.response.send_message(f"Ticket channel created", ephemeral=True)

        return

    @app_commands.default_permissions(manage_channels=True, manage_roles=True)
    @app_commands.command(name="create_channel_and_role", description="Creates channel and locks it for new created role")
    async def create_channel_and_role(self, interaction: discord.Interaction, channel_and_role_name: str):
        new_role = await interaction.guild.create_role(name=channel_and_role_name,color=discord.Color.blue())
        new_category_channel = await interaction.guild.create_category_channel(name="Command create channel")

        overwrites={
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            new_role: discord.PermissionOverwrite(view_channel=True)
        }
        new_channel = await interaction.guild.create_text_channel(name=channel_and_role_name, overwrites=overwrites,category=new_category_channel)
        await interaction.response.send_message("Channel and role created", ephemeral=True)

    @app_commands.default_permissions(administrator=True)
    @app_commands.command(name="create_command", description="Dodaje komendę serwerową")
    @app_commands.choices(
        command_type=[
            app_commands.Choice(name="Tekst (wiadomość)", value="text"),
            app_commands.Choice(name="Embed (sformatowany tekst)", value="embed-text"),
            app_commands.Choice(name="Prywatna wiadomość (DM)", value="dm-text"),
            app_commands.Choice(name="Counter (Licznik)", value="counter"),
            app_commands.Choice(name="Random (Losowa wartość)", value="random")
        ],
        permission=[
            app_commands.Choice(name="Wszyscy", value="none"),
            app_commands.Choice(name="Zarządzanie wiadomościami", value="manage_messages"),
            app_commands.Choice(name="Administrator", value="administrator")
        ]
    )
    async def add_command(self, interaction: discord.Interaction, command_name: str, command_type: app_commands.Choice[str], permission: app_commands.Choice[str], attributes: str = None):
        c_type = command_type.value
        c_permission = permission.value
        c_safe_name = command_name.replace(' ', '_').lower()

        try:
            if c_type == "counter":
                if attributes is None:
                    attributes = "{counter}"
                elif "{counter}" not in attributes:
                    await interaction.response.send_message("Tworzysz licznik, ale nie podałeś zmiennej w atrybutach." \
                    " Użyj tagu {counter} w swoim tekście" \
                    " Np. 'Ilość zbanowanych osób {counter}'",
                    ephemeral=True)
                    return

            if (c_type == "text" or c_type == "embed-text" or c_type == "dm-text" or "random") and attributes is None:
                await interaction.response.send_message("Komenda typu 'text', 'embed-text', 'dm-text' lub 'random' musi mieć podaną treść w 'attributes'", ephemeral=True)
                return

            self.bot.db.save_command(interaction.guild_id, c_safe_name, c_type, c_permission, attributes)
            await interaction.response.send_message(f"Utworzono komendę {c_safe_name} o typie {c_type} z uprawnieniami {c_permission}")
        except sqlite3.IntegrityError:
            await interaction.response.send_message(f"Komenda o nazwie {c_safe_name} już istnieje na tym serwerze", ephemeral=True)

    @app_commands.command(name="server_commands", description="Wyświetla listę wszystkich komend serwerowych")
    async def server_commands(self, interaction: discord.Interaction):
        commands = self.bot.db.get_guild_commands(interaction.guild_id)

        if not commands:
            await interaction.response.send_message("Ten serwer nie ma utworzonych żadnych komend")
            return

        opis = ""
        for cmd in commands:
            c_name = cmd["command_name"]
            c_type = cmd["command_type"]
            opis += f"{c_name} - {c_type} \n"

        await interaction.response.send_message(f"**Lista komend**:\n {opis}")

async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))