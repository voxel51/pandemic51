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
    '''Serves snapshot URLs for all cities.

    Returns:
        {"data": {"<city>": "<snapshot-url>", ...}}
    '''
    return {"data": pana.get_snapshots()}


@app.route("/pdi/<city>")
def pdi(city):
    '''Serves PDI graph data for the requested city.

    Args:
        city: the city

    Returns:
        {"data": data, "events": events, "labels" : labels}
    '''
    if city not in panc.STREAMS_MAP:
        return 404, "Not Found"

    points, events = pana.get_pdi_graph_data(city)

    labels = {p["time"]: p for p in points}

    return {"data": points, "events": events, "labels" : labels}


if __name__ == "__main__":
    app.run(host="0.0.0.0")
