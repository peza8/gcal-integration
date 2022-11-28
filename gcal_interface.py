import os
from typing import List
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config_interface import config_interface
from models.event import Event

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

    def get_events_for_time_window(self, min_date: datetime.datetime, max_date: datetime.datetime) -> List[Event]:
        """Method to fetch raw
        """
        events_list = []
        try:
            print(f"Fetching category data from {min_date} to {max_date}")
            for calendar_id in config_interface.get_calendar_ids():
                events_list += self._get_events_for_time_window_from_pagination(
                    calendar_id=calendar_id,
                    min_date=min_date,
                    max_date=max_date
                )
        except HttpError as err:
            print(f'HTTP error: {err}')
        return events_list

    def get_calendars(self) -> List[str]:
        page_token = None
        while True:
            calendar_list = self.client.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                print(calendar_list_entry['summary'])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

    def _get_events_for_time_window_from_pagination(
        self,
        calendar_id: str,
        min_date: datetime.datetime,
        max_date: datetime.datetime
    ) -> List[Event]:
        events_list = []
        page_token = None
        min_date_str = min_date.isoformat() + 'Z'
        max_date_str = max_date.isoformat() + 'Z'
        while True:
            events = self.client.events().list(
                calendarId=calendar_id,
                pageToken=page_token,
                timeMin=min_date_str,
                timeMax=max_date_str,
            ).execute()
            events_list += events.get("items")
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        return Event.event_from_list(events_list)