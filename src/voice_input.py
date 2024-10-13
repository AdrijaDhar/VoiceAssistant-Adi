import speech_recognition as sr
from src.voice_output import speak  # Ensure this is correct

def get_text_input():
    """Function to take user input as text."""
    return input("You: ")

def get_voice_input():
    """Function to take user input as voice and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for background noise
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # Set timeouts
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            speak("Sorry, I could not understand the audio.")
            return None

        except sr.RequestError:
            print("Network error.")
            speak("Network error.")
            return None

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            speak("There was an error capturing your input.")
            return None
