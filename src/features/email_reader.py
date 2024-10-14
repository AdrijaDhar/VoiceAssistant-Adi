import os
import base64
import json
import subprocess
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from src.voice_output import speak

# Gmail API scope for reading emails
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticate the user and return the Gmail API service."""
    creds = None
    if os.path.exists("config/token.json"):
        creds = Credentials.from_authorized_user_file(".gitignore/token.json", SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "/Users/adrijadhar/Desktop/Voice Assistant/.gitignore/client_secret_785292845338-64kclifmcsaq7c5g16nmh3tqdodkil6a.apps.googleusercontent.com.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open(".gitignore/token.json", "w") as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def read_unread_emails():
    """Fetch and read new emails from Gmail and open the Mail app."""
    try:
        # Open Mac Mail app
        print("Opening Mac Mail app...")
        speak("Opening your Mail app.")
        subprocess.run(['open', '-a', 'Mail'])

        # Authenticate and get unread emails from Gmail
        service = authenticate_gmail()
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages', [])

        if not messages:
            speak("You have no unread emails.")
            print("No unread emails.")
        else:
            speak(f"You have {len(messages)} unread emails.")
            for msg in messages[:5]:  # Read the top 5 unread emails
                msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
                headers = msg_data['payload'].get('headers', [])

                # Extract sender and subject from headers
                sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown sender')
                subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No subject')
                snippet = msg_data.get('snippet', '')

                # Speak out the email details
                email_text = f"New email from {sender}. Subject: {subject}. Snippet: {snippet}."
                print(email_text)  # Print for debugging
                speak(email_text)  # Speak out the email details

    except Exception as e:
        print(f"Error reading emails: {e}")
        speak("I encountered an issue reading your emails.")
