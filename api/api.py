'''
Main app runner.

Copyright 2020, Voxel51, Inc.
voxel51.com
'''
from flask import Flask
import urllib

import eta.core.serial as etas

import pandemic51.config as panc
import pandemic51.core.api as pana
import pandemic51.core.streaming as pans


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


@app.route("/streams/<city>")
def stream(city):
    '''Serves a city's up to date stream URL.

    Args:
        city: the city

    Returns:
        {
            "url": url
        }
    '''
    stream_name = panc.STREAMS_MAP[city]
    url = etas.load_json(panc.STREAMS_PATH)[stream_name]["chunk_path"]
    try:
        urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        url = pans.update_streams(stream_name)

    if "videos2archives" in url:
        url = "https://pdi-service.voxel51.com/stream-archive/" + url.split(".com/")[1]
    elif "earthcam" in url:
        url = "https://pdi-service.voxel51.com/stream/" + url.split(".com/")[1]

    return {"url": url}


if __name__ == "__main__":
    app.run(host="0.0.0.0")
