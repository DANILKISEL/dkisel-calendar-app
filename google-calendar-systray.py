import json
import datetime
import webbrowser
import threading
import time
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem, Icon

# Function to create a simple icon for the system tray
def create_image(width, height):
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2 - 10, height // 2 - 10, width // 2 + 10, height // 2 + 10),
        fill=(0, 0, 0))
    return image

# Function to check events and open links if necessary
def check_events():
    while True:
        with open('./events.json', 'r') as file:
            events = json.load(file)

        current_time = datetime.datetime.now()

        for event in events:
            event_start = datetime.datetime.fromisoformat(event['start']).replace(tzinfo=None)
            if 0 <= (event_start - current_time).total_seconds() <= 60:
                webbrowser.open(event['meet_link'])
                print(f"Opening meeting link: {event['meet_link']}")

        time.sleep(60)  # Check every minute

# Function to run the system tray icon
def setup(icon):
    icon.visible = True

# Create the system tray icon
icon = Icon("Event Checker", create_image(64, 64), "Event Checker", menu=pystray.Menu(
                MenuItem("Quit", lambda _: icon.stop())
            ))

# Start the event checking in a separate thread
threading.Thread(target=check_events, daemon=True).start()

# Run the system tray application
icon.run(setup)