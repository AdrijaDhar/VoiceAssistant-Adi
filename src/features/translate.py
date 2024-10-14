import requests
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import tempfile
from src.voice_output import speak

import requests
from src.voice_output import speak

def translate_text(text, target_lang="en"):
    """Translate text using LibreTranslate API."""
    try:
        # Check available languages dynamically
        response = requests.get("https://libretranslate.de/languages")
        supported_languages = {lang["name"].lower(): lang["code"] for lang in response.json()}

        if target_lang not in supported_languages.values():
            raise ValueError(f"Target language '{target_lang}' is not supported.")

        # Perform translation
        response = requests.post(
            "https://libretranslate.de/translate",
            data={
                "q": text,
                "source": "auto",
                "target": target_lang,
                "format": "text",
            },
        )

        translated_text = response.json().get("translatedText", "")
        if translated_text:
            print(f"Translated Text: {translated_text}")
            speak(translated_text)
        else:
            speak("Sorry, the translation failed.")
    except ValueError as ve:
        print(ve)
        speak(str(ve))
    except Exception as e:
        print(f"Error translating text: {e}")
        speak("Sorry, I couldn't translate the text.")

    """Translate text using LibreTranslate API."""
    try:
        response = requests.post(
            "https://libretranslate.de/translate",
            data={
                "q": text,
                "source": "auto",
                "target": target_lang,
                "format": "text",
            },
        )
        translated_text = response.json()["translatedText"]
        print(f"Translated Text: {translated_text}")

        # Speak the translated text
        speak_text(translated_text)
        return translated_text

    except Exception as e:
        print(f"Error translating text: {e}")
        speak("Sorry, I couldn't translate the text.")
        return None

def speak_text(text):
    """Convert text to speech and play the audio."""
    try:
        tts = gTTS(text=text, lang='en')
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_file:
            tts.save(temp_file.name)
            playsound(temp_file.name)
    except Exception as e:
        print(f"Error in text-to-speech: {e}")

