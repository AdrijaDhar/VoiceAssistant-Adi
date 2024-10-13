import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

from datetime import datetime
import requests
import pytz
import re
from src.voice_input import get_text_input, get_voice_input
from src.voice_output import speak
import urllib3
import spacy
from dateutil import parser
from transformers import pipeline
import json
# Load HuggingFace's NER model

# Load the small English model from SpaCy
nlp = spacy.load("en_core_web_sm")
# Suppress urllib3 warnings
urllib3.disable_warnings(urllib3.exceptions.NotOpenSSLWarning)

def greet_user():
    """
    Greet the user based on the time of day.
    """
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        greeting = "Good Morning!"
    elif 12 <= current_hour < 18:
        greeting = "Good Afternoon!"
    elif 18 <= current_hour < 21:
        greeting = "Good Evening!"
    else:
        greeting = "Good Night!"

    speak(greeting)
    speak("How can I assist you today?")
    print(f"{greeting} How can I assist you today?")


def process_query(query):
    """
    Process the user's query and respond accordingly.
    """
    query = query.lower()

    if "date" in query:
        today = datetime.now().strftime("%A, %B %d, %Y")
        response = f"Today's date is {today}."
        print(response)
        speak(response)

    elif "time" in query:
        # Extract the city name from the query
        city = get_city_from_query(query)
        get_time_for_city(city)

    elif "weather" in query:
        print("Fetching weather updates...")
        speak("Fetching weather updates...")
        fetch_weather(query)

    else:
        response = "I am not sure how to help with that."
        print(response)
        speak(response)




import re
from transformers import pipeline
from fuzzywuzzy import process

# Load the NER pipeline
ner_pipeline = pipeline(
    "ner", 
    model="dslim/bert-base-NER", 
    aggregation_strategy="simple", 
    device=-1  # Use CPU explicitly
)

# Load the city names from OpenWeatherMap city list (you must have this JSON loaded)
with open("city.list.json", "r", encoding="utf-8") as f:
    city_data = json.load(f)

CITY_NAMES = [city["name"] for city in city_data]

def clean_query_for_ner(query):
    """
    Remove punctuation and unnecessary words for better NER performance.
    """
    query = re.sub(r"[^\w\s]", "", query)  # Remove punctuation
    query = re.sub(r"\b(?:what|is|the|of|in|right|now|today)\b", "", query, flags=re.IGNORECASE)
    return query.strip()

def get_city_from_query(query):
    """
    Extract the city name using NER with a fallback to fuzzy matching.
    """
    try:
        cleaned_query = clean_query_for_ner(query)
        print(f"Cleaned query for NER: {cleaned_query}")

        # Step 1: Run NER on the cleaned query
        ner_results = ner_pipeline(cleaned_query)
        city_tokens = [
            entity["word"].replace("##", "") for entity in ner_results
            if entity["entity_group"] in {"LOC", "GPE"}
        ]
        city = " ".join(city_tokens).strip()

        if city:
            print(f"Extracted city (NER): {city}")
            return city

        print("No city found in cleaned query, retrying with original query.")

        # Step 2: Retry NER with the original query
        ner_results = ner_pipeline(query)
        city_tokens = [
            entity["word"].replace("##", "") for entity in ner_results
            if entity["entity_group"] in {"LOC", "GPE"}
        ]
        city = " ".join(city_tokens).strip()

        if city:
            print(f"Extracted city on retry (NER): {city}")
            return city

        # Step 3: Fallback to fuzzy matching with OpenWeatherMap city names
        matched_city, score = process.extractOne(query, CITY_NAMES)
        if score > 70:
            print(f"Extracted city (Fuzzy): {matched_city}")
            return matched_city

        print("No city found after retries, using default location.")
        return get_user_location()

    except Exception as e:
        print(f"Error extracting city: {str(e)}")
        speak("Sorry, I couldn't determine the city. Using Kolkata as default.")
        return "Kolkata"





def get_user_location():
    """
    Get the user's location using IP address.
    """
    try:
        response = requests.get('https://ipinfo.io')
        location_data = response.json()
        city = location_data.get('city', 'Kolkata')  # Default to Kolkata
        return city
    except Exception as e:
        print(f"Could not determine location: {str(e)}")
        speak("Sorry, I couldn't determine your location. Using Kolkata as default.")
        return "Kolkata"


def get_time_for_city(city):
    """
    Get the current time for the given city using the World Time API.
    """
    try:
        # Fetch the list of timezones
        url = "http://worldtimeapi.org/api/timezone"
        response = requests.get(url)
        timezones = response.json()

        # Find a matching timezone for the city
        matching_timezone = next((tz for tz in timezones if city.lower() in tz.lower()), None)

        if matching_timezone:
            # Fetch the current time for the matching timezone
            timezone_url = f"http://worldtimeapi.org/api/timezone/{matching_timezone}"
            timezone_response = requests.get(timezone_url).json()

            # Extract and parse the datetime string
            raw_time = timezone_response["datetime"]
            parsed_time = parser.isoparse(raw_time)  # Use dateutil parser

            # Format the parsed time to 12-hour format with AM/PM
            formatted_time = parsed_time.strftime("%I:%M %p")
            result = f"The current time in {city} is {formatted_time}."
        else:
            result = f"Sorry, I couldn't find the timezone for {city}."

        print(result)
        speak(result)

    except Exception as e:
        print(f"Error fetching time for {city}: {str(e)}")
        speak(f"Sorry, I couldn't fetch the time for {city}.")



def fetch_weather(query):
    api_key = "03affd43bfa223102b782377b13afec0"
    city = get_city_from_query(query)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        weather_data = response.json()

        if weather_data["cod"] == 200:
            temp = weather_data["main"]["temp"]
            description = weather_data["weather"][0]["description"]
            result = f"The weather in {city} is {description} with a temperature of {temp}°C."
            print(result)
            speak(result)
        else:
            error_message = f"Could not fetch weather for {city}. Please try again."
            print(error_message)
            speak(error_message)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        speak("Sorry, I couldn't fetch the weather right now.")





def main():
    """
    Main function to start the voice assistant.
    """
    greet_user()
    speak("Would you like to use text or voice input?")
    print("Type '1' for text input or '2' for voice input.")

    choice = input("Your choice: ")

    if choice == '1':
        query = get_text_input()
    elif choice == '2':
        query = get_voice_input()
    else:
        speak("Invalid choice. Please enter one or two.")
        print("Invalid choice. Please enter '1' or '2'.")
        return

    if query:
        process_query(query)


if __name__ == "__main__":
    main()
