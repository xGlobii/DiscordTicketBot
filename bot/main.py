import discord
import os
from dotenv import load_dotenv
import datetime
from discord.ext import commands
import random

from sql_lite_manager import SqLiteManager
from views import DiscordUi, CloseTicketBtn

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

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

    async def setup_hook(self):
        # Quick test
        await self.load_extension("bot_commands")
        MY_GUILD = discord.Object(id=1559125242272550962)
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
        #await self.tree.sync()
        self.add_view(DiscordUi())
        self.add_view(CloseTicketBtn())


    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.playing, name="Eating chicken nuggets at KFC 🍗")
        await self.change_presence(status=discord.Status.online, activity=activity)

        current_guild_ids = [(str(guild.id), ) for guild in self.guilds]
        self.db.synchronize_guild_list(current_guild_ids)

        print(f"Logged on a {self.user}")

    async def on_guild_join(self, guild):
        guild_id = str(guild.id)
        self.db.add_guild_to_list(guild_id)

    async def on_guild_remove(self, guild):
        guild_id = str(guild.id)
        self.db.remove_guild_from_list(guild_id)

    async def on_message(self, message):
        if message.author == self.user:
            return

        guild_prefix = self.guild_prefixes.get(message.guild.id)
        if guild_prefix is None:
            guild_prefix = '!'

        if message.content.startswith(guild_prefix):
            full_command = message.content.split(' ')
            command = full_command[0][len(guild_prefix):]
            custom_command = self.db.get_custom_command(message.guild.id, command)
            
            if custom_command is None:
                await message.channel.send("Command not found")
                return


            required_permission = custom_command["required_permission"]

            permissions = message.author.guild_permissions
            
            if required_permission == "none":
                pass
            elif required_permission != "none" and getattr(permissions, required_permission,  False):
                pass
            else:
                await message.reply("You do not have the necessary permissions to use this command")
                return

            c_type = custom_command["command_type"]

            if c_type == "text":
                await message.channel.send(custom_command["attributes"].replace("{user}", message.author.mention))
                return

            if c_type == "embed-text":

                description = custom_command["attributes"].replace("\\n", "\n").replace("{user}", message.author.mention)   

                embed = discord.Embed(
                    color=discord.Color.dark_blue(),
                    type="rich",
                    title=f"{command}",
                    description=description,
                    timestamp=datetime.datetime.now(datetime.timezone.utc))
                await message.channel.send(embed=embed)
                return

            if c_type == "dm-text":
                try:
                    await message.author.send(custom_command["attributes"])
                except:
                    await message.reply("You have disabled private messages")
                return

            if c_type == "counter":
                counter_value = self.db.get_and_increment_counter(message.guild.id, command)
                text = custom_command["attributes"]
                text = text.replace("{counter}", str(counter_value))
                await message.channel.send(text)
                return

            if c_type == "random":
                values = custom_command["attributes"].split('|')
                random_value = random.choice(values)
                await message.channel.send(random_value)
                return

        if message.content == self.user.mention:
            await message.reply(f"My prefix on this server is: {guild_prefix}")

    async def on_guild_join(self, guild:discord.Guild):
        welcome_channel = guild.system_channel
        if welcome_channel == None:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    welcome_channel = channel
                    break

        if welcome_channel is not None:
            description_msg = "``/ping`` - Ping pong\n"
            description_msg += "``/tickets`` - Get user tickets\n"
            description_msg += "``/invite`` - Get bot invite link\n"
            description_msg += "``/set_prefix`` - Configure server side command prefix\n"
            description_msg += "``/prepare`` - Prepares ticket channel\n"
            description_msg += "``/create_channel_and_role`` - Creates channel and locks it for new created role\n"
            description_msg += "``/add_access`` - Adds access to specified role for specified channel\n"
            description_msg += "``/remove_access`` - Removes access to specified role for specified channel\n"
            description_msg += "``/create_command`` - Add new server command\n"
            description_msg += "``/server_commands`` - Displays a list of all server commands"
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

client.run(token)