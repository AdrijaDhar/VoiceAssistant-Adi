import pyttsx3



def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Adjust the speech rate if needed
    sentences = text.split('. ')
    for sentence in sentences:
        engine.say(sentence)
        engine.runAndWait()
    engine.stop()

