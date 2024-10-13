import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

from datetime import datetime
import requests
import pytz
import re
import urllib3
import spacy
from dateutil import parser
from transformers import pipeline
import json
from src.voice_input import get_text_input, get_voice_input
from src.voice_output import speak
from src.features.reminder import set_reminder  # Use Mac Calendar app for reminders
from fuzzywuzzy import process

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")
urllib3.disable_warnings(urllib3.exceptions.NotOpenSSLWarning)

# HuggingFace's NER pipeline
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple", device=-1)

# Load OpenWeatherMap city data
with open("city.list.json", "r", encoding="utf-8") as f:
    city_data = json.load(f)

CITY_NAMES = [city["name"] for city in city_data]

def greet_user():
    """Greet the user based on the time of day."""
    current_hour = datetime.now().hour
    greeting = (
        "Good Morning!" if 5 <= current_hour < 12 else
        "Good Afternoon!" if 12 <= current_hour < 18 else
        "Good Evening!" if 18 <= current_hour < 21 else
        "Good Night!"
    )
    speak(greeting)
    speak("How can I assist you today?")
    print(f"{greeting} How can I assist you today?")

def clean_query_for_ner(query):
    """Clean the query for better NER performance."""
    query = re.sub(r"[^\w\s]", "", query)
    query = re.sub(r"\b(?:what|is|the|of|in|right|now|today)\b", "", query, flags=re.IGNORECASE)
    return query.strip()

def get_city_from_query(query):
    """Extract the city name using NER or fallback to fuzzy matching."""
    try:
        cleaned_query = clean_query_for_ner(query)
        ner_results = ner_pipeline(cleaned_query)
        city_tokens = [entity["word"].replace("##", "") for entity in ner_results if entity["entity_group"] in {"LOC", "GPE"}]
        city = " ".join(city_tokens).strip()

        if not city:
            matched_city, score = process.extractOne(query, CITY_NAMES)
            city = matched_city if score > 70 else get_user_location()

        print(f"City found: {city}")
        return city

    except Exception as e:
        print(f"Error extracting city: {e}")
        speak("Sorry, I couldn't determine the city. Using Kolkata as default.")
        return "Kolkata"

def get_user_location():
    """Get the user's location using IP address."""
    try:
        response = requests.get('https://ipinfo.io').json()
        return response.get('city', 'Kolkata')
    except Exception as e:
        print(f"Location error: {e}")
        return "Kolkata"

def get_time_for_city(city):
    """Get the time for a city using World Time API."""
    try:
        url = "http://worldtimeapi.org/api/timezone"
        timezones = requests.get(url).json()
        matching_timezone = next((tz for tz in timezones if city.lower() in tz.lower()), None)

        if matching_timezone:
            timezone_response = requests.get(f"http://worldtimeapi.org/api/timezone/{matching_timezone}").json()
            parsed_time = parser.isoparse(timezone_response["datetime"]).strftime("%I:%M %p")
            result = f"The current time in {city} is {parsed_time}."
            print(result)
            speak(result)
        else:
            speak(f"Sorry, I couldn't find the timezone for {city}.")

    except Exception as e:
        print(f"Time error: {e}")

def fetch_weather(query):
    """Fetch weather information for a city."""
    api_key = "03affd43bfa223102b782377b13afec0"
    city = get_city_from_query(query)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        weather_data = requests.get(url).json()
        if weather_data["cod"] == 200:
            temp = weather_data["main"]["temp"]
            description = weather_data["weather"][0]["description"]
            result = f"The weather in {city} is {description} with a temperature of {temp}°C."
            print(result)
            speak(result)
        else:
            speak(f"Could not fetch weather for {city}.")
    except Exception as e:
        print(f"Weather error: {e}")

def get_minutes_from_user():
    """Prompt user for the number of minutes."""
    for attempt in range(3):
        speak("In how many minutes?")
        time_input = get_voice_input()
        match = re.search(r"\d+", time_input)
        if match:
            return int(match.group())
    return int(input("Enter the time in minutes: "))

def process_query(query):
    """Process the user's query."""
    query = query.lower()

    if "date" in query:
        today = datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today's date is {today}.")
    
    elif "time" in query:
        city = get_city_from_query(query)
        get_time_for_city(city)

    elif "weather" in query:
        fetch_weather(query)

    elif "reminder" in query:
        speak("What should I remind you about?")
        reminder_text = get_voice_input() or input("Enter the reminder text: ")
        minutes = get_minutes_from_user()
        set_reminder(reminder_text, minutes)

    else:
        speak("I'm not sure how to help with that.")

def main():
    """Main function to start the voice assistant."""
    greet_user()
    print("Type '1' for text input or '2' for voice input.")
    choice = input("Your choice: ")

    if choice == '1':
        query = get_text_input()
    elif choice == '2':
        query = get_voice_input()
    else:
        speak("Invalid choice.")
        return

    if query:
        process_query(query)

if __name__ == "__main__":
    main()
