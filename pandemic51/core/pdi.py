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


def compute_pdi(times, counts):
    '''Computes the physical distancing indexes (PDIs) for the given
    time-series data.

    Args:
        times: a list of timestamps
        counts: a list of object counts

    Returns:
        the list of PDI values
    '''
    times = np.asarray([datetime.utcfromtimestamp(t) for t in times])
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

    return pdis
