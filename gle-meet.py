
# Function to create a meeting
import os
import pickle
import datetime
import uuid
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def get_credentials():
    """Handles the authentication and returns the credentials."""
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None

    # Load credentials from token.pickle if it exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no valid credentials, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def create_meeting(start_time="12.12.2025, 12:34", meet_duration=60, attendees="grown.dk.up@gmail.com", title="NONE", description=""):
    """Creates a meeting in Google Calendar."""

    # Get credentials
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    # Parse start_time from DD.MM.YYYY, HH:MM format
    try:
        start_datetime = datetime.datetime.strptime(start_time, "%d.%m.%Y, %H:%M")
        start_datetime = start_datetime.replace(tzinfo=datetime.timezone.utc)  # Set timezone to UTC or adjust as needed
    except ValueError:
        print("Invalid date format. Please use DD.MM.YYYY, HH:MM.")
        return

    end_datetime = start_datetime + datetime.timedelta(minutes=meet_duration)

    event = {
        'summary': title,
        'location': 'Online',
        'description': description,
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'UTC',  # Use UTC or specify your timezone here
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'UTC',  # Use UTC or specify your timezone here
        },
        'conferenceData': {
            'createRequest': {
                'requestId': str(uuid.uuid4()),  # Generate a unique requestId
                'conferenceSolutionKey': {
                    'type': "hangoutsMeet"
                }
            }
        },
        'attendees': [{'email': email.strip()} for email in attendees.split(',')],
    }

    try:
        event = service.events().insert(calendarId='primary', body=event,
                                        conferenceDataVersion=1).execute()
        print(f"Meeting created: {event.get('htmlLink')}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage (uncomment to use):
create_meeting()
