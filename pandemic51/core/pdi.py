'''
Methods for computing physical distancing index (PDI).

Copyright 2020, Voxel51, Inc.
voxel51.com
'''
from datetime import datetime, timedelta
import dateutil.parser

import numpy as np
import scipy.interpolate as spi


WINDOW_DAYS = 2
LP = 2
SMOOTHING_WIDTH = 40

ALL_GRAPH_START_DATE = dateutil.parser.parse("2020-02-01")


def compute_pdi(timestamps, counts, *args):
    '''Computes the physical distancing indexes (PDIs) for the given data.

    The input series may be truncated if necessary to produce valid PDIs.

    Args:
        timestamps: a list of timestamps
        counts: a list of object counts
        *args: optional additional lists to truncate to match the other outputs

    Returns:
        (timestamps, PDIs, *args)
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
        kernel_size = min(SMOOTHING_WIDTH, len(pdis))
        kernel = np.ones(kernel_size) / kernel_size
        pdis = list(np.convolve(pdis, kernel, mode="same"))

    # Omit startup values
    startup_time = times[0] + timedelta(days=WINDOW_DAYS)
    indices = np.argwhere(times > startup_time)
    skip = indices[0, 0] if indices.size != 0 else 0

    return (timestamps[skip::], pdis[skip::]) + tuple(a[skip::] for a in args)


def normalize_pdi_values(pdi):
    '''Normalizes the given PDI values by scaling them to a max of 1.

    Args:
        pdi: a list of PDI values

    Returns:
        a list of normalized PDI values in [0, 1]
    '''
    return list(np.asarray(pdi) / max(pdi))


def resample_pdis(pdis_map, num_samples=150, start_date=ALL_GRAPH_START_DATE):
    '''Resamples the given PDI time series to uniformly spaced time intervals,
    using linear interpolation to impute values as necessary.

    Missing data are filled with `None`s.

    Args:
        pdi_map: a dict mapping keys to {"time": [...], "pdi": [...]} dicts
        num_samples: the number of uniformly spaced samples to take
        start_date: a datetime specifying the start date for sampling

    Returns:
        [
            {
                "time": <timestamp>,
                "<key1>": <pdi>,
                "<key2>": <pdi>,
                ...
            },
            ...
        ]
    '''
    start_timestamp = int(start_date.timestamp())
    stop_timestamp = int(max(max(d["time"]) for d in pdis_map.values()))

    timestamps = np.linspace(
        start_timestamp, stop_timestamp, num=num_samples, dtype=int)

    samples = [{"time": t} for t in timestamps]
    for key, data in pdis_map.items():
        f = spi.interp1d(
            data["time"], data["pdi"], kind="linear", bounds_error=False,
            fill_value=-1)
        for sample, pdi in zip(samples, f(timestamps)):
            sample[key] = pdi if pdi >= 0 else None

    return samples


def compute_pdi_change(timestamps, pdis, num_days=7):
    '''Computes change in PDI, both over the given number of days and since the
    all-time maximum.

    The return values are expressed as relative changes, where
    postive = increase and negative = decrease. Multiply by 100 to get
    percentages.

    Args:
        timestamps: a list of timestamps
        pdis: a list of PDI values
        num_days: the number of days over which to compute the PDI change. By
            default, this is 7 days

    Returns:
        (num_days_change, max_change)
    '''
    if not timestamps:
        return 0.0, 0.0

    times = np.asarray([datetime.utcfromtimestamp(t) for t in timestamps])

    current_pdi = pdis[-1]
    max_pdi = max(pdis)

    old_time = times[-1] - timedelta(days=num_days)
    old_pdi = pdis[np.argmin(np.abs(times - old_time))]

    num_days_change = (current_pdi - old_pdi) / old_pdi
    max_change = (current_pdi - max_pdi) / max_pdi

    return num_days_change, max_change
