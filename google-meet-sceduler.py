import pygame
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
import uuid  # Import the uuid module

# Function to create a meeting
def create_meeting(start_time, meet_duration, attendees):
    SERVICE_ACCOUNT_FILE = './credentials.json'  # Path to your credentials file
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('calendar', 'v3', credentials=credentials)

    start_datetime = datetime.datetime.fromisoformat(start_time)
    end_datetime = start_datetime + datetime.timedelta(minutes=meet_duration)

    event = {
        'summary': 'Meeting Title',
        'location': 'Online',
        'description': 'Meeting Description',
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': start_datetime.tzinfo.zone if start_datetime.tzinfo else 'UTC',
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': end_datetime.tzinfo.zone if end_datetime.tzinfo else 'UTC',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': str(uuid.uuid4()),  # Generate a unique requestId
                'conferenceSolutionKey': {
                    'type': "hangoutsMeet"
                }
            }
        },
        'attendees': [{'email': email} for email in attendees],
    }

    event = service.events().insert(calendarId='primary', body=event,
                                    conferenceDataVersion=1).execute()

    print(f"Meeting created: {event.get('htmlLink')}")

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Google Meet Scheduler")

# Set up fonts
font = pygame.font.Font(None, 36)

# Input fields
start_time_input = ""
duration_input = ""
attendees_input = ""
current-input = "start_time_input"


def handle_keydown():

    input = ""


    if event.key == pygame.K_RETURN:  # Press Enter to create meeting
        try:
            attendees_list = tuple(attendees_input.split(","))
            create_meeting(start_time_input, int(duration_input), attendees_list)
        except Exception as e:
            print(f"Error: {e}")

    elif event.key == pygame.K_BACKSPACE:
        if len(input) > 0:
            attendees_input = attendees_input[:-1]
    else:
        attendees_input += event.unicode

# Main loop
running = True
while running:
    screen.fill((255, 255, 255))  # White background

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:


            if event.key == pygame.K_RETURN:  # Press Enter to create meeting
                try:
                    attendees_list = tuple(attendees_input.split(","))
                    create_meeting(start_time_input, int(duration_input), attendees_list)
                except Exception as e:
                    print(f"Error: {e}")

            elif event.key == pygame.K_BACKSPACE:
                if len(attendees_input) > 0:
                    attendees_input = attendees_input[:-1]
            else:
                attendees_input += event.unicode

    # Render text inputs
    start_time_text = font.render(f"Start Time (ISO): {start_time_input}", True, (0, 0, 0))
    duration_text = font.render(f"Duration (min): {duration_input}", True, (0, 0, 0))
    attendees_text = font.render(f"Attendees (comma-separated): {attendees_input}", True, (0, 0, 0))

    screen.blit(start_time_text, (20, 20))
    screen.blit(duration_text, (20, 80))
    screen.blit(attendees_text, (20, 140))

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()