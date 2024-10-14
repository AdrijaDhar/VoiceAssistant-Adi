import os
import subprocess
from src.voice_output import speak

def open_application(app_name):
    """Try to open an application on macOS."""
    try:
        # Common apps are often available via `open -a` without searching
        print(f"Trying to open: {app_name}")
        result = subprocess.run(['open', '-a', app_name], capture_output=True, text=True)

        if result.returncode == 0:
            speak(f"Opening {app_name}.")
            print(f"{app_name} opened successfully.")
            return True
        else:
            # If not found, try searching manually in /Applications
            app_path = f"/Applications/{app_name}.app"
            if os.path.exists(app_path):
                print(f"Found {app_name} in Applications folder.")
                subprocess.Popen(['open', app_path])
                speak(f"Opening {app_name}.")
                return True

            print(f"{app_name} not found on the device.")
            return False  # App not found; fallback to Google search
    except Exception as e:
        print(f"Error opening {app_name}: {e}")
        speak(f"I encountered an issue opening {app_name}.")
        return False
