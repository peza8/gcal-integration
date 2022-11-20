import os
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GCalInterface:
    Scopes = ['https://www.googleapis.com/auth/calendar.readonly']

    def __init__(self) -> None:
        self.creds: Credentials = None
        self.authenticate()
        self.client = build('calendar', 'v3', credentials=self.creds)

    def authenticate(self):
        """The file token.json stores the user's access and refresh tokens, and is
        created automatically when the authorization flow completes for the first
        time.
        """
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.Scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.Scopes)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

    def get_categories(self, min_date: datetime.datetime, max_date: datetime.datetime) -> dict:
        """Method to fetch raw
        """
        try:
            print(f"Fetching category data from {min_date} to {max_date}")
            page_token = None
            min_date_str = min_date.isoformat() + 'Z'
            max_date_str = max_date.isoformat() + 'Z'
            while True:
                events = self.client.events().list(
                    calendarId='primary',
                    pageToken=page_token,
                    timeMin=min_date_str,
                    timeMax=max_date_str,
                    # maxResults=10,
                    # singleEvents=True,
                ).execute()
                for event in events['items']:
                    print(event.get('summary'))
                    print(event.get('eventType'))
                page_token = events.get('nextPageToken')
                if not page_token:
                    break
        except HttpError as err:
            print(f'HTTP error: {err}')