import speech_recognition as sr

def get_text_input():
    """
    Function to take user input as text.
    """
    return input("You: ")

def get_voice_input():
    """
    Function to take user input as voice and convert it to text.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        # Recognize the voice input using Google Web Speech API
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        print("Could not request results. Check your internet connection.")
        return None
