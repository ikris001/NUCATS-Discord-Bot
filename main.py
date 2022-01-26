import discord
import os
from discord.ext import commands

discord_token = "*Removed so it can be uploaded on github*"


intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents = intents)




for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        client.load_extension(f"cogs.{name}")


client.run(discord_token)
