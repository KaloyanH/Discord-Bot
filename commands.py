from api_commands.google_api import google_api_response
from api_commands.weather_api import weather_api_response
from api_commands.cats_api import cats_api_response


async def list_of_commands(channel, message):
    await channel.send(f"{message.author.mention} Current commands are : !Hi, !Bye, !google (Enter query), !Weather ("
                       f"Enter city), !cat")


async def hello_command(channel, message):
    await channel.send(f"Hi, {message.author.mention}! Always nice to see you!")


async def bye_command(channel, message):
    await channel.send(f"Bye! See you soon {message.author.mention}!")


async def get_weather_command(channel, message, location):
    await weather_api_response(channel, message, location)


async def get_a_cat_command(channel, message):
    await cats_api_response(channel, message)


async def get_google_results(channel, message, query):
    await google_api_response(channel, message, query)
