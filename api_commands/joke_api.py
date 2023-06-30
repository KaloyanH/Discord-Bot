import requests


async def joke_api_response(channel):
    joke_url = "https://v2.jokeapi.dev/joke/Any"
    response = requests.get(joke_url)
    random_joke = response.json()
    message = f"{random_joke['setup']}\n{random_joke['delivery']}" if 'setup' in random_joke else random_joke[
        'joke']
    await channel.send(message)

