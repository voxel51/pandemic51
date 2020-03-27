'''
Methods for computing physical distancing index (PDI).

Copyright 2020, Voxel51, Inc.
voxel51.com
'''
from datetime import datetime, timedelta

import numpy as np


V1_WINDOW_DAYS = 2
V1_LP = 2
V1_SMOOTHING_WIDTH = 40

V2_LP = 2
V2_WINDOW_SAMPLES = 100
V2_SMOOTHING_WIDTH = 30


def compute_pdi(timestamps, counts, urls):
    '''Computes the physical distancing indexes (PDIs) for the given data.

    Args:
        timestamps: a list of timestamps
        counts: a list of object counts
        urls: a list of annotated image URLs

    Returns:
        (timestamps, PDIs, urls)
    '''
    return _compute_pdi_v2(timestamps, counts, urls)


def compute_pdi_change(timestamps, pdis, num_days=7):
    '''Computes change in PDI over the given number of days.

    Args:
        timestamps: a list of timestamps
        pdis: a list of PDI values
        num_days: the number of days over which to compute the PDI change. By
            default, this is 7 days

    Returns:
        the change in PDI (postive = increase, negative = decrease)
    '''
    if not timestamps:
        return 0.0

    target_time = timestamps[-1] - 60 * 60 * 24 * 24 * num_days
    idx_prev = int(np.argwhere(np.array(timestamps) > target_time)[0])
    return pdis[-1] - pdis[idx_prev]


def _compute_pdi_v1(timestamps, counts, urls):
    times = np.asarray([datetime.utcfromtimestamp(t) for t in timestamps])
    counts = np.asarray(counts)

    avg_fcn = lambda x: np.linalg.norm(x, ord=V1_LP) / (
                len(x) ** (1 / V1_LP))

    pdis = []
    for time in times:
        start_time = time - timedelta(days=V1_WINDOW_DAYS)
        window_counts = counts[(start_time <= times) & (times <= time)]
        pdi = avg_fcn(window_counts)
        pdis.append(pdi)

    if V1_SMOOTHING_WIDTH:
        kernel = np.ones(V1_SMOOTHING_WIDTH) / V1_SMOOTHING_WIDTH
        pdis = list(np.convolve(pdis, kernel, mode="same"))

    # skip start up values
    skip = int(np.argwhere(
        times > times[0] + timedelta(days=V1_WINDOW_DAYS))[0])

    return timestamps[skip::], pdis[skip::], urls[skip::]


def _compute_pdi_v2(timestamps, counts, urls):
    counts = np.asarray(counts)

    avg_fcn = lambda x: np.linalg.norm(x, ord=V2_LP) / (len(x) ** (1 / V2_LP))

    pdis = np.zeros(counts.shape)
    for n in range(len(pdis)):
        pdis[n] = avg_fcn(counts[max(0, n - V2_WINDOW_SAMPLES):n + 1])

    if V2_SMOOTHING_WIDTH:
        kernel = np.ones(V2_SMOOTHING_WIDTH) / V2_SMOOTHING_WIDTH
        pdis = list(np.convolve(pdis, kernel, mode="same"))

    # startup time
    skip = int(V2_WINDOW_SAMPLES / 2)

    return timestamps[skip::], pdis[skip::], urls[skip::]
