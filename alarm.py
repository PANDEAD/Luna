import datetime
import os
import time
import threading
from gtts import gTTS

def speak(audio):
   tts = gTTS(text=audio, lang='en')
   tts.save("audio.mp3")
   os.system("afplay audio.mp3")


def play_alarm_sound():
    sound_file = "temp2.mp3"
    os.system(f"afplay {sound_file}")

def set_alarm_callback():
    alarm_thread = threading.Thread(target=play_alarm_sound)
    alarm_thread.start()

def set_alarm(Timing):
    try:
        altime = datetime.datetime.strptime(Timing, "%I:%M %p").time()
        print(f"Done, alarm is set for {Timing}")
        speak("Done, alarm is set")

        current_datetime = datetime.datetime.now()
        alarm_datetime = datetime.datetime.combine(current_datetime.date(), altime)

        if alarm_datetime <= current_datetime:
            alarm_datetime += datetime.timedelta(days=1)  # If the alarm time is in the past, set it for the next day

        time_diff = (alarm_datetime - current_datetime).total_seconds()
        alarm_timer = threading.Timer(time_diff, set_alarm_callback)
        alarm_timer.start()
    except ValueError:
        print("Invalid time format. Please specify the alarm time in HH:MM AM/PM format.")
    return
