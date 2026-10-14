import discord
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()

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
            description=f"{self.description.value}"
        )

        close_btn = CloseTicketBtn()

        await thread.send(f"||{interaction.user.mention} {support_role.mention}||",embed=embed, view=close_btn)
        await interaction.response.send_message("Twój ticket został utworzony!", ephemeral=True)

class CloseTicketBtn(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close ticket", custom_id="ticket_close", style=discord.ButtonStyle.danger)
    async def closeTicketBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.channel.delete()

class DiscordUi(discord.ui.View):
    def __init__(self, support_role_id: int):
        super().__init__(timeout=None)
        self.support_role_id = support_role_id

    @discord.ui.button(label="Create ticket", custom_id="ticket_create", style=discord.ButtonStyle.primary)
    async def createTicketBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        form = TicketModal(support_role_id=self.support_role_id)
        await interaction.response.send_modal(form)

class MyClient(discord.Client):

    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Szybkie testowanie
        MY_GUILD = discord.Object(id=1559125242272550962)
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
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
async def prepare(interaction: discord.Interaction, support_role: discord.Role):
    if interaction.guild is None:
        await interaction.response.send_message("This is guild command only")
        return

    tickets_channel = discord.utils.get(interaction.guild.text_channels, name="tickets")
    support_role_id = support_role.id

    if tickets_channel is None:
        new_channel = await interaction.guild.create_text_channel("tickets")
        channel_id = new_channel.id
        await interaction.response.send_message(f"Created channel: {new_channel.mention}", ephemeral=True)

        embed = discord.Embed(
            color=discord.Color.red(),
            title="Create ticket",
            type="rich",
            description="Have an issue? Create ticket and let us know"
        )

        btn = DiscordUi(support_role_id=support_role_id)

        await new_channel.send(embed=embed, view=btn)
    else:
        channel_id = tickets_channel.id
        await interaction.response.send_message(f"Ticket channel exists: {tickets_channel.mention}", ephemeral=True)
    
    return


@client.tree.command(name="ping", description="Testowa komenda")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

token = os.getenv('DISCORD_TOKEN')
client.run(token)