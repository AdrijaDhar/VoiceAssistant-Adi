from datetime import datetime
import time
from Input.text_speech import speak_text

def set_reminder(reminder_text, reminder_time):
    current_time = datetime.now()
    target_time = datetime.strptime(reminder_time, '%H:%M')
    # Assuming the reminder is for today
    time_to_wait = (target_time - current_time).seconds

    print(f"Reminder set for {reminder_time}")
    speak_text(f"Reminder set for {reminder_time}")

    # Wait until the reminder time
    time.sleep(time_to_wait)

    print(f"Reminder: {reminder_text}")
    speak_text(f"Reminder: {reminder_text}")
