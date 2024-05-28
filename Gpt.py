import openai
import os
from gtts import gTTS

api_key = "sk-proj-9LLi8g3mNCnoBKQ2EF5mT3BlbkFJTyf0wXhEQqK9URb71Xty"

def speak(audio):
   tts = gTTS(text=audio, lang='en')
   tts.save("audio1.mp3")
   os.system("afplay audio1.mp3")

def chatgpt_api(query):
    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages = [{"role":"user","content": query}],
            max_tokens= 100,
            temperature = 0.4
        )

        return response.choices[0].messages.content.strip()  # Extract the generated response
    except Exception as e:
        print(f"Error in ChatGPT API call: {str(e)}")
        speak("I'm sorry, but I couldn't provide a response at the moment.")
