import os
import datetime
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    """Shows basic usage of the Calendar API.
    Prints the next 10 events on the user's calendar along with their Google Meet links.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
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

        print(f"Event: {summary}")
        print(f"Start: {start}")

        if meet_link:
            print(f"Google Meet Link: {meet_link}")
        else:
            print("No Google Meet link available.")

        print()  # Print a newline for better readability

if __name__ == '__main__':
    main()