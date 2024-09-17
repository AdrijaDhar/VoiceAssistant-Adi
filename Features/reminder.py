from datetime import datetime,timedelta
import time
from Input.text_speech import speak_text

def set_reminder(reminder_text, reminder_time):
    current_time = datetime.now()
    target_time = datetime.strptime(reminder_time, '%H:%M')
    target_time = current_time.replace(hour=target_time.hour, minute=target_time.minute, second=0, microsecond=0)

    # If the target time is earlier than the current time, set it for the next day
    if target_time <= current_time:
        target_time += timedelta(days=1)
    
    # Correctly format the time in 12-hour format with AM/PM
    formatted_time = target_time.strftime('%I:%M %p')
    print(f"Reminder set for {target_time.strftime('%Y-%m-%d')} at {formatted_time}: {reminder_text}")
    speak_text(f"Reminder set for {formatted_time} on {target_time.strftime('%A')}. {reminder_text}")

    # Loop until the reminder time is reached
    while datetime.now() < target_time:
        # Check every second for a more responsive experience
        time.sleep(1)

    print(f"Reminder: {reminder_text}")
    speak_text(f"Reminder: {reminder_text}")

