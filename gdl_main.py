import json
import discord
from discord.ext import commands

from lib.gdl_general_cmnd import GeneralCommands
from lib.gdl_stuff_cmnd import StuffCommands
from lib.gdl_lib import load_save


with open("config.json", "r") as file:
    config = json.load(file)

with open("lib/documentation.json", "r") as file:
    doc = json.load(file)


bot = commands.Bot(command_prefix=config["PREFIX"])

save = load_save()

for command_class in (GeneralCommands, StuffCommands):
    bot.add_cog(command_class(bot, (config["PREFIX"], config["SEPARATOR"], config["ADMIN"]), save, doc))


@bot.event
async def on_ready():
    print("Connecté")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{config['PREFIX']}aide"))


bot.run(config["TOKEN"])