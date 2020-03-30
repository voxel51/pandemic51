'''
Backend API methods.

Copyright 2020, Voxel51, Inc.
voxel51.com
'''
from collections import defaultdict

import pandemic51.config as panc
import pandemic51.core.database as pand
import pandemic51.core.events as pane


def get_snapshots():
    '''Returns a dictionary of snapshot info.

    Returns:
        {
            "<city>": {
                "url": url,
                "week": week,
                "max": max,
            },
            ...
        }
    '''
    streams_to_cities = {v: k for k, v in panc.STREAMS_MAP.items()}

    snapshots = defaultdict(dict)

    # Get snapshot URLs
    for snapshot in pand.query_snapshots():
        stream_name = snapshot["stream_name"]
        if stream_name not in streams_to_cities:
            continue

        city = streams_to_cities[stream_name]
        snapshots[city]["url"] = _make_snapshot_url(snapshot["url"])

    # Get PDI changes
    pdi_changes = pand.query_pdi_changes()
    for stream_name, pdi_change in pdi_changes.items():
        if stream_name not in streams_to_cities:
            continue

        city = streams_to_cities[stream_name]
        snapshots[city].update(pdi_change)

    return snapshots


def get_pdi_graph_data(city):
    '''Gets PDI graph data for the given city.

    Args:
        city: the city

    Returns:
        points, events
    '''
    # Get PDI values
    stream_name = panc.STREAMS_MAP[city]
    points = pand.query_stream_pdi(stream_name)

    for p in points:
        p["url"] = _make_snapshot_url(p["url"])

    # Load events for city
    events = pane.load_events_for_city(city)

    # Add events to points
    pane.add_events_to_points(points, events)

    return points, events


def _make_snapshot_url(url):
    return panc.SNAPSHOTS_URL + url.replace(panc.DATA_DIR, "")
