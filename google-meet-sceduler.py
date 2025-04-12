import pygame
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
import uuid  # Import the uuid module

# Function to create a meeting
def create_meeting(start_time, meet_duration, attendees, title, description):
    SERVICE_ACCOUNT_FILE = './credentials.json'  # Path to your credentials file
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('calendar', 'v3', credentials=credentials)

    # Parse start_time from DD.MM.YYYY, HH:MM format
    try:
        start_datetime = datetime.datetime.strptime(start_time, "%d.%m.%Y, %H:%M")
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
        'attendees': [{'email': email.strip()} for email in attendees],
    }

    event = service.events().insert(calendarId='primary', body=event,
                                    conferenceDataVersion=1).execute()

    print(f"Meeting created: {event.get('htmlLink')}")

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Google Meet Scheduler")

# Set up fonts
font = pygame.font.Font("Arial_Black.ttf", 36)

# Input fields
start_time_input = ""
duration_input = ""
attendees_input = ""
title_input = ""
description_input = ""
current_input_index = 0

input_fields = ["start_time", "duration", "attendees", "title", "description"]

def handle_keydown(event):
    global start_time_input,duration_input, attendees_input, title_input, description_input, current_input_index
    if event.key == pygame.K_e:
        screen.fill((255, 255, 255))  # White background


    if current_input_index == 0:  # Start Time Input
        if event.key == pygame.K_RETURN:
            current_input_index += 1  # Move to next input field
        elif event.key == pygame.K_BACKSPACE:
            if len(start_time_input) > 0:
                start_time_input = start_time_input[:-1]
        else:
            start_time_input += event.unicode

    elif current_input_index == 1:  # Duration Input
        if event.key == pygame.K_RETURN:
            current_input_index += 1  # Move to next input field
        elif event.key == pygame.K_BACKSPACE:
            if len(duration_input) > 0:
                duration_input = duration_input[:-1]
        else:
            duration_input += event.unicode

    elif current_input_index == 2:  # Attendees Input
        if event.key == pygame.K_RETURN:
            current_input_index += 1  # Move to next input field
        elif event.key == pygame.K_BACKSPACE:
            if len(attendees_input) > 0:
                attendees_input = attendees_input[:-1]
        else:
            attendees_input += event.unicode

    elif current_input_index == 3:  # Title Input
        if event.key == pygame.K_RETURN:
            current_input_index += 1  # Move to next input field
        elif event.key == pygame.K_BACKSPACE:
            if len(title_input) > 0:
                title_input = title_input[:-1]
        else:
            title_input += event.unicode

    elif current_input_index == 4:  # Description Input
        if event.key == pygame.K_RETURN:  # Press Enter to create meeting
            try:
                attendees_list = tuple(attendees_input.split(","))
                create_meeting(start_time_input, int(duration_input), attendees_list, title_input, description_input)
                # Clear inputs after creating meeting
                start_time_input = ""
                duration_input = ""
                attendees_input = ""
                title_input = ""
                description_input = ""
                current_input_index = 0  # Reset to first input field
            except Exception as e:
                print(f"Error: {e}")
        elif event.key == pygame.K_BACKSPACE:
            if len(description_input) > 0:
                description_input = description_input[:-1]
        else:
            description_input += event.unicode

def handle_navigation(event):
    global current_input_index

    if event.key == pygame.K_DOWN:   # Move down in input fields
        current_input_index += 1
        if current_input_index >= len(input_fields):
            current_input_index = len(input_fields) - 1

    elif event.key == pygame.K_UP:   # Move up in input fields
        current_input_index -= 1
        if current_input_index < 0:
            current_input_index = 0

# Main loop
running = True
while running:
    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            handle_navigation(event)
            handle_keydown(event)

    # Render text inputs based on current input field focus
    colors = [(0, 0, 255) if i == current_input_index else (0, 0, 0) for i in range(len(input_fields))]

    start_time_text = font.render(f"Start Time (DD.MM.YYYY, HH:MM): {start_time_input}", True, colors[0])
    duration_text = font.render(f"Duration (min): {duration_input}", True, colors[1])
    attendees_text = font.render(f"Attendees (comma-separated): {attendees_input}", True, colors[2])
    title_text = font.render(f"Meeting Title: {title_input}", True, colors[3])
    description_text = font.render(f"Meeting Description: {description_input}", True, colors[4])

    # Blit text onto the screen
    screen.blit(start_time_text, (20, 20))
    screen.blit(duration_text, (20, 80))
    screen.blit(attendees_text, (20,140))
    screen.blit(title_text,(20 ,200))
    screen.blit(description_text,(20 ,260))

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

