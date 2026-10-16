import discord
from discord import app_commands
import os
from dotenv import load_dotenv
import sqlite3
import datetime
from discord.utils import format_dt

load_dotenv()

class SqLiteManager():
    def __init__(self, db_path: str = "database.sqlite"):
        self.db_path = db_path
        self.initiate_tables()

    def save_config(self, guild_id: int, support_role_id: int, ticket_channel_id: int) -> None:
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute(
                """INSERT OR REPLACE INTO config (guild_id, support_role_id, ticket_channel_id) VALUES (?, ?, ?)"""
                , (guild_id, support_role_id, ticket_channel_id)
            )

    def save_ticket(self, ticket_id: int, guild_id: int, creator_id: int, title: str, description: str):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute(
                """ INSERT INTO tickets (ticket_id, guild_id, creator_id, title, description) VALUES (?, ?, ?, ?, ?)""",
                (ticket_id, guild_id, creator_id, title, description)
            )

    def close_ticket(self, ticket_id: int, closed_by_id: int):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""UPDATE tickets SET closed_by_id = ?, closed_at = CURRENT_TIMESTAMP WHERE ticket_id = ?""", (closed_by_id, ticket_id))

    def initiate_tables(self) -> None:
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS config (
                guild_id INTEGER PRIMARY KEY,
                support_role_id INTEGER,
                ticket_channel_id INTEGER
                )"""
            )

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS tickets(
                ticket_id INTEGER PRIMARY KEY,
                guild_id INTEGER,
                creator_id INTEGER,
                title TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                closed_by_id INTEGER NULL,
                closed_at TIMESTAMP NULL
                )
                """
            )

    def get_config(self, guild_id: int):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""SELECT support_role_id, ticket_channel_id FROM config WHERE guild_id = ?""", (guild_id,))
            return cursor.fetchone()

    def get_tickets(self, user_id: int, offset: int):
        with sqlite3.connect(self.db_path) as db:
            cursor = db.cursor()
            cursor.execute("""SELECT title, description, created_at, closed_by_id, closed_at FROM tickets WHERE creator_id = ? LIMIT 10 OFFSET ?""", (user_id, offset))
            return cursor.fetchall()


db = SqLiteManager()

