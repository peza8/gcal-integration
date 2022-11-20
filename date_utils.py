from dateutil.parser import parse
import datetime

def get_beginning_of_current_week() -> datetime:
    now_date = parse(datetime.datetime.utcnow().isoformat() + 'Z')
    current_week = now_date.isocalendar().week
    current_year = now_date.isocalendar().year
    date_str = f"{current_year}-{current_week}-1"
    date_week_start = datetime.datetime.strptime(date_str, "%Y-%W-%w")
    return date_week_start

def get_end_of_current_week() -> datetime:
    now_date = parse(datetime.datetime.utcnow().isoformat() + 'Z')
    current_week = now_date.isocalendar().week
    current_year = now_date.isocalendar().year
    date_str = f"{current_year}-{current_week}-0"
    date_week_end = datetime.datetime.strptime(date_str, "%Y-%W-%w")
    return date_week_end