import subprocess
from src.voice_output import speak

def read_recent_notifications():
    """Fetch and read recent notifications from macOS."""
    try:
        # AppleScript to get the last 5 notifications
        script = '''
        tell application "System Events"
            set recentNotifications to {}
            set appProcesses to application processes

            repeat with appProcess in appProcesses
                try
                    set appName to name of appProcess
                    set notifications to every notification of appProcess
                    repeat with n in notifications
                        set end of recentNotifications to appName & ": " & description of n
                    end repeat
                end try
            end repeat

            return recentNotifications
        end tell
        '''

        # Execute the AppleScript using osascript
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        notifications = result.stdout.strip().split(", ")

        if notifications and notifications[0] != "":
            print("Recent Notifications:")
            speak("Here are your recent notifications.")
            for notification in notifications[:5]:  # Limit to the top 5
                print(notification)
                speak(notification)
        else:
            print("No recent notifications found.")
            speak("You don't have any recent notifications.")

    except Exception as e:
        print(f"Error reading notifications: {e}")
        speak("I encountered an issue reading your notifications.")
