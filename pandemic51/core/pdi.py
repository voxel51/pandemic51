'''
Methods for computing physical distancing index (PDI).

Copyright 2017-2020, Voxel51, Inc.
voxel51.com
'''
from datetime import datetime, timedelta

import numpy as np


WINDOW_DAYS = 3
TOP = 0.1
LP = 2
SMOOTHING_WIDTH = 30

V2_LP = 2
V2_WINDOW_SAMPLES = 100

N_HOURS = 24 * 7


def _compute_pdi_v1(timestamps, counts, urls):
    '''Computes the physical distancing indexes (PDIs) for the given
    time-series data.

    Args:
        timestamps: a list of timestamps
        counts: a list of object counts

    Returns:
        the list of PDI values
    '''
    times = np.asarray([datetime.utcfromtimestamp(t) for t in timestamps])
    counts = np.asarray(counts)

    avg_fcn = lambda x: np.linalg.norm(x, ord=LP) / (len(x) ** (1 / LP))

    pdis = []
    for time in times:
        start_time = time - timedelta(days=WINDOW_DAYS)
        window_counts = counts[(start_time <= times) & (times <= time)]

        num_top = int(TOP * len(window_counts))
        top_window_counts = sorted(window_counts)[-num_top:]
        pdi = avg_fcn(top_window_counts)

        pdis.append(pdi)

    if SMOOTHING_WIDTH:
        kernel = np.ones(SMOOTHING_WIDTH) / SMOOTHING_WIDTH
        pdis = list(np.convolve(pdis, kernel, mode="same"))

    return timestamps, pdis, urls


def _compute_pdi_v2(timestamps, counts, urls):
    counts = np.asarray(counts)

    avg_fcn = lambda x: np.linalg.norm(x, ord=V2_LP) / (len(x) ** (1 / V2_LP))

    pdis = np.zeros(counts.shape)
    for n in range(len(pdis)):
        pdis[n] = avg_fcn(counts[max(0, n-V2_WINDOW_SAMPLES):n+1])

    if SMOOTHING_WIDTH:
        kernel = np.ones(SMOOTHING_WIDTH) / SMOOTHING_WIDTH
        pdis = list(np.convolve(pdis, kernel, mode="same"))

    # startup time
    skip = int(V2_WINDOW_SAMPLES / 2)

    return timestamps[skip::], pdis[skip::], urls[skip::]


compute_pdi = _compute_pdi_v2


def market_change(timestamps, pdis):
    '''Change in PDI over time

    Args:
        timestamps, pdis: outputs from `compute_pdi`

    Returns:
        the change in pdi over the past N_HOURS.

    '''
    idx_now = -1
    target_time = timestamps[idx_now] - 60 * 60 * 24 * N_HOURS
    idx_prev = int(np.argwhere(np.array(timestamps) > target_time)[0])

    return pdis[idx_now] - pdis[idx_prev]
