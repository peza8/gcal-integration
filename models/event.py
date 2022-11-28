from typing import List
import json
import datetime
from pprint import pprint

import pandas as pd

from date_utils import get_date_from_string


class Event:
    def __init__(self, event_data: dict) -> None:
        self.raw_data = event_data
        self.title = event_data["summary"]
        self.attendees = self.get_attendees(event_data)
        self.attendees_count = len(self.attendees)
        self.event_type = event_data["eventType"]
        self.color_id = self.get_color_id(event_data)
        self.event_type_category = self.get_pretty_category_name()
        self.start_time = self.get_date_from_event_data(event_data["start"])
        self.end_time = self.get_date_from_event_data(event_data["end"])
        self.duration = self.compute_duration()


    # -------------------------------------------------------
    #                     Class Methods
    # -------------------------------------------------------
    @classmethod
    def event_from_list(cls, raw_events: List[dict]) -> List["Event"]:
        return [Event(x) for x in raw_events if x["status"] != "cancelled"]

    @classmethod
    def get_dataframe_from_events(cls, events: List["Event"]) -> pd.DataFrame:
        category_list = [event.event_type_category for event in events]
        duration_list = [event.duration for event in events]
        events_df = pd.DataFrame({
            "category": category_list,
            "duration": duration_list
        })
        return events_df

    # -------------------------------------------------------
    #                   Public Methods
    # -------------------------------------------------------
    def print_event_list(event_list: List["Event"]):
        for event in event_list:
            # pprint(event.raw.__dict__, indent=2)
            # pprint(event.color_id, indent=2)
            print(f"{event.color_id} | {event.title}")

    def is_collaborative_work_event(self) -> bool:
        return self.attendees_count > 1 and self.event_type == "default"

    def get_pretty_category_name(self) -> str:
        # print(f"{self.title} | Color id: {self.color_id}")
        EVENT_TYPES = {
            0: "Standard",
            10: "Deep Work",
            3: "Music",
            8: "Admin",
            4: "Social",
            1: "Exercise"
        }
        event_type = EVENT_TYPES[self.color_id]
        if event_type == "Standard":
            if self.is_collaborative_work_event():
                return "Collaborative work"
            else:
                return "Individual non-deep work"
        else:
            return event_type


    # -------------------------------------------------------
    #                   Private Methods
    # -------------------------------------------------------
    def __str__(self):
        object_str = str(self.__dict__)
        object_str_formatted = json.dumps(object_str, indent=2)
        return object_str_formatted


    def compute_duration(self) -> float:
        elapsed_time = self.end_time - self.start_time
        duration_in_s = elapsed_time.total_seconds()
        duration_hrs = round(duration_in_s / (60*60), 2)
        return duration_hrs

    def get_attendees(self, event_data: str) -> List[str]:
        attendees = event_data.get("attendees")
        if attendees is None:
            return []
        else:
            return attendees

    def get_date_from_event_data(self, event_time_data: dict) -> datetime.datetime:
        event_time_str = event_time_data.get("dateTime")
        if event_time_str is None:
            event_time_str = event_time_data.get("date")
        return get_date_from_string(event_time_str)

    def get_color_id(self, event_data: dict) -> int:
        color_id_str = event_data.get("colorId")
        if color_id_str is None:
            return 0
        else:
            return int(color_id_str)