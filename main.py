import discord
import os
from dotenv import load_dotenv
import datetime
from discord.ext import commands

from sql_lite_manager import SqLiteManager
from views import DiscordUi, CloseTicketBtn

load_dotenv()

#db = SqLiteManager()

def get_dynamic_prefix(bot, message):
    if not message.guild:
        return '!'

    return bot.guild_prefixes.get(message.guild.id, '!')

class MyClient(commands.Bot):

    def __init__(self, *, intents: discord.Intents):
        self.db = SqLiteManager()
        self.guild_prefixes = self.db.get_prefixes()
        self.db.initiate_tables()
        super().__init__(command_prefix=get_dynamic_prefix, intents=intents)
        # self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Szybkie testowanie
        await self.load_extension("bot_commands")
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
        if message.content == self.user.mention:
            await message.reply(f"Mój prefix na tym serwerze to {self.guild_prefixes.get(message.guild.id)}")

    async def on_guild_join(self, guild:discord.Guild):
        welcome_channel = guild.system_channel
        if welcome_channel == None:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    welcome_channel = channel
                    break

        if welcome_channel is not None:
            description_msg = "``/prepare`` - prepares channel to be ticket channel\n"
            description_msg += "``/tickets`` - displays all user tickets\n"
            embed = discord.Embed(
                color=discord.Color.blurple(),
                title="Welcome",
                description=description_msg,
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            await welcome_channel.send(embed=embed)
        else:
            try:
                if guild.owner is not None:
                    await guild.owner.send("You added me to the server, " \
                    "but I can't send messages. Please check my permissions to ensure I work properly")
            except:
                pass

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

token = os.getenv('DISCORD_TOKEN')
client.run(token)