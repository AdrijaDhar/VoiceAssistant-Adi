import requests
import spacy
from gnews import GNews
from src.voice_output import speak

# Load the spaCy English NLP model
nlp = spacy.load("en_core_web_sm")

# Initialize the GNews client
google_news = GNews(language='en', country='US', max_results=5)

def extract_keywords(query):
    """Use NLP to extract relevant keywords and entities from the query."""
    doc = nlp(query.lower())
    keywords = []

    # Extract named entities and nouns from the query
    for token in doc:
        if token.ent_type_ or token.pos_ in {"NOUN", "PROPN"}:
            keywords.append(token.text)

    # Join keywords into a cleaned query string
    return " ".join(keywords)

def get_news(query):
    """Fetch and speak the top news headlines based on the cleaned query."""
    try:
        cleaned_query = extract_keywords(query)
        print(f"Searching news for: {cleaned_query}")

        # Fetch the news articles
        articles = google_news.get_news(cleaned_query)

        if articles:
            speak(f"Here are the top news results for {cleaned_query}.")
            for i, article in enumerate(articles, start=1):
                headline = article['title']
                print(f"{i}. {headline}")
                speak(headline)
        else:
            speak(f"Sorry, I couldn't find any relevant news for {cleaned_query}.")
            print(f"No news found for {cleaned_query}.")

    except Exception as e:
        print(f"Error fetching news: {e}")
        speak("There was an error fetching the news. Please try again later.")
