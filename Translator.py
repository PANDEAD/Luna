import os
import re
import speech_recognition as sr
from gtts import gTTS
from googletrans import Translator

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

def speak(text, lang='en' ):
    tts = gTTS(text, lang=lang)
    tts.save('translated_audio.mp3')
    os.system('afplay translated_audio.mp3')  # Play the audio using Mac's afplay command

if __name__ == "__main__":
    print("Welcome to the Language Translator Voice Assistant!")

    while True:
        user_input = recognize_speech()
        if user_input.lower() == "exit":
            print("Voice translator is exiting...")
            speak("voice translator is exiting")
            break

        # Use regular expressions to extract the source text and target language
        translation_match = re.match(r"translate (.+) into (.+)", user_input, re.I)
        if translation_match:
            source_text, target_language = translation_match.groups()
            print(f"Translating '{source_text}' into {target_language}...")

            translated_text = translate_text(source_text, target_language)
            print("Translated text:", translated_text)
            target_language_code = translator.detect(translated_text).lang
            speak("Translation: " + translated_text, lang=target_language_code)
        else:
            print("Please provide a valid translation query, e.g., 'translate hello into french'")