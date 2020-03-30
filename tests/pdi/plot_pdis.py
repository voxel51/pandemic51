'''
Script for plotting physical distancing index (PDI).

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
from datetime import datetime
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import eta.core.image as etai
import eta.core.utils as etau

import pandemic51.core.pdi as panp
import pandemic51.core.utils as panu


LABELS_DIR = "out/labels"

CONFIDENCE_THRESH = 0.1

LABELS_WHITELIST = {"person", "bicycle", "car", "motorcycle"}

MIN_DATE = None
#MIN_DATE = etau.parse_isotime("2020-01-01")


# Input images to process
label_paths = etau.list_files(LABELS_DIR, abs_paths=True)


def filter_objects(objects):
    filters = []
    if CONFIDENCE_THRESH:
        filters.append(lambda obj: obj.confidence > CONFIDENCE_THRESH)
    if LABELS_WHITELIST:
        filters.append(lambda obj: obj.label in LABELS_WHITELIST)

    return objects.get_matches(filters, match=all)


# Load data
count_map = {}
for label_path in label_paths:
    timestamp = panu.parse_timestamp_from_path(label_path)
    image_labels = etai.ImageLabels.from_json(label_path)

    objects = image_labels.objects
    objects = filter_objects(objects)

    count_map[timestamp] = len(objects)


if MIN_DATE:
    count_map = {k: v for k, v in count_map.items() if k > MIN_DATE}


# Extract time series
times = [t.timestamp() for t in count_map.keys()]
counts = list(count_map.values())

# Compute PDI
times, pdis, counts = panp.compute_pdi(times, counts, counts)

timestamps = [datetime.utcfromtimestamp(t) for t in times]
plt_times = mpl.dates.date2num(timestamps)

#
# Plot results
#

plt.cla()

plt.plot_date(plt_times, counts, "bo")
plt.plot_date(plt_times, pdis, "r-")
plt.title("physical distancing index")

plt.show()
