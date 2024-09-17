from Input.input import capture_voice_input
from Input.text_speech import speak_text
# from input_handling.text_input import capture_text_input
from Features.reminder import set_reminder
import re
from datetime import datetime
import time

def extract_time_and_text(user_input):
    # Regular expression to find time in the format 'HH:MM am/pm' or 'HH:MM'
    time_pattern = r'(\b\d{1,2}:\d{2}\s?(?:am|pm|a\.m\.|p\.m\.)?)'
    match = re.search(time_pattern, user_input, re.IGNORECASE)

    if match:
        time_str = match.group(0).strip()
        print(f"Extracted time string: {time_str}")  # Debug statement

        # Normalize the time string
        time_str_normalized = time_str.lower().replace(' ', '')
        if 'am' in time_str_normalized or 'pm' in time_str_normalized:
            time_str_normalized = time_str_normalized.replace('am', 'a.m.').replace('pm', 'p.m.')
        
        print(f"Normalized time string: {time_str_normalized}")  # Debug statement
        
        try:
            # Check if the time string contains 'a.m.' or 'p.m.' for 12-hour format
            if 'a.m.' in time_str_normalized or 'p.m.' in time_str_normalized:
                time_obj = datetime.strptime(time_str_normalized, '%I:%M%p')
            else:
                # Assume it's a 24-hour format if no 'a.m.' or 'p.m.' is present
                time_obj = datetime.strptime(time_str_normalized, '%H:%M')

            # Convert the time to 24-hour format for setting the reminder
            reminder_time = time_obj.strftime('%H:%M')

            # Extract the reminder text by removing the time part and extra words from the input
            reminder_text = re.sub(time_pattern, '', user_input, flags=re.IGNORECASE).replace('set reminder at', '').replace('today', '').strip()
            
            return reminder_time, reminder_text

        except ValueError:
            print(f"Invalid time format after normalization: {time_str_normalized}")  # More specific debug statement
            speak_text(f"I couldn't understand the time format. Please specify the time more clearly, like '2:30 p.m.' or '14:30'.")
            return None, None
    else:
        print("No valid time found in the input.")  # Debug statement
        speak_text("I couldn't find a valid time in your input. Please say it in a format like '2:30 p.m.' or '14:30'.")
        return None, None






def ask_to_continue():
    speak_text("Do you have any other queries, or should I stop?")
    
    retries = 3  # Allow the user 3 attempts to respond
    while retries > 0:
        response = capture_voice_input()
        print(f"User response: {response}")  # Debug statement
        
        if response:
            # Normalize the input to lower case for comparison
            response = response.lower().strip()
            if "stop" in response or "no" in response or "exit" in response or "quit" in response:
                speak_text("Okay, stopping now. Have a great day!")
                return False
            elif "yes" in response or "continue" in response or "more" in response:
                speak_text("Sure, I am here to help. Please tell me your next query.")
                return True
            else:
                retries -= 1
                speak_text("I didn't catch that. Please say 'stop' if you want to end or 'continue' if you have more queries.")
        else:
            retries -= 1
            speak_text("I didn't hear anything. Please say 'stop' if you want to end or 'continue' if you have more queries.")
    
    # If the user does not respond properly after retries
    speak_text("I'm sorry, I could not understand you. Stopping now. Have a great day!")
    return False


def main():
    while True:
        speak_text("How can I assist you?")
        user_input = capture_voice_input()
        
        if user_input:
            if "reminder" in user_input.lower():
                reminder_time, reminder_text = extract_time_and_text(user_input)
                if reminder_time:
                    if not reminder_text:
                        reminder_text = "This is your reminder."  # Default text if not specified
                    set_reminder(reminder_text, reminder_time)
                    
                    # Ask if the user wants to continue
                    if not ask_to_continue():
                        break
                else:
                    print("Could not find a valid time in the input.")
                    speak_text("I couldn't find a valid time in your input. Please try again.")
            else:
                print("Feature not recognized. Please try again.")
                speak_text("I'm sorry, I can only help with setting reminders right now. Please try saying something like 'Set a reminder at 2:30 p.m.'")
        else:
            speak_text("Sorry, I didn't catch that. Could you please repeat?")
            
        # Optionally, include a small pause before listening again
        time.sleep(1)

if __name__ == "__main__":
    main()

