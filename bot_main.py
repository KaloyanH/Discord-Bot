import os
import discord
from commands import *

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
discord.Intents.message_content = True
client = discord.Client(intents=intents)
authorized_channels = []  # List of the channels you want to authorize for this bot


@client.event
async def on_ready():
    print(f"{client.user.name} successfully connected to server!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel = message.channel
    cmd = message.content.lower()
    if channel.name in authorized_channels:
        if cmd == "!commands":
            await list_of_commands(channel, message)
        elif cmd in ["!hello", "!hi"]:
            await hello_command(channel, message)
        elif cmd in ["!bye", "!goodbye"]:
            await bye_command(channel, message)
        elif cmd.startswith("!weather"):  # Searches for temperature measurements for any city in the world
            try:
                location = " ".join(cmd.split(" ", 1)[1:])
                await get_weather_command(channel, message, location)
            except IndexError:
                await channel.send(f"{message.author.mention}, please provide the correct location!")
        elif cmd.startswith("!cat"):  # Displays a random cat image
            await get_a_cat_command(channel, message)
        elif cmd.startswith("!google"):  # Uses google search engine to search the web
            query = " ".join(cmd.split(" ", 1)[1:])
            await get_google_results(channel, message, query)


client.run(TOKEN)
