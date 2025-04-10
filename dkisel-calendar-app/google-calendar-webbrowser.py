import json
import datetime
import webbrowser

# Load events from the JSON file
with open('./events.json', 'r') as file:
    events = json.load(file)

# Get current local time
current_time = datetime.datetime.now()

for event in events:
    # Parse event start time with timezone info
    event_start = datetime.datetime.fromisoformat(event['start']).replace(tzinfo=None)

    # Check if the event starts in 1 minute
    if 0 <= (event_start - current_time).total_seconds() <= 60:
        # Open the meet link
        webbrowser.open(event['meet_link'])
        print(f"Opening meeting link: {event['meet_link']}")