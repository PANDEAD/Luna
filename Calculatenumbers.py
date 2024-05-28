import speech_recognition as sr
import wolframalpha
import ssl
import urllib.request
from gtts import gTTS
import os

ssl._create_default_https_context = ssl._create_unverified_context
urllib.request.urlopen("https://www.wolframalpha.com")

# Replace with your Wolfram Alpha API key
api_key = "PJQLGV-V2JQX3YKVL"

def WolframAlphaQuery(query):
    client = wolframalpha.Client(api_key)
    res = client.query(query)
    try:
        answer = next(res.results).text
        return answer
    except StopIteration:
        return "I'm sorry, I couldn't find an answer to your question."

