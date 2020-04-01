'''
Methods for working with events.

Copyright 2020, Voxel51, Inc.
voxel51.com
'''
from datetime import datetime, timedelta
import dateutil.parser
import time as tm

import numpy as np
import pandas as pd

import pandemic51.config as panc


MAX_EVENT_AGE_DAYS = 3


def load_events_for_city(city):
    '''Loads the events for the given city.

    Args:
        city: the city name

    Returns:
        {
            "<time>": {
                "time": time,
                "event": event,
                "reference": reference,
            },
            ...
        }
    '''
    raw = pd.read_csv(panc.EVENTS_PATH)

    events = {}
    for date, city_, event, reference in zip(
            raw["date"], raw["city"], raw["event"], raw["reference"]):
        load_event = False

        if city_ == city:
            load_event = True
        elif city_.strip(" ") == "U.S." and city in panc.US_CITIES:
            load_event = True
        elif city_.strip(" ") == "Worldwide":
            load_event = True

        reference = str(reference)
        if reference == "nan":
            load_event = False

        if not load_event:
            continue

        event_time = int(tm.mktime(dateutil.parser.parse(date).timetuple()))
        events[event_time] = {
            "time": event_time,
            "event": event.strip('"'),
            "reference": reference,
        }

    return events


def add_events_to_points(points, events):
    '''Adds events to the points in the given list, when possible.

    Args:
        points: list of dicts returned by `query_stream_pdi`
        events: dict returned by `load_events_for_city`

    Returns:
        the input `points` with `event` and `event_val` keys added
    '''
    event_timestamps = sorted(events.keys())
    event_times = [datetime.utcfromtimestamp(t) for t in event_timestamps]

    for p in points:
        point_time = datetime.utcfromtimestamp(p["time"])
        event_idx = _find_event_index(point_time, event_times)

        if event_idx is not None:
            p["event"] = event_timestamps[event_idx]
        else:
            p["event"] = None

        p["event_val"] = 0


def _find_event_index(time, event_times):
    idx = np.searchsorted(event_times, time) - 1
    if idx < 0:
        # Time is before all events
        return None

    if abs(time - event_times[idx]) > timedelta(days=MAX_EVENT_AGE_DAYS):
        # Last event is too old
        return None

    return idx
