import requests
from gtts import gTTS
import os

def get_joke():
    url = "https://v2.jokeapi.dev/joke/Programming?format=txt"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return "Sorry, I couldn't fetch a joke at the moment."
    
def fetch_dad_joke():
    api_url = "https://api.api-ninjas.com/v1/dadjokes?limit=1"
    response = requests.get(api_url)
    if response.status_code == 200:
        joke_data = response.json()
        joke = joke_data[0].get("joke", "No dad joke available.")
        return joke
    else:
        return "Sorry, I couldn't fetch a dad joke at the moment."


