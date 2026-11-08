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
        if interaction.guild is None:
            await interaction.response.send_message("This is guild command only")
            return
        
        view = PaginationView(self.bot, interaction.guild_id, user)
        generated_embed = view.generate_embed()
        await interaction.user.send(embed=generated_embed, view=view)
        await interaction.response.send_message("User tickets sent in a private message", ephemeral=True)

    @app_commands.command(name="invite", description="Get bot invite link")
    async def invite(self, interaction: discord.Interaction):
        await interaction.response.send_message(os.getenv('INVITE_URL'),ephemeral=True)

    @app_commands.default_permissions(administrator=True)
    @app_commands.command(name="set_prefix", description="Configure server side command prefix")
    async def setPrefix(self, interaction: discord.Interaction, prefix: str):
        if interaction.guild is None:
            await interaction.response.send_message("This is guild command only")
            return
        
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
    @app_commands.choices(
            channel_type=[
                app_commands.Choice(name="Text", value="text"),
                app_commands.Choice(name="Voice", value="voice"),
                app_commands.Choice(name="Both (text and voice)", value="both")
            ]
        )
    async def create_channel_and_role(self, interaction: discord.Interaction, channel_type: app_commands.Choice[str], channel_and_role_name: str):
        if interaction.guild is None:
            await interaction.response.send_message("This is guild command only")
            return

        new_role = await interaction.guild.create_role(name=channel_and_role_name,color=discord.Color.blue())
        new_category_channel = await interaction.guild.create_category_channel(name="Command create channel")

        overwrites={
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            new_role: discord.PermissionOverwrite(view_channel=True, connect=True, send_messages=True)
        }

        c_type = channel_type.value

        if c_type == "text":
            await interaction.guild.create_text_channel(name=channel_and_role_name, overwrites=overwrites, category=new_category_channel)
        elif c_type == "voice":
            await interaction.guild.create_voice_channel(name=channel_and_role_name, overwrites=overwrites, category=new_category_channel)
        elif c_type == "both":
            await interaction.guild.create_text_channel(name=channel_and_role_name, overwrites=overwrites, category=new_category_channel)
            await interaction.guild.create_voice_channel(name=channel_and_role_name, overwrites=overwrites, category=new_category_channel)
        
        await interaction.response.send_message("Channel and role created", ephemeral=True)

    @app_commands.default_permissions(manage_channels=True)
    @app_commands.command(name="add_access", description="Adds access to specified role for specified channel")
    async def add_access(self, interaction: discord.Interaction, channel: discord.abc.GuildChannel, role: discord.Role):
        if interaction.guild is None:
            await interaction.response.send_message("This is guild command only")
            return
        
        overwrites = discord.PermissionOverwrite(view_channel=True, send_messages=True, connect=True)
        await channel.set_permissions(role, overwrite=overwrites)
        await interaction.response.send_message("Done", ephemeral=True)

    @app_commands.default_permissions(manage_channels=True)
    @app_commands.command(name="remove_access", description="Removes access to specified role for specified channel")
    async def remove_access(self, interaction: discord.Interaction, channel: discord.abc.GuildChannel, role: discord.Role):
        if interaction.guild is None:
            await interaction.response.send_message("This is guild command only")
            return
        
        await channel.set_permissions(role, overwrite=None)
        await interaction.response.send_message("Done", ephemeral=True)

    @app_commands.default_permissions(administrator=True)
    @app_commands.command(name="create_command", description="Add new server command")
    @app_commands.choices(
        command_type=[
            app_commands.Choice(name="Text (message)", value="text"),
            app_commands.Choice(name="Embed (formated text)", value="embed-text"),
            app_commands.Choice(name="Direct message (DM)", value="dm-text"),
            app_commands.Choice(name="Counter", value="counter"),
            app_commands.Choice(name="Random", value="random")
        ],
        permission=[
            app_commands.Choice(name="All", value="none"),
            app_commands.Choice(name="Manage Messages", value="manage_messages"),
            app_commands.Choice(name="Administrator", value="administrator")
        ]
    )
    async def add_command(self, interaction: discord.Interaction, command_name: str, command_type: app_commands.Choice[str], permission: app_commands.Choice[str], attributes: str = None, description: str = None):
        if interaction.guild is None:
            await interaction.response.send_message("This is guild command only")
            return
        
        c_type = command_type.value
        c_permission = permission.value
        c_safe_name = command_name.replace(' ', '_').lower()

        try:
            if c_type == "counter":
                if attributes is None:
                    attributes = "{counter}"
                elif "{counter}" not in attributes:
                    await interaction.response.send_message("You're creating a counter, but you didn't specify a variable in the attributes." \
                    " Use the {counter} tag in your text" \
                    " For example, 'Number of banned users {counter}'",
                    ephemeral=True)
                    return

            if (c_type == "text" or c_type == "embed-text" or c_type == "dm-text" or "random") and attributes is None:
                await interaction.response.send_message("Command of type 'text', 'embed-text', 'dm-text' or 'random' must include specified content in 'attributes'", ephemeral=True)
                return

            self.bot.db.save_command(interaction.guild_id, c_safe_name, c_type, c_permission, attributes, description)
            await interaction.response.send_message(f"Command {c_safe_name} created")
        except sqlite3.IntegrityError:
            await interaction.response.send_message(f"A command named {c_safe_name} already exists on this server", ephemeral=True)

    @app_commands.command(name="server_commands", description="Displays a list of all server commands")
    async def server_commands(self, interaction: discord.Interaction):
        if interaction.guild is None:
            await interaction.response.send_message("This is guild command only")
            return

        commands = self.bot.db.get_guild_commands(interaction.guild_id)

        if not commands:
            await interaction.response.send_message("No commands have been created on this server")
            return

        prefix = self.bot.guild_prefixes[interaction.guild_id]

        desc = ""
        for cmd in commands:
            c_name = cmd["command_name"]
            c_desc = cmd["description"]
            if c_desc == "":
                c_desc = "`unspecified`"
            desc += f"{prefix}{c_name} - {c_desc}\n"

        await interaction.response.send_message(f"**Command list**:\n {desc}")

async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))