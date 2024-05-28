from gtts import gTTS
import speech_recognition as sr
import requests
import os

def speak(text):
    tts = gTTS(text, lang='en')
    tts.save("output.mp3")
    os.system("afplay output.mp3") 

def get_weather(location):
    api_key = "d80316a6767b991337879768f8d282fe"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    complete_url = f"{base_url}?q={location}&appid={api_key}"
    
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] == 200:
        main_data = data["main"]
        temperature = main_data["temp"]
        temperature = round(temperature - 273.15, 2)  # Convert from Kelvin to Celsius
        weather_data = data["weather"]
        weather_description = weather_data[0]["description"]

        return f"The current temperature in {location} is {temperature} degrees Celsius, and the weather is {weather_description}."
    else:
        return "Sorry, I couldn't find weather information for that location."

