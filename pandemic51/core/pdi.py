'''
Methods for computing physical distancing index (PDI).

Copyright 2020, Voxel51, Inc.
voxel51.com
'''
from datetime import datetime, timedelta

import numpy as np


WINDOW_DAYS = 2
LP = 2
SMOOTHING_WIDTH = 40


def compute_pdi(timestamps, counts, urls):
    '''Computes the physical distancing indexes (PDIs) for the given data.

    Args:
        timestamps: a list of timestamps
        counts: a list of object counts
        urls: a list of annotated image URLs

    Returns:
        (timestamps, PDIs, urls)
    '''
    times = np.asarray([datetime.utcfromtimestamp(t) for t in timestamps])
    counts = np.asarray(counts)

    avg_fcn = lambda x: np.linalg.norm(x, ord=LP) / (len(x) ** (1 / LP))

    pdis = []
    for time in times:
        start_time = time - timedelta(days=WINDOW_DAYS)
        window_counts = counts[(start_time <= times) & (times <= time)]
        pdi = avg_fcn(window_counts)
        pdis.append(pdi)

    if SMOOTHING_WIDTH:
        kernel = np.ones(SMOOTHING_WIDTH) / SMOOTHING_WIDTH
        pdis = list(np.convolve(pdis, kernel, mode="same"))

    # Omit startup values
    startup_time = times[0] + timedelta(days=WINDOW_DAYS)
    skip = np.argwhere(times > startup_time)[0, 0]

    return timestamps[skip::], pdis[skip::], urls[skip::]


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

    times = np.asarray([datetime.utcfromtimestamp(t) for t in timestamps])

    old_time = times[-1] - timedelta(days=num_days)
    old_idx = np.argmin(np.abs(times - old_time))

    return pdis[-1] - pdis[old_idx]
