import discord
import json


client = discord.Client()
with open('config.json', 'r') as file:
    config = json.load(file)
    file.close()


def analyse(message):
    command, arguments = message.split(" ", 1), None

    if len(command) == 2:
        command, arguments, command
        arguments = arguments.split(config["SEPARATOR"])

        for index, value in enumerate(arguments):
            try: arguments[index] = int(value)
            except: continue
            
    else: command = command[0]

    return command, arguments



@client.event
async def on_message(message):
    if message.author.bot or message.content[0] != config["PREFIX"]: return None






client.run(token)