from gcal_interface import GCalInterface
from graphics import plot_event_type_aggregates
from date_utils import get_end_of_current_week, get_beginning_of_current_week



def analyze_calendar_categories():
    """Function to aggregate and sum calendar categories
    """
    gcal_client = GCalInterface()
    events = gcal_client.get_events_for_time_window(
        get_beginning_of_current_week(),
        get_end_of_current_week()
    )
    plot_event_type_aggregates(events)


if __name__ == "__main__":
    analyze_calendar_categories()