import discord
import datetime
from discord.utils import format_dt

from sql_lite_manager import SqLiteManager

db = SqLiteManager()

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