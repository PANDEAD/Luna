from googleapiclient.discovery import build
import webbrowser
from gtts import gTTS
import os

api_key = 'AIzaSyCmb5kp59bGnZoYZElg6-q82z6U0XtGRMs'
youtube = build('youtube', 'v3', developerKey="AIzaSyCmb5kp59bGnZoYZElg6-q82z6U0XtGRMs")
def say(audio):
    tts = gTTS(text=audio, lang="en")
    tts.save("temp.mp3")
    os.system("afplay temp.mp3")  # For macOS
    os.remove("temp.mp3")



def pands(query):
    try:
        search_response = youtube.search().list(
            q=query,
            type='video',
            part='id',
            maxResults=1
        ).execute()

        if 'items' in search_response:
            video_id = search_response['items'][0]['id']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            webbrowser.open(video_url)
        else:
            print("No video found for the query.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        say("an error occured")
        


