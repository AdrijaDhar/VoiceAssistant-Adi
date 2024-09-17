from Input.input import capture_voice_input
from Input.text_speech import speak_text
# from input_handling.text_input import capture_text_input
from Features.reminder import set_reminder
import re
from datetime import datetime


def extract_time_and_text(user_input):
    # Regular expression to find time in the format 'HH:MM' or 'H:MM a.m./p.m.'
    time_pattern = r'(\b\d{1,2}:\d{2}\s?(?:a\.m\.|p\.m\.)?\b)'
    match = re.search(time_pattern, user_input, re.IGNORECASE)

    if match:
        time_str = match.group(0).strip()
        
        try:
            # Convert to 24-hour format if it's in the 'a.m.' or 'p.m.' format
            if 'a.m.' in time_str.lower() or 'p.m.' in time_str.lower():
                time_obj = datetime.strptime(time_str, '%I:%M %p')
            else:
                # Assume it's a 24-hour format
                time_obj = datetime.strptime(time_str, '%H:%M')

            reminder_time = time_obj.strftime('%H:%M')
            # Extract the reminder text by removing the time part
            reminder_text = user_input.replace(time_str, '').replace('set reminder at', '').strip()
            return reminder_time, reminder_text

        except ValueError:
            print("Invalid time format.")
            speak_text("Invalid time format.")
            return None, None
    else:
        return None, None


def main():
    user_input = capture_voice_input()
    if user_input:
        if "reminder" in user_input:
            reminder_time, reminder_text = extract_time_and_text(user_input)
            if reminder_time:
                if not reminder_text:
                    reminder_text = "This is your reminder."  # Default text if not specified
                set_reminder(reminder_text, reminder_time)
            else:
                print("Could not find a valid time in the input.")
                speak_text("Could not find a valid time in the input.")
        else:
            print("Feature not recognized. Please try again.")
            speak_text("Feature not recognized. Please try again.")

if __name__ == "__main__":
    main()
