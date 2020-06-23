"""
Pulls the latest PDI data for cities in the comparison chart.

Use --output-file to change the ouptut csv destination. The default is
"./pdi.csv".

NOTES:
    - The CSV is sparsely populated
    - Columns are cities, rows are timestamps
    - A city is not guaranteed to have a PDI value for a particular timestamp
    - Timestamps are in unix time
    - PDI values fall between 0 and 100

Copyright 2017-2020, Voxel51, Inc.
voxel51.com

Benjamin Kane, ben@voxel51.com
"""
import argparse
import requests

CITIES = sorted(
    list(
        {
            "london",
            "dublin",
            "newjersey",
            "prague",
            "newyork",
            "fortlauderdale",
            "lasvegas",
            "miami",
        }
    )
)

ENDPOINT = "https://pdi-service.voxel51.com/api/pdi/%s"

parser = argparse.ArgumentParser(description="CSV generator for Voxel51's PDI")

parser.add_argument("--output-file", type=str, default="pdi.csv")


def pdi_to_csv(writer):
    times = set()
    results = {}
    for city in CITIES:
        url = ENDPOINT % city
        json = requests.get(url=url).json()
        city_results = {}
        for point in json["data"]:
            times.add(point["time"])
            city_results[point["time"]] = point["pdi"]
        results[city] = city_results

    times = sorted(list(times))
    header = "time, " + ", ".join(CITIES) + "\n"
    writer.write(header)
    for time in times:
        row = str(time)
        for city in CITIES:
            if time not in results[city]:
                row += ", "
            else:
                row += ", %0.5f" % results[city][time]
        row += "\n"
        writer.write(row)


if __name__ == "__main__":
    fl = parser.parse_args().output_file
    with open(fl, "w") as writer:
        pdi_to_csv(writer)
