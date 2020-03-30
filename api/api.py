'''
Main app runner.

Copyright 2020, Voxel51, Inc.
voxel51.com
'''
from flask import Flask

import pandemic51.config as panc
import pandemic51.core.api as pana


app = Flask(__name__)


@app.route("/snapshots")
def snapshots():
    '''Serves snapshots for all cities.

    Returns:
        {
            "data": {
                "<city>": {
                    "url": url,
                    "week": week,
                    "max": max,
                },
                ...
            }
        }
    '''
    return {"data": pana.get_snapshots()}


@app.route("/pdi/<city>")
def pdi(city):
    '''Serves PDI graph data for the requested city.

    Args:
        city: the city

    Returns:
        {
            "data": data,
            "events": events,
            "labels" : labels
        }
    '''
    if city not in panc.STREAMS_MAP:
        return 404, "Not Found"

    points, events = pana.get_pdi_graph_data(city)

    labels = {p["time"]: p for p in points}

    return {"data": points, "events": events, "labels": labels}


@app.route("/pdi-all")
def pdi_all():
    '''Serves normalized PDI data for all cities, for comparison on a single
    graph.

    Returns:
        {
            "cities": {
                "<city>": {
                    "time": [...],
                    "normalized_pdi": [...],
                },
                ...
            }
        }
    '''
    return {"cities": pana.get_all_pdi_graph_data()}


@app.route("/streams/<city>")
def stream(city):
    '''Serves the given city's stream URL.

    Args:
        city: the city

    Returns:
        {"url": url}
    '''
    if city not in panc.STREAMS_MAP:
        return 404, "Not Found"

    return {"url": pana.get_stream_url(city)}


if __name__ == "__main__":
    app.run(host="0.0.0.0")
