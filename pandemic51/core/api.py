'''
Backend API methods.

Copyright 2020, Voxel51, Inc.
voxel51.com
'''
from collections import defaultdict

import numpy as np

import pandemic51.config as panc
import pandemic51.core.database as pand
import pandemic51.core.events as pane
import pandemic51.core.pdi as panp
import pandemic51.core.streaming as pans


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

    # Get all PDI values
    all_pdi = pand.query_all_pdi()

    # Compute PDI changes
    for stream_name, data in all_pdi.items():
        if stream_name not in streams_to_cities:
            continue

        city = streams_to_cities[stream_name]
        week_change, max_change = panp.compute_pdi_change(
            data["time"], data["pdi"])
        snapshots[city]["week"] = week_change
        snapshots[city]["max"] = max_change

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


def get_all_pdi_graph_data():
    '''Gets normalized PDI graph data for all cities, for comparison on a
    single graph.

    Returns:
        [
            {
                "time": time,
                "average": <average-normalized-pdi>,
                "<city1>": <normalized-pdi>,
                "<city2>": <normalized-pdi>,
                ...
            },
            ...
        ]
    '''
    streams_to_cities = {v: k for k, v in panc.STREAMS_MAP.items()}

    # Get all PDI values
    all_pdi = pand.query_all_pdi()

    # Normalize PDI values
    norm_pdi = {}
    for stream_name, data in all_pdi.items():
        if stream_name not in streams_to_cities:
            continue

        city = streams_to_cities[stream_name]
        norm_pdi[city] = {
            "time": data["time"],
            "pdi": panp.normalize_pdi_values(data["pdi"]),
        }

    # Resample to uniform times
    data = panp.resample_pdis(norm_pdi)

    # Add average PDI series
    for d in data:
        vals = [v for k, v in d.items() if k != "time" and v is not None]
        d["average"] = np.mean(vals) if vals else None

    return data


def get_stream_url(city):
    '''Gets the stream URL for the given city.

    Args:
        city: the city

    Returns:
        the stream URL
    '''
    stream_name = panc.STREAMS_MAP[city]
    stream = pans.Stream.from_stream_name(stream_name)
    return stream.get_live_stream_url()


def _make_snapshot_url(url):
    return panc.SNAPSHOTS_URL + url.replace(panc.DATA_DIR, "")
