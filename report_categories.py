from gcal_interface import GCalInterface
from date_utils import get_end_of_current_week, get_beginning_of_current_week


def analyze_calendar_categories():
    """Function to aggregate and sum calendar categories
    """
    gcal_client = GCalInterface()
    categories = gcal_client.get_categories(
        get_beginning_of_current_week(),
        get_end_of_current_week()
    )



if __name__ == "__main__":
    analyze_calendar_categories()