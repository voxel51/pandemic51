'''
Test script for plotting object density vs time.

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal as sps

import eta.core.image as etai
import eta.core.utils as etau

import pandemic51.core.utils as panu


LABELS_DIR = "out/labels"

CONFIDENCE_THRESH = 0.1

LABELS_WHITELIST = {"person", "bicycle", "car", "motorcycle"}

#MIN_DATE = None
MIN_DATE = etau.parse_isotime("2020-02-01")


# Input images to process
label_paths = etau.list_files(LABELS_DIR, abs_paths=True)


def filter_objects(objects):
    filters = []
    if CONFIDENCE_THRESH:
        filters.append(lambda obj: obj.confidence > CONFIDENCE_THRESH)
    if LABELS_WHITELIST:
        filters.append(lambda obj: obj.label in LABELS_WHITELIST)

    return objects.get_matches(filters, match=all)


def compute_object_density(objects):
    # @todo could implement a proper scanline algorithm for this
    mask = np.zeros((512, 512), dtype=bool)
    for obj in objects:
        tlx, tly, w, h = obj.bounding_box.coords_in(img=mask)
        mask[tly:tly + h, tlx:tlx + w] = True

    return mask.sum() / mask.size


# Load data
label_map = {}
count_map = {}
density_map = {}
for label_path in label_paths:
    timestamp = panu.parse_timestamp_from_path(label_path)
    image_labels = etai.ImageLabels.from_json(label_path)
    objects = image_labels.objects

    objects = filter_objects(objects)

    label_map[timestamp] = image_labels

    count_map[timestamp] = len(objects)
    density_map[timestamp] = compute_object_density(objects)


if MIN_DATE:
    label_map = {k: v for k, v in label_map.items() if k > MIN_DATE}
    count_map = {k: v for k, v in count_map.items() if k > MIN_DATE}
    density_map = {k: v for k, v in density_map.items() if k > MIN_DATE}

# Extract timeseries
cdates = mpl.dates.date2num(list(count_map.keys()))
ddates = mpl.dates.date2num(list(density_map.keys()))
counts = np.asarray(list(count_map.values()))
densities = np.asarray(list(density_map.values()))


#
# Apply smoothing
#

window_size = 30
smoothing_size = 30

top = 0.1
p = 2

avg_fcn = lambda x: np.linalg.norm(x, ord=p) / (len(x) ** (1 / p))
#avg_fcn = np.mean
#avg_fcn = np.median


def apply_top_smoothing(values, window_size, top, avg_fcn):
    num_values = len(values)
    num_top = int(window_size * top)

    smoothed_values = []
    for idx in range(1, num_values + 1):
        window = values[max(0, idx - window_size):idx]
        top_window = sorted(window)[-num_top:]
        smoothed_values.append(avg_fcn(top_window))

    return np.asarray(smoothed_values)


def apply_moving_average(values, window_size):
    kernel = np.ones(window_size) / window_size
    return sps.convolve(values, kernel, mode="same")


def apply_moving_median(values, window_size):
    return sps.medfilt(values, kernel_size=window_size)


smooth_counts = apply_top_smoothing(counts, window_size, top=top, avg_fcn=avg_fcn)
smooth_densities = apply_top_smoothing(densities, window_size, top=top, avg_fcn=avg_fcn)

smooth_counts = apply_moving_average(smooth_counts, smoothing_size)
smooth_densities = apply_moving_average(smooth_densities, smoothing_size)

#smooth_counts = apply_moving_median(counts, window_size)
#smooth_densities = apply_moving_median(densities, window_size)

#
# Plot results
#

plt.cla()

plt.subplot(121)
plt.plot_date(cdates, counts, "bo")
plt.plot_date(cdates, smooth_counts, "r-")
plt.title("object count")

plt.subplot(122)
plt.plot_date(ddates, densities, "bo")
plt.plot_date(ddates, smooth_densities, "r-")
plt.title("object density")

plt.show()
