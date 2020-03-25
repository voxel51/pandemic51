'''
Test script for plotting person density vs time.

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
# pragma pylint: disable=redefined-builtin
# pragma pylint: disable=unused-wildcard-import
# pragma pylint: disable=wildcard-import
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import *
# pragma pylint: enable=redefined-builtin
# pragma pylint: enable=unused-wildcard-import
# pragma pylint: enable=wildcard-import

import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal as sps

import eta.core.image as etai
import eta.core.utils as etau

import pandemic51.core.density as pand


stream = "timesquare"
LABELS_DIR = os.path.join("out", stream, "labels")
CONFIDENCE_THRESH = 0.15


# Input images to process
label_paths = etau.list_files(LABELS_DIR, abs_paths=True)


def parse_timestamp_from_path(path):
    # Example input: "2020-03-21_1584781705273_48_09:08:25"
    s = os.path.splitext(os.path.basename(path))[0]
    return etau.parse_isotime(s[:10] + " " + s[-8:])


# Load data
label_map = {}
count_map = {}
density_map = {}
for label_path in label_paths:
    timestamp = parse_timestamp_from_path(label_path)
    image_labels = etai.ImageLabels.from_json(label_path)
    objects = image_labels.objects

    # Filter by confidence
    objects.filter_elements([lambda obj: obj.confidence > CONFIDENCE_THRESH])

    label_map[timestamp] = image_labels

    count_map[timestamp] = len(objects)
    density_map[timestamp] = pand.compute_object_density(objects)


# Extract timeseries
cdates = mpl.dates.date2num(list(count_map.keys()))
ddates = mpl.dates.date2num(list(density_map.keys()))
counts = np.asarray(list(count_map.values()))
densities = np.asarray(list(density_map.values()))


# Apply smoothing
kernel_size = 29

'''
# Moving average
kernel = np.ones(kernel_size) / kernel_size
smooth_counts = sps.convolve(counts, kernel, mode="same")
smooth_densities = sps.convolve(densities, kernel, mode="same")
'''

# Windowed-median
smooth_counts = sps.medfilt(counts, kernel_size=kernel_size)
smooth_densities = sps.medfilt(densities, kernel_size=kernel_size)


#
# Plot results
#

plt.subplot(121)
plt.plot_date(cdates, counts, "bo")
plt.plot_date(cdates, smooth_counts, "r-")
plt.title("person count")

plt.subplot(122)
plt.plot_date(ddates, densities, "bo")
plt.plot_date(ddates, smooth_densities, "r-")
plt.title("person density (frame coverage in [0, 1])")

plt.show()
