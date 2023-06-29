import os
import requests

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ENGINE_ID = os.getenv("ENGINE_ID")


async def google_api_response(channel, message, query):
    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={ENGINE_ID}&q={query}"
    response = requests.get(url)
    res_json = response.json()
    items = res_json.get('items', [])[:5]  # Limited to 5 results to avoid spam in the channel

    if not query:
        await channel.send(f"{message.author.mention}, please enter a query!")
        return
    await channel.send(message.author.mention)
    for item in items:
        title = item.get('title', '')
        link = item.get('link', '')

        await channel.send(
            f"Title: {title}\nLink: {link}\n --- ")
