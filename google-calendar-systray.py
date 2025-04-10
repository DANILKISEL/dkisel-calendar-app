import json
import datetime
import webbrowser
import threading
import time
import subprocess
from PIL import Image
import pystray
from pystray import MenuItem, Icon

# Function to load an icon from a specified path
def load_icon(icon_path):
    return Image.open(icon_path)

# Function to check events and open links if necessary
def check_events():
    while True:
        with open('./events.json', 'r') as file:
            events = json.load(file)

        current_time = datetime.datetime.now()

        for event in events:
            event_start = datetime.datetime.fromisoformat(event['start'])
            if 0 <= (event_start - current_time).total_seconds() <= 60:
                webbrowser.open(event['meet_link'])
                print(f"Opening meeting link: {event['meet_link']}")

        time.sleep(60)  # Check every minute

# Function to refresh events manually and run the external script
def refresh_events():
    print("Refreshing events...")
    # Run the google-calendar-requests.py script
    try:
        subprocess.run(['python', './google-calendar-requests.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e}")

# Function to run the system tray icon
def setup(icon):
    icon.visible = True

# Load the icon from ./appIco directory
icon_image = load_icon('appIco.png')

# Create the system tray icon with a refresh option
icon = Icon("Event Checker", icon_image, "Event Checker", menu=pystray.Menu(
    MenuItem("Refresh", refresh_events),
    MenuItem("Quit", lambda _: icon.stop())
            ))

# Start the event checking in a separate thread
threading.Thread(target=check_events, daemon=True).start()

# Run the system tray application
icon.run(setup)