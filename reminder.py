import threading
import datetime
import os
from gtts import gTTS
import speech_recognition as sr

def speak(audio):
   tts = gTTS(text=audio, lang='en')
   tts.save("audio1.mp3")
   os.system("afplay audio1.mp3")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, timeout=5)  

    try:
        print("Understanding..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except sr.UnknownValueError:
        speak("Say that again")
        print("Say that again")
        return "None"
    except sr.RequestError:
        speak("Sorry, I am having trouble connecting to the internet")
        print("Sorry, I am having trouble connecting to the internet")
        return "None"
    return query

def play_reminder_sound(topic):
    speak(f"Reminder: {topic}")

def set_reminder_callback(remind_time, topic):
    reminder_thread = threading.Thread(target=play_reminder_sound, args=(topic,))
    reminder_thread.start()

def set_reminder(Timing):
    try:
        remind_time = datetime.datetime.strptime(Timing, "%I:%M %p").time()
        print(f"Reminder time set for {Timing}")
        speak("Reminder time set. Now, please specify the topic of the reminder.")
        topic_input = takeCommand().lower()

        current_datetime = datetime.datetime.now()
        reminder_datetime = datetime.datetime.combine(current_datetime.date(), remind_time)

        if reminder_datetime <= current_datetime:
            reminder_datetime += datetime.timedelta(days=1)  # If the reminder time is in the past, set it for the next day

        time_diff = (reminder_datetime - current_datetime).total_seconds()
        reminder_timer = threading.Timer(time_diff, set_reminder_callback, args=(topic_input, topic_input))
        reminder_timer.start()

        speak("Reminder set successfully.")

    except ValueError:
        print("Invalid time format. Please specify the reminder time in HH:MM AM/PM format.")
        speak("Invalid time format. Call me again!")

