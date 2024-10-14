import subprocess
from src.voice_output import speak

def press_brightness_key(key_code, times):
    """Press a brightness key multiple times using AppleScript."""
    try:
        script = f'''
        tell application "System Events"
            repeat {times} times
                key code {key_code}
                delay 0.1
            end repeat
        end tell
        '''

        # Run the AppleScript
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)

        if result.returncode == 0:
            print("Brightness adjusted successfully.")
        else:
            raise Exception(result.stderr)

    except Exception as e:
        print(f"Error adjusting brightness: {e}")
        speak("I couldn't adjust the brightness. Please try manually.")

def set_brightness(level):
    """Set brightness by simulating brightness keys."""
    try:
        if level > 50:
            # Use key code 144 for increasing brightness
            times = (level - 50) // 10  # Calculate number of presses needed
            press_brightness_key(144, times)
            speak(f"Brightness set to {level} percent.")
        elif level < 50:
            # Use key code 145 for decreasing brightness
            times = (50 - level) // 10  # Calculate number of presses needed
            press_brightness_key(145, times)
            speak(f"Brightness set to {level} percent.")
        else:
            speak("Brightness is already at 50 percent.")

    except Exception as e:
        print(f"Error setting brightness: {e}")
        speak("There was an error adjusting the brightness.")


def set_volume(level):
    """Set system volume using AppleScript."""
    try:
        result = subprocess.run(
            ["osascript", "-e", f'set volume output volume {level}'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            speak(f"Volume set to {level} percent.")
            print(f"Volume set to {level} percent.")
        else:
            raise Exception(result.stderr)
    except Exception as e:
        print(f"Error setting volume: {e}")
        speak("I couldn't adjust the volume. Please try manually.")

def mute_volume():
    """Mute the system volume."""
    try:
        subprocess.run(["osascript", "-e", 'set volume output muted true'])
        speak("Volume muted.")
        print("Volume muted.")
    except Exception as e:
        print(f"Error muting volume: {e}")

def unmute_volume():
    """Unmute the system volume."""
    try:
        subprocess.run(["osascript", "-e", 'set volume output muted false'])
        speak("Volume unmuted.")
        print("Volume unmuted.")
    except Exception as e:
        print(f"Error unmuting volume: {e}")

def shutdown():
    """Shutdown the MacBook."""
    try:
        subprocess.run(["sudo", "shutdown", "-h", "now"])
        speak("Shutting down the MacBook.")
    except Exception as e:
        print(f"Error shutting down: {e}")

def restart():
    """Restart the MacBook."""
    try:
        subprocess.run(["sudo", "shutdown", "-r", "now"])
        speak("Restarting the MacBook.")
    except Exception as e:
        print(f"Error restarting: {e}")

def empty_trash():
    """Empty the Trash."""
    try:
        subprocess.run(["rm", "-rf", "~/.Trash/*"])
        speak("Trash emptied.")
        print("Trash emptied.")
    except Exception as e:
        print(f"Error emptying trash: {e}")

def lock_screen():
    """Lock the MacBook screen."""
    try:
        subprocess.run(["pmset", "displaysleepnow"])
        speak("Locking the screen.")
    except Exception as e:
        print(f"Error locking screen: {e}")

def sleep():
    """Put the MacBook to sleep."""
    try:
        subprocess.run(["pmset", "sleepnow"])
        speak("Putting the MacBook to sleep.")
    except Exception as e:
        print(f"Error putting MacBook to sleep: {e}")
