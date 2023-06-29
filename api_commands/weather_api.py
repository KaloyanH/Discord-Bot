import math
import requests
import os

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
celsius_symbol = "\u2103"


# Uses the given location name to get the latitude and longitude
def get_location_coordinates(location):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={WEATHER_API_KEY}"
    geo_req = requests.get(geo_url)

    if geo_req.status_code == 200:
        geo_json = geo_req.json()
        if geo_json:
            latitude = geo_json[0].get("lat")
            longitude = geo_json[0].get("lon")
            return latitude, longitude
    return None, None


# Returns the actual temperature in celsius based on the latitude and longitude
def get_current_temperature(latitude, longitude):
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}" \
                  f"&lon={longitude}&appid={WEATHER_API_KEY}"
    weather_req = requests.get(weather_url)

    if weather_req.status_code == 200:
        weather_json = weather_req.json()
        temperature = weather_json["main"]["temp"]
        temperature_celsius = math.ceil(temperature - 273.15)
        return temperature_celsius
    return None


async def weather_api_response(channel, message, location):
    latitude, longitude = get_location_coordinates(location)

    if latitude and longitude:
        temperature = get_current_temperature(latitude, longitude)

        if temperature:
            await channel.send(
                f"{message.author.mention} The current temperature in {location.capitalize()}"
                f" is {temperature}{celsius_symbol}! "
            )
        else:
            await channel.send(
                f"{message.author.mention} Unable to fetch weather information for {location.capitalize()}."
            )
    else:
        await channel.send(
            f"{message.author.mention} Failed to fetch location information for {location.capitalize()}."
        )