class TicketModal(discord.ui.Modal, title="Create ticket"):
    def __init__(self, support_role_id: int):
        super().__init__()
        self.support_role_id = support_role_id

    topic = discord.ui.TextInput(
        label="Temat zgłoszenia",
        style=discord.TextStyle.short,
        placeholder="Opisz krótko swój problem",
        required=True
    )

    description = discord.ui.TextInput(
        label="Opis",
        style=discord.TextStyle.long,
        placeholder="Opisz szczegółowo swój problem",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        thread = await interaction.channel.create_thread(name=f"{interaction.user} - {self.topic.value} - Ticket", type=discord.ChannelType.private_thread)
        support_role: discord.Role = interaction.guild.get_role(self.support_role_id)

        embed = discord.Embed(
            color=discord.Color.green(),
            type="rich",
            title=f"{self.topic.value}",
            description=f"{self.description.value}",
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )

        close_btn = CloseTicketBtn()

        db.save_ticket(thread.id, interaction.guild.id, interaction.user.id, self.topic.value, self.description.value)
        await thread.send(f"||{interaction.user.mention} {support_role.mention}||",embed=embed, view=close_btn)
        await interaction.response.send_message("Twój ticket został utworzony!", ephemeral=True)

class CloseTicketBtn(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close ticket", custom_id="ticket_close", style=discord.ButtonStyle.danger)
    async def closeTicketBtn(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild_config = db.get_config(interaction.guild.id)

        if guild_config is None:
            await interaction.response.send_message(f"Wystąpił błąd z konfiguracją kanału dla tego serwera", ephemeral=True)
            return

        support_role_id, _ = guild_config

        if interaction.user.get_role(support_role_id) is not None:
            db.close_ticket(ticket_id=interaction.channel.id, closed_by_id=interaction.user.id)
            await interaction.response.defer()
            await interaction.channel.delete()
        else:
            await interaction.response.send_message(f"Tylko administrator może zamknąć ten ticket", ephemeral=True)

class DiscordUi(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create ticket", custom_id="ticket_create", style=discord.ButtonStyle.primary)
    async def createTicketBtn(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild_config = db.get_config(interaction.guild_id)

        if guild_config is None:
            await interaction.response.send_message(f"Wystąpił błąd z konfiguracją kanału dla tego serwera", ephemeral=True)
            return

        support_role_id, ticket_channel_id = guild_config

        if interaction.channel.id != ticket_channel_id:
            await interaction.response.send_message(f"Wystąpił błąd z konfiguracją kanału dla tego serwera", ephemeral=True)
            return

        form = TicketModal(support_role_id=support_role_id)
        await interaction.response.send_modal(form)

class PaginationView(discord.ui.View):
    def __init__(self, user: discord.User, current_page = 0):
        super().__init__()
        self.current_page = current_page
        self.user = user

    def generate_embed(self):

        ticket_description = f"Title | Description | Created At | Closed By | Closed At\n"

        tickets = db.get_tickets(user_id=self.user.id, offset=self.current_page * 10)

        for ticket in tickets:
            title, description, created_at, closed_by_id, closed_at = ticket

            dt_closed: datetime
            time_closed: str = ""
            closed_by:str = "Open"

            dt_created = datetime.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            dt_created = dt_created.replace(tzinfo=datetime.timezone.utc)
            time_created = format_dt(dt_created, style="F")
            if closed_at is not None:
                dt_closed = datetime.datetime.strptime(closed_at, "%Y-%m-%d %H:%M:%S")
                dt_closed = dt_closed.replace(tzinfo=datetime.timezone.utc)
                time_closed = format_dt(dt_closed, style="F")
                closed_by = f"<@{closed_by_id}>"

            ticket_description += f"{title} - {description} - {time_created} - {closed_by} - {time_closed}\n"

        embed = discord.Embed(
                    color=discord.Color.dark_blue(),
                    type="rich",
                    title=f"{self.user.global_name} tickets",
                    description=ticket_description,
                    timestamp=datetime.datetime.now(datetime.timezone.utc)
                )

        return embed

    @discord.ui.button(label=">", custom_id="next_page", style=discord.ButtonStyle.primary)
    async def nextPageBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Zostałem kliknięty", ephemeral=True)

class MyClient(discord.Client):

    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Szybkie testowanie
        MY_GUILD = discord.Object(id=1559125242272550962)
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
        self.add_view(DiscordUi())
        self.add_view(CloseTicketBtn())

        #await self.tree.sync()

    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.playing, name="Eating nuggets at KFC 🍗")
        await self.change_presence(status=discord.Status.online, activity=activity)
        print(f"Logged on a {self.user}")


    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('$hello'):
            await message.channel.send("Hello!")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

@app_commands.default_permissions(manage_channels=True)
@client.tree.command(name="prepare", description="Prepares ticket channel")
async def prepare(interaction: discord.Interaction, ticket_channel: discord.TextChannel, support_role: discord.Role):
    if interaction.guild is None:
        await interaction.response.send_message("This is guild command only")
        return

    db.save_config(interaction.guild_id, support_role_id=support_role.id, ticket_channel_id=ticket_channel.id)

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

@client.tree.command(name="ping", description="Testowa komenda")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@client.tree.command(name="tickets", description="Get user tickets")
async def tickets(interaction: discord.Interaction, user: discord.User):
    view = PaginationView(user)
    generated_embed = view.generate_embed()
    await interaction.user.send(embed=generated_embed, view=view)
    await interaction.response.send_message("Tickety użytkownika wysłane w wiadomości prywatnej", ephemeral=True)

token = os.getenv('DISCORD_TOKEN')
client.run(token)