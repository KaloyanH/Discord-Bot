import os
import discord
from commands import *

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
discord.Intents.message_content = True
client = discord.Client(intents=intents)
authorized_channels = []  # List of the channels you want to authorize for this bot


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
        elif cmd.startswith("!joke"):
            await get_random_joke(channel)
        elif cmd.startswith("!weather"):
            await handle_weather_command(channel, message, cmd)
        elif cmd.startswith("!cat"):
            await get_a_cat_command(channel, message)
        elif cmd.startswith("!google"):
            await handle_google_search(channel, message, cmd)



client.run(TOKEN)
