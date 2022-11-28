from pprint import pprint

import matplotlib.pyplot as plt

from gcal_interface import GCalInterface
from models.event import Event
from graphics import plot_event_type_aggregates, plot_event_categories_pie
from date_utils import get_end_of_current_week, get_beginning_of_current_week



def analyze_calendar_categories():
    """Function to aggregate and sum calendar categories
    """
    gcal_client = GCalInterface()
    events = gcal_client.get_events_for_time_window(
        get_beginning_of_current_week(),
        get_end_of_current_week()
    )

    # Plotting
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(14,8))
    plot_event_type_aggregates(events, ax1)
    plot_event_categories_pie(events, ax2)
    plt.show()


if __name__ == "__main__":
    analyze_calendar_categories()