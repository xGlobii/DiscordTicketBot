import discord
import datetime
import math
import os
from discord.utils import format_dt

from sql_lite_manager import SqLiteManager

db = SqLiteManager()

class PaginationView(discord.ui.View):
    def __init__(self, bot, guild_id: int, user: discord.User, current_page = 0):
        super().__init__()
        self.current_page = current_page
        self.user = user
        self.guild_id = guild_id
        self.bot = bot
        self.tickets_per_page = int(os.getenv('RECORDS_PER_PAGE', '5'))
        self.all_tickets = self.bot.db.get_all_user_tickets(guild_id=self.guild_id, user_id=self.user.id)
        self.max_pages = math.ceil(self.all_tickets / self.tickets_per_page)
        if self.current_page == 0:
            self.children[0].disabled = True
        if self.current_page >= self.max_pages - 1:
            self.children[1].disabled = True

    def generate_embed(self):

        guild = self.bot.get_guild(self.guild_id)

        tickets = self.bot.db.get_tickets(guild_id=self.guild_id, user_id=self.user.id, offset=self.current_page * self.tickets_per_page)

        embed = discord.Embed(
                            color=discord.Color.dark_blue(),
                            type="rich",
                            title=f"{self.user.global_name} tickets",
                            timestamp=datetime.datetime.now(datetime.timezone.utc),
                        )

        for ticket in tickets:
            title, description, created_at, closed_by_id, closed_at = ticket

            dt_closed: datetime
            time_closed: str = ""
            closed_by:str = "Open"

            dt_created = datetime.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            dt_created = dt_created.replace(tzinfo=datetime.timezone.utc)
            time_created = format_dt(dt_created, style="d")
            if closed_at is not None:
                dt_closed = datetime.datetime.strptime(closed_at, "%Y-%m-%d %H:%M:%S")
                dt_closed = dt_closed.replace(tzinfo=datetime.timezone.utc)
                time_closed = format_dt(dt_closed, style="d")
                closed_by = f"<@{closed_by_id}>"

            ticket_description = (f"Description: {description}\n"
                                  f"Opened: {time_created}\n"
                                  f"Closed: {time_closed} by {closed_by}\n"
            )
            embed.add_field(
                name=f"{title}",
                value=ticket_description,
                inline=False
            )

        if guild:
            icon = guild.icon.url if guild.icon else None
            embed.set_author(name=f"Server {guild.name}", icon_url=icon)
        
        embed.set_footer(text=f"Page {self.current_page + 1} / {self.max_pages}")

        return embed

    @discord.ui.button(label="<", custom_id="previous_page", style=discord.ButtonStyle.primary)
    async def previousPageBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page -= 1
        if self.current_page == 0:
            self.children[0].disabled = True
        else:
            self.children[0].disabled = False

        self.children[1].disabled = False
        new_embed = self.generate_embed()
        await interaction.response.edit_message(embed=new_embed, view=self)

    @discord.ui.button(label=">", custom_id="next_page", style=discord.ButtonStyle.primary)
    async def nextPageBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page += 1
        if self.current_page == self.max_pages - 1:
            self.children[1].disabled = True
        else:
            self.children[1].disabled = False

        self.children[0].disabled = False
        new_embed = self.generate_embed()
        await interaction.response.edit_message(embed=new_embed, view=self)

class CloseTicketBtn(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close ticket", custom_id="ticket_close", style=discord.ButtonStyle.danger)
    async def closeTicketBtn(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild_config = db.get_config(interaction.guild.id)

        if guild_config is None:
            await interaction.response.send_message(f"An error occurred with the channel configuration for this server", ephemeral=True)
            return

        support_role_id, _ = guild_config

        if interaction.user.get_role(support_role_id) or interaction.user.guild_permissions.administrator is not None:
            db.close_ticket(ticket_id=interaction.channel.id, closed_by_id=interaction.user.id)
            await interaction.response.defer()
            await interaction.channel.delete()
        else:
            await interaction.response.send_message(f"Only an administrator can close this ticket", ephemeral=True)

class DiscordUi(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create ticket", custom_id="ticket_create", style=discord.ButtonStyle.primary)
    async def createTicketBtn(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild_config = db.get_config(interaction.guild_id)

        if guild_config is None:
            await interaction.response.send_message(f"An error occurred with the channel configuration for this server", ephemeral=True)
            return

        support_role_id, ticket_channel_id = guild_config

        if interaction.channel.id != ticket_channel_id:
            await interaction.response.send_message(f"An error occurred with the channel configuration for this server", ephemeral=True)
            return

        form = TicketModal(support_role_id=support_role_id)
        await interaction.response.send_modal(form)

class TicketModal(discord.ui.Modal, title="Create ticket"):
    def __init__(self, support_role_id: int):
        super().__init__()
        self.support_role_id = support_role_id

    topic = discord.ui.TextInput(
        label="Subject of the report",
        style=discord.TextStyle.short,
        placeholder="Briefly describe your problem",
        required=True
    )

    description = discord.ui.TextInput(
        label="Description",
        style=discord.TextStyle.long,
        placeholder="Describe your problem in full detail",
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
        await interaction.response.send_message("Your ticket has been created!", ephemeral=True)