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


NAMES = {
    "london": "abbey_road",
    "chicago": "chicago",
    "dublin": "dublin",
    "newjersey": "new_jersey",
    "prague": "prague",
    "newyork": "time_square",
    "neworleans": "new_orleans",
}

US = {"chicago", "newyork", "neworleans", "newjersey"}

EVENTS_CSV_PATH = "./news_events.csv"


@app.route("/snapshots")
def snapshots():
    inv = {v: k for k, v in NAMES.items()}
    r = pand.query_snapshots()
    res = {}
    for i in r:
        if i["city"] not in inv:
            continue

        res[inv[i["city"]]] = (
            "https://pdi-service.voxel51.com/snapshots" +
            i["url"].replace(panc.P51_BASEDIR + "/data", "")
        )

    return {"data": res}


@app.route("/pdi/<city>")
def pdi(city):
    if city not in NAMES:
        return 404, "Not Found"

    raw = pd.read_csv(EVENTS_CSV_PATH)
    events = []
    for date, city_, event, ref in zip(
            raw["date"], raw["city"], raw["event"], raw["reference"]):
        if city_.strip(" ") == "U.S." and city in US:
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
    points = pand.query_stream_pdi(NAMES[city])

    def closest(lst, K):
        return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]

    for p in points:
        p["url"] = (
            "https://pdi-service.voxel51.com/snapshots" +
            p["url"].replace(panc.P51_BASEDIR + "/data", "")
        )
        p["event"] = closest(levents, p["time"])
        p["event_val"] = 0

    labels = {p["time"]: p for p in points}

    return {"data": points, "events": devents, "labels" : labels}


if __name__ == "__main__":
    app.run(host='0.0.0.0')
