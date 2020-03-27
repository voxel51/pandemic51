'''
Main app runner.

Copyright 2020, Voxel51, Inc.
voxel51.com
'''
from datetime import datetime
import pandas as pd
import time

from flask import Flask
app = Flask(__name__)

import pandemic51.core.config as panc
import pandemic51.core.database as pand


STREAMS_MAP = {
    "london": "abbey_road",
    "chicago": "chicago",
    "dublin": "dublin",
    "newjersey": "new_jersey",
    "prague": "prague",
    "newyork": "time_square",
    "neworleans": "new_orleans",
}

US_CITIES = {"chicago", "newyork", "neworleans", "newjersey"}

EVENTS_CSV_PATH = "./news_events.csv"


@app.route("/snapshots")
def snapshots():
    '''Serves snapshots for all cities.

    Returns:
        {"data": data}
    '''
    names_rev = {v: k for k, v in STREAMS_MAP.items()}

    data = {}
    for snapshot in pand.query_snapshots():
        if snapshot["city"] not in names_rev:
            continue

        data[names_rev[snapshot["city"]]] = (
            "https://pdi-service.voxel51.com/snapshots" +
            snapshot["url"].replace(panc.P51_BASEDIR + "/data", "")
        )

    return {"data": data}


@app.route("/pdi/<city>")
def pdi(city):
    '''Serves data for the given city.

    Args:
        city: the city

    Returns:
        {"data": data, "events": events, "labels" : labels}
    '''
    if city not in STREAMS_MAP:
        return 404, "Not Found"

    raw = pd.read_csv(EVENTS_CSV_PATH)
    events = []
    for date, city_, event, ref in zip(
            raw["date"], raw["city"], raw["event"], raw["reference"]):
        if city_.strip(" ") == "U.S." and city in US_CITIES:
            pass
        elif city_.strip(" ") == "Worldwide":
            pass
        elif city_ != city:
            continue

        ref = str(ref)
        if ref == "nan":
            continue

        event = event.strip('"')
        events.append({
            "time": time.mktime(
                datetime.strptime(date, "%m/%d/%Y").timetuple()),
            "event": event,
            "reference": ref,
        })

    devents = {int(e["time"]): e for e in events}
    levents = [e["time"] for e in events]
    points = pand.query_stream_pdi(STREAMS_MAP[city])

    for p in points:
        p["url"] = (
            "https://pdi-service.voxel51.com/snapshots" +
            p["url"].replace(panc.P51_BASEDIR + "/data", "")
        )
        p["event"] = _closest(levents, p["time"])
        p["event_val"] = 0

    labels = {p["time"]: p for p in points}

    return {"data": points, "events": devents, "labels" : labels}


def _closest(lst, K):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]


if __name__ == "__main__":
    app.run(host="0.0.0.0")
