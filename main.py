import discord
from discord.ext import commands
from config import settings, bot_cogs

client = commands.Bot(command_prefix = settings["prefix"])
client.remove_command('help')

@client.event
async def on_ready():
	print('bot started')

for cog in bot_cogs:
	client.load_extension(cog)

client.run(settings['token'])