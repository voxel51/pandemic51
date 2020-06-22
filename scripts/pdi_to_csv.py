"""
Pulls the latest PDI data for cities in the comparison chart.

Use --output-file to change the ouptut csv destination. The default is
"./pdi.csv".

NOTES:
    - The CSV is sparsely populated
    - A city is not guaranteed to have a PDI value for a particular timestamp
    - Timestamps are in unix time
    - PDI values fall between 0 and 100

PANDAS (pd.read_csv()) output:

               city  1577664388  1577665807  1577678501  ...
dublin                                                   ...
fortlauderdale                                           ...
hollywood                                                ...
lasvegas                                                 ...
london                                                   ...
miami                                                    ...
newjersey                                                ...
newyork                                                  ...
prague                 15.15776    15.66639    18.08353  ...


Copyright 2017-2020, Voxel51, Inc.
voxel51.com

Benjamin Kane, ben@voxel51.com
"""
import argparse
import requests

CITIES = {
    "london",
    "dublin",
    "newjersey",
    "prague",
    "newyork",
    "fortlauderdale",
    "lasvegas",
    "miami",
}

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
    header = "city, " + ", ".join([str(t) for t in times]) + "\n"
    writer.write(header)
    for city in sorted(list(CITIES)):
        row = city + ", "
        for time in times:
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
