import subprocess
from src.voice_output import speak

def set_reminder(reminder_text, minutes):
    """Set a reminder in the Mac Reminders app."""
    try:
        # AppleScript to add a reminder to the Mac Reminders app
        script = f'''
        tell application "Reminders"
            set theReminder to make new reminder with properties {{name:"{reminder_text}"}}
            set due date of theReminder to (current date) + ({minutes} * minutes)
        end tell
        '''

        # Run the AppleScript
        subprocess.run(["osascript", "-e", script], check=True)

        # Confirm the reminder was added
        speak(f"Reminder set: {reminder_text} in {minutes} minutes.")
        print(f"Reminder set: {reminder_text} in {minutes} minutes.")

    except subprocess.CalledProcessError as e:
        print(f"Error setting reminder: {e}")
        speak("There was an error setting the reminder.")
