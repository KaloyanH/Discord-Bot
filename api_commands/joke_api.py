import requests


async def joke_api_response(channel):
    joke_url = "https://v2.jokeapi.dev/joke/Any"
    response = requests.get(joke_url)
    random_joke = response.json()
    await channel.send(f"{random_joke['setup']}\n{random_joke['delivery']}")

