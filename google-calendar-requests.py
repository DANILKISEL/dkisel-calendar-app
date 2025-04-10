import os
import datetime
import pickle
import json  # Import json module for saving data
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class Event:
    def __init__(self, event_name: str, start_time: datetime.datetime, meet_link: str):
        self.event_name = event_name
        self.start_time = start_time.isoformat()  # Store as ISO format string for JSON serialization
        self.meet_link = meet_link

    def to_dict(self):
        """Convert the Event instance to a dictionary for JSON serialization."""
        return {
            "event_name": self.event_name,
            "start_time": self.start_time,
            "meet_link": self.meet_link
        }

def main():
    """Shows basic usage of the Calendar API.
Prints the next 10 events on the user's calendar along with their Google Meet links,
and saves them to events.json.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.now().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting upcoming events')

    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    event_list = []  # List to hold Event instances

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        summary = event.get('summary', 'No Title')

        # Check for conference data (Google Meet link)
        meet_link = None
        if 'conferenceData' in event:
            meet_link_info = event['conferenceData'].get('entryPoints', [])
            for entry in meet_link_info:
                if entry.get('entryPointType') == 'video':
                    meet_link = entry.get('uri')
                    break

        # Create an Event instance and add it to the list
        event_instance = Event(event_name=summary, start_time=datetime.datetime.fromisoformat(start[:-1]), meet_link=meet_link if meet_link else "")
        event_list.append(event_instance)

    # Convert Event instances to dictionaries for JSON serialization
    serialized_events = [event.to_dict() for event in event_list]

    # Save events to JSON file
    with open('events.json', 'w') as json_file:
        json.dump(serialized_events, json_file, indent=4)  # Write list to JSON file

    print(f"Saved {len(event_list)} upcoming events to events.json")

if __name__ == '__main__':
    main()