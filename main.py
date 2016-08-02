"""Add events to a Google Calendar."""

import os
import sys

import httplib2
from apiclient import discovery
import oauth2client

import crea

SCOPES = 'https://www.googleapis.com/auth/calendar'

# If modifying these scopes, delete your previously saved credentials at ~/.credentials/
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'


def get_credentials():
    """Get valid user credentials from storage."""
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    credential_path = os.path.join(credential_dir, CLIENT_SECRET_FILE)
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    return credentials


def main(new_events, calendar):
    """Add events to the requested calendar."""
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    for event in new_events:
        print("Adding {0}...".format(event['summary']), end='')
        try:
            service.events().insert(calendarId=calendar, body=event).execute()
        except Exception:
            if "The requested identifier already exists." in str(sys.exc_info()[1]):
                print("Event already exists.")
                continue
            else:
                raise Exception("An error occured: {0} {1}".format(sys.exc_info()[0], sys.exc_info()[1]))
        print("Event added.")


if __name__ == '__main__':
    CREA_CALENDAR_ID = '1if765nauiejb3goqgdij4jk1k@group.calendar.google.com'
    crea_events = crea.get_events()x
    main(crea_events, CREA_CALENDAR_ID)
