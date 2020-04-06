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
    '''Serves PDI data for all cities, normalized to [0, 1] for comparison on a
    single graph.

    Returns:
        {
            "data": [
                {
                    "time": time,
                    "average": <average-normalized-pdi>,
                    "<city1>": <normalized-pdi>,
                    "<city2>": <normalized-pdi>,
                    ...
                },
                ...
            ]
        }
    '''
    return {"data": pana.get_all_pdi_graph_data()}


@app.route("/streams/<city>")
def stream(city):
    '''serves the given city's stream url.

    Args:
        city: the city

    Returns:
        {"url": url}
    '''
    if city not in panc.STREAMS_MAP:
        return 404, "Not Found"

    return {"url": pana.get_stream_url(city)}


@app.route("/covid19/<str:city>/<str:metric>/<int:start>/<int:stop>")
def covid19(city, metric, start, stop):
    '''serves the given city's covid19 <metric> timeseries data, where <metric>
    is one of "cases", "deaths", "recovered".

    Args:
        city: the city
        metric: one of "cases", "deaths", or "recovered"
        start: unix time start timestamp
        stop: unix time end timestamp

    Returns:
        {"data": data}
    '''
    if city not in panc.STREAMS_MAP:
        return 404, "Not Found"

    if metric not in panc.COVID19_METRICS:
        return 404, "Not Found"

    return {"data": pana.get_covid19_timeseries(city, metric, start, stop)}


if __name__ == "__main__":
    app.run(host="0.0.0.0")
