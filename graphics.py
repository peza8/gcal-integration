from typing import List
import matplotlib.pyplot as plt

from models.event import Event


def plot_event_type_aggregates(events: List[Event], ax: plt.Axes):
    # TODO: Move to event class
    colors = ["silver", "gold", "teal", "orchid", "palegreen", "purple", "coral"]
    events_df = Event.get_dataframe_from_events(events)
    events_df_aggregate = events_df.groupby(["category"])["duration"].sum()
    events_df_aggregate.plot.bar(
        x='category',
        y='duration',
        rot=45,
        width=1.0,
        ax=ax,
        color=colors
    )
    ax.set_title("Time spend by category")
    ax.set_ylabel("Time (hours)")

    # plt.gcf().subplots_adjust(bottom=0.35, top=0.7) #adjusting the plotting area
    plt.tight_layout()

def plot_event_categories_pie(events: List[Event], ax: plt.Axes):
    events_df = Event.get_dataframe_from_events(events)
    events_df_aggregate = events_df.groupby(["category"])["duration"].sum()
    events_df_aggregate.plot.pie(y="category")
    plt.tight_layout()