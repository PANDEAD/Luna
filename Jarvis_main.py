import threading
import time
import sounddevice as sd
import librosa
import numpy as np
from tensorflow.keras.models import load_model
from gtts import gTTS
import os
from Gpt import chatgpt_api
import datetime
import speedtest
from email import message
from reminder import set_reminder
from numpy import tile
import speech_recognition as sr
import requests
from bs4 import BeautifulSoup
import random
from plyer import notification
from pygame import mixer
import mediapipe as mp
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import pandas as pd
import time
import subprocess
from pync import Notifier
from alarm import set_alarm
import re
from googletrans import Translator
import youtube
import youtube2
import wikipedia
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from scipy.io.wavfile import write
import jokes
import weather
from Calculatenumbers import WolframAlphaQuery
import pygame

fs = 22050
seconds = 2
model = load_model("saved_model/WWD.h5")


def speak(audio):
   tts = gTTS(text=audio, lang='en')
   tts.save("audio.mp3")
   os.system("afplay audio.mp3")

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


def voice_assistant():
        while True:
                query = takeCommand().lower()

                if "go to sleep" in query:
                    speak("Ok sir , You can call me anytime")
                    break 
                
                elif "schedule my day" in query:
                    speak("Do you want to clear old tasks? (Please say YES or NO)")
                    while True:
                        query = takeCommand().lower()
                        if "yes" in query or "sure" in query or "clear" in query:
                            tasks = []  # Empty list
                            with open("tasks.txt", "w") as file:
                                file.write("")
                            break
                        elif "no" in query:
                            with open("tasks.txt", "r") as file:
                                tasks = file.readlines()
                            speak("Old tasks retained.")
                            break
                        else:
                            speak("Sorry, I didn't understand your response. Please say YES or NO.")

                    while True:
                        speak("Please tell the task, or say 'stop' to finish.")
                        task = takeCommand()
                        if "stop" in task:
                            break
                        tasks.append(task + "\n")

                    with open("tasks.txt", "w") as file:
                        file.writelines(tasks)

                    speak("Tasks added successfully.")

                elif "none" in query:
                    takeCommand().lower()

                elif 'alarm' in query:
                  speak("Sir, please tell the time to set the alarm, for example, 'set an alarm to 5:30 AM'.")
                  tt = takeCommand()
                  tt = tt.replace("set an alarm to", "").strip().replace(".", "").lower()
                  set_alarm(tt)
                
                elif "reminder" in query:
                    speak("Sure, please specify the time for the reminder.")
                    time_input = takeCommand()
                    time_input= time_input.strip().replace(".", "").lower()
                    set_reminder(time_input)
                    

                  
                elif "show my schedule" in query:
                    subprocess.Popen(["open", "tasks.txt"])
                    file = open("tasks.txt", "r")
                    content = file.read()
                    file.close()

                    tts = gTTS(text=content, lang="en")

                    tts.save("schedule.mp3")

                    mixer.init()
                    mixer.music.load("schedule.mp3")
                    mixer.music.play()

                    Notifier.notify(
                    title="My Schedule",
                    subtitle="Your schedule for the day",
                    message=content,
                    #appIcon="icon.png",  # Replace with your icon file path
                    timeout=15
                   )

                

                elif "focus mode" in query:
                    subprocess.Popen(["python3", "FocusMode.py"])

                elif "translate" in query:
                    translator = Translator()
                    def recognize_speech():
                        recognizer = sr.Recognizer()
                        with sr.Microphone() as source:
                            print("Listening...")
                            speak("listening")
                            recognizer.adjust_for_ambient_noise(source)
                            audio = recognizer.listen(source)

                        try:
                            text = recognizer.recognize_google(audio)
                            print("You said:", text)
                            return text
                        except sr.UnknownValueError:
                            print("Could not understand audio.")
                            return ""
                        except sr.RequestError as e:
                            print(f"Error with the request: {e}")
                            return ""

                    def translate_text(text, target_language):
                        translation = translator.translate(text, dest=target_language)
                        translated_text = translation.text
                        return translated_text

                    def say(text, lang= 'en'):
                        tts = gTTS(text, lang=lang)
                        tts.save('translated_audio.mp3')
                        os.system('afplay translated_audio.mp3')  # Play the audio using Mac's afplay command
                    
                    def detect_language(text):
                        try:
                            language = detect(text)
                            return language
                        except LangDetectException:
                            print("Could not detect the language.")
                        return 'en'


                    if __name__ == "__main__":
                        print("Welcome to the Language Translator Voice Assistant!")

                        while True:
                            user_input = recognize_speech()
                            if user_input.lower() == "exit":
                                print("Voice translator is exiting...")
                                say("voice translator is exiting")
                                break

                            translation_match = re.match(r"translate (.+) into (.+)", user_input, re.I)
                            if translation_match:
                                source_text, target_language = translation_match.groups()
                                print(f"Translating '{source_text}' into {target_language}...")
                                source_language = detect_language(source_text)
                                print(f"Detected source language: {source_language}")
                                translated_text = translate_text(source_text, target_language)
                                print("Translated text:", translated_text)
                                target_language_code = translator.detect(translated_text).lang
                                say("Translation: " + translated_text, lang=target_language_code)
                            else:
                                print("Please provide a valid translation query, e.g., 'translate hello into french'")

                
                       
                     
                elif "the time" in query or "current time" in query:
                    current_time = datetime.datetime.now().strftime("%H:%M")  
                    speak("The current time is " + current_time)

                elif "internet speed" in query or "Wi-Fi speed" in query:
                    st = speedtest.Speedtest()
                    download_speed = st.download() / 1_000_000  # Convert to Mbps
                    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
                    download_message = f"Download Speed: {download_speed:.2f} Mbps"
                    upload_message = f"Upload Speed: {upload_speed:.2f} Mbps"
                    print(download_message)
                    print(upload_message)
                    subprocess.call(["say", download_message])
                    subprocess.call(["say", upload_message])


                elif "screenshot" in query:
                     from PIL import ImageGrab
                     screenshot = ImageGrab.grab()
                     screenshot.save("screenshot.png")
                     screenshot.show()


                elif "click my photo" in query:
                        subprocess.Popen(["open", "-a", "Photo Booth"])
                        time.sleep(2)
                        speak("SMILE")

                
                

                ############################################################
                elif "hello" in query or "hey" in query:
                    speak("Hello sir, how are you ?")
                elif "not fine" in query:
                    speak("I am sorry to hear that. Is there anything I can do to help you?")
                elif "i am fine" in query or "good" in query:
                    speak("that's great, sir")
                elif "how are you" in query:
                    speak("Perfect, sir")
                elif "thank you" in query:
                    speak("you are welcome, sir")
                
                elif "tired" in query:
                    speak("Playing your favourites, sir")
                    a = (1,2,3)
                    b = random.choice(a)
                    if b==1:
                        youtube_url = "https://www.youtube.com/watch?v=kw4tT7SCmaY"
                        subprocess.Popen(["open", youtube_url])
                    elif b==2:
                       youtube_url = "https://www.youtube.com/watch?v=xrbY9gDVms0"
                       subprocess.Popen(["open", youtube_url])
                    elif b==3:
                       youtube_url = "https://www.youtube.com/watch?v=wQA68Oqr1qE" 
                       subprocess.Popen(["open", youtube_url])
                 


                elif "mute" in query:
                    subprocess.Popen(["amixer", "-D", "pulse", "sset", "Master", "mute"])
                    speak("Audio muted")

                elif "unmute" in query:
                    subprocess.Popen(["amixer", "-D", "pulse", "sset", "Master", "unmute"])
                    speak("Audio unmuted")
                
                elif "pause" in query:
                    pygame.mixer.music.pause()
                    speak("Audio paused")
                
               

                elif "volume up" in query:
                    subprocess.Popen(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"])
                    speak("Turning volume up, sir")

                elif "volume down" in query:
                        subprocess.Popen(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"])
                        speak("Turning volume down, sir")

                
                elif "google" in query:
                    from SearchNow import searchGoogle
                    query1= query.replace("search","").replace("on","").replace("for","")
                    query2 = query.replace("google","").replace("on","").replace("search","").replace("for","")
                    print(f"Searching for: {query}")
                    speak(f"Searching for: {query}")
                    searchGoogle(query1)
                    info = wikipedia.summary(query2, 2)
                    speak(info)

                elif "play" in query:
                    youtube2.pands(query)
                   
                elif "wikipedia" in query:
                    from SearchNow import searchWikipedia
                    searchWikipedia(query)
                
                elif 'youtube' in query and len(query.split()) > 1:
                    youtube.search_and_play(query)
                
                elif "news" in query:
                   from NewsRead import latestnews
                   latestnews()

                elif "calculate" in query:
                    while True:
                        speak("Tell me your question")
                        cal = takeCommand()
                        cal1 = WolframAlphaQuery(cal)
                        speak(cal1)
                        speak("Do you want to continue or stop?")
                        response = takeCommand().lower()
                        if "stop" in response:
                            speak("Okay, I will stop.")
                            break
                   

                elif "weather" in query:
                    speak("Tell me the location ")
                    loc = takeCommand()
                    wea = weather.get_weather(loc)
                    speak(wea)

                elif "joke" in query:
                    joke = jokes.get_joke()
                    speak(joke)
                
                elif "dad joke" in query:
                    joke1= jokes.fetch_dad_joke()
                    speak(joke1)
                             
                elif "sleep" in query:
                    speak("Going to sleep,sir")
                    exit()

                elif "send email" in query:
                    speak("sending email")
                    html = '''
                        <html>
                            <body>
                                <h1>Here is your Report</h1>
                                <p>Hello, welcome to your report!</p>
                                
                            </body>
                        </html>
                        '''
                    def attach_file_to_email(email_message, filename, extra_headers=None):
                        with open(filename, "rb") as f:
                            file_attachment = MIMEApplication(f.read())  
                        file_attachment.add_header(
                            "Content-Disposition",
                            f"attachment; filename= {filename}",
                        )
                        if extra_headers is not None:
                            for name, value in extra_headers.items():
                                file_attachment.add_header(name, value)
                        email_message.attach(file_attachment)
                    email_from = 'sulthana05shaik20@gmail.com'
                    password = 'iqoj uhhj owyx wvxp'
                    email_to = 'sulthana05shaik20@gmail.com'
                    date_str = pd.Timestamp.today().strftime('%Y-%M-%D')
                    email_message = MIMEMultipart()
                    email_message['From'] = email_from
                    email_message['To'] = email_to
                    email_message['Subject'] = f'Report email - {date_str}'
                    email_message.attach(MIMEText(html, "html"))
                    attach_file_to_email(email_message, "/Users/saniasulthanashaik/Downloads/ECE.key")
                    email_string = email_message.as_string()
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                        server.login(email_from, password)
                        server.sendmail(email_from, email_to, email_string) 

                elif "remember that" in query:
                    rememberMessage = query.replace("remember that", "").replace("jarvis", "").strip()
                    speak("You told me to remember that " + rememberMessage)
                    with open("Remember.txt", "a") as remember:
                        remember.write(rememberMessage + "\n")

                elif "what do you remember" in query:
                    remember = open("Remember.txt","r")
                    speak("You told me to remember that" + remember.read())

                elif "shutdown system" in query:
                    speak("Are You sure you want to shutdown")
                    shutdown = input("Do you wish to shutdown your computer? (yes/no)")
                    if shutdown == "yes":
                        os.system("shutdown /s /t 1")

                    elif shutdown == "no":
                        break
                else:
                    ans = chatgpt_api(query)
                    print(ans)
                    speak(ans)

          
                 




def activate_wake_word_detection():
    while True:
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
        sd.wait()
        mfcc = librosa.feature.mfcc(y=myrecording.ravel(), sr=fs, n_mfcc=40)
        mfcc_processed = np.mean(mfcc.T, axis=0)
        prediction_thread(mfcc_processed)
        time.sleep(0.001)

def prediction(y):
    prediction = model.predict(np.expand_dims(y, axis=0))
    if prediction[:, 1] > 0.96:
        speak("Hello, What can I do for you?")
        voice_assistant()

                
def prediction_thread(y):
    pred_thread = threading.Thread(target=prediction, name="PredictFunction", args=(y,))
    pred_thread.start()
    pred_thread.join()

def voice_thread():
    listen_thread = threading.Thread(target=activate_wake_word_detection, name="ListeningFunction")
    listen_thread.start()
    listen_thread.join()


voice_thread()
