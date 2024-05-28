import time
import datetime
import sys
import os
import speech_recognition as sr
from gtts import gTTS
import subprocess

def is_admin():
    return os.geteuid() == 0

def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a voice command...")
        r.adjust_for_ambient_noise(source)  # Adjust for noise
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print(f"Voice command received: {command}")
        return command
    except sr.UnknownValueError:
        print("Google Web Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech Recognition service; {e}")
    return None

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save('voice.mp3')
    subprocess.call(['afplay', 'voice.mp3'])

if is_admin():
    # Use gTTS for speech output.
    speak("Please say 'start focus mode' to activate focus mode.")
    
    # Wait for a voice command to start focus mode.
    while True:
        command = get_voice_input()
        if command == "start focus mode":
            break

    # Get the focus time through a voice command.
    speak("Please specify the duration for the focus mode in minutes, for example, '30 minutes'.")
    
    while True:
        duration_input = get_voice_input()
        if duration_input and "minutes" in duration_input:
            try:
                focus_duration = int(''.join(filter(str.isdigit, duration_input)))
                break
            except ValueError:
                speak("I'm sorry, I couldn't understand the duration. Please try again.")

    host_path = '/etc/hosts'
    redirect = '127.0.0.1'

    current_time = datetime.datetime.now().strftime("%H:%M")
    print(f"Current time: {current_time}")
    time.sleep(2)

    website_list = ["www.facebook.com", "www.instagram.com", "www.pinterest.com", "www.reddit.com", "www.netflix.com", "www.hulu.com", "www.primevideo.in", "www.tumblr.com","www.twitter.com","www.hotstar.com"]

    stop_time = (datetime.datetime.now() + datetime.timedelta(minutes=focus_duration)).strftime("%H:%M")
    print(f"Focus mode will end at: {stop_time}")

    if current_time < stop_time:
        with open(host_path, "r+") as file:
            content = file.read()
            time.sleep(2)
            for website in website_list:
                if website in content:
                    pass
                else:
                    file.write(f"{redirect} {website}\n")
                    print("DONE")
                    time.sleep(1)
            print("FOCUS MODE TURNED ON !!!!")

    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time >= stop_time:
            with open(host_path, "r+") as file:
                content = file.readlines()
                file.seek(0)
                for line in content:
                    if not any(website in line for website in website_list):
                        file.write(line)
                file.truncate()

                print("Websites are unblocked !!")

                with open("focus.txt", "a") as focus_file:
                    focus_file.write(f",{focus_duration}")  # Write the focus duration in focus.txt
                break

else:
    os.system(f'sudo {sys.executable} ' + ' '.join(sys.argv))
