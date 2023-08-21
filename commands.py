from api_commands.cats_api import cats_api_response
from api_commands.google_api import google_api_response
from api_commands.joke_api import joke_api_response
from api_commands.weather_api import weather_api_response
from scraper.basic_scraper import extract_products_from_site, visualize_table


async def list_of_commands(channel, message):
    await channel.send(f"{message.author.mention} Current commands are : !Hi, !Bye, !Joke, "
                       f"!google (Enter query), !Weather (Enter city), !cat, !find (Enter product)")


async def hello_command(channel, message):
    await channel.send(f"Hi, {message.author.mention}! Always nice to see you!")


async def bye_command(channel, message):
    await channel.send(f"Bye! See you soon {message.author.mention}!")


async def get_random_joke(channel):
    await joke_api_response(channel)


async def get_a_cat_command(channel, message):
    await cats_api_response(channel, message)


async def handle_weather_command(channel, message, cmd):
    try:
        location = cmd.split(" ", 1)[1]
        await weather_api_response(channel, message, location)
    except IndexError:
        await channel.send(f"{message.author.mention}, please provide the correct location!")


async def handle_google_search(channel, message, cmd):
    query = cmd.split(" ", 1)[1]
    await google_api_response(channel, message, query)
    
async def find_product_command(channel, cmd):
    search_term = cmd.replace('!find', '', 1).strip()
    df = extract_products_from_site(search_term)
    await visualize_table(channel, df)
