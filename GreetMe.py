import datetime
from gtts import gTTS
import os

def speak(audio):
    tts = gTTS(text=audio, lang="en")
    tts.save("temp.mp3")
    os.system("mpg321 temp.mp3")
    os.remove("temp.mp3")

def greetMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour <= 12:
        speak("Good Morning, sir")
    elif hour > 12 and hour < 18:
        speak("Good Afternoon, sir")
    else:
        speak("Good Evening, sir")
    
    speak("Please tell me, how can I help you?")
