from gtts import gTTS
from playsound import playsound
import os

def speak(text):
    """
    Convert text to speech using gTTS and play it.
    """
    tts = gTTS(text=text, lang='en')
    filename = "response.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)  # Clean up the temporary file
