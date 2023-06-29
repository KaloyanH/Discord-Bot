import os
import requests

CATS_API_KEY = os.getenv("CATS_API_KEY")


async def cats_api_response(channel, message):
    cat_url = f"https://api.thecatapi.com/v1/images/search"
    headers = {
        "x-api-key": CATS_API_KEY
    }

    response = requests.get(cat_url, headers=headers)
    data = response.json()
    cat_img = data[0]["url"]

    await channel.send(
        f"{message.author.mention} {cat_img}"
    )
