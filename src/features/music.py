#error while using spotify api- need to fix it later

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from src.voice_output import speak
import json
import os
import subprocess
import webbrowser

# Get the absolute path to the credentials file
current_dir = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(current_dir, "../../config/spotify_credentials.json")

# Load Spotify credentials
with open(credentials_path, "r") as f:
    creds = json.load(f)

# Configure Spotify OAuth
auth_manager = SpotifyOAuth(
    client_id=creds["client_id"],
    client_secret=creds["client_secret"],
    redirect_uri=creds["redirect_uri"],
    scope="user-read-playback-state user-modify-playback-state",
)

# Initialize Spotify client with OAuth
sp = spotipy.Spotify(auth_manager=auth_manager)

def play_on_spotify(track_name):
    """Search for a song on Spotify and open it in the Spotify desktop app."""
    try:
        # Search for the track
        results = sp.search(q=track_name, type='track', limit=1)

        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            track_uri = track['uri']

            print(f"Playing '{track_name}' by {artist_name} on Spotify.")
            speak(f"Playing '{track_name}' by {artist_name} on Spotify.")

            # Use macOS 'open' command to open Spotify with the track URI
            subprocess.run(['open', '-a', 'Spotify', track_uri])

        else:
            print("No tracks found.")
            speak("I couldn't find the song you requested.")

    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify authentication error: {e}")
        speak("There was an issue with Spotify authentication.")
    except Exception as e:
        print(f"Error playing on Spotify: {e}")
        speak("I encountered an issue playing the song on Spotify.")



def search_on_youtube(track_name):
    """Search and open a song on YouTube."""
    try:
        query = f"https://www.youtube.com/results?search_query={track_name.replace(' ', '+')}"
        print(f"Searching for {track_name} on YouTube...")
        speak(f"Searching for {track_name} on YouTube.")
        webbrowser.open(query)
    except Exception as e:
        print(f"Error opening YouTube: {e}")
        speak("I encountered an issue opening YouTube.")


def play_music(track_name, platform):
    """Play music on the chosen platform."""
    platform = platform.lower().strip()
    if platform == "spotify":
        if not play_on_spotify(track_name):
            print("Failed to play on Spotify. Trying YouTube...")
            search_on_youtube(track_name)
    elif platform == "youtube":
        search_on_youtube(track_name)
    else:
        print("Invalid platform. Please choose 'spotify' or 'youtube'.")
        speak("Please choose a valid platform: Spotify or YouTube.")
