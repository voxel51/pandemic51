'''Utility Functions


Copyright 2017-2020, Voxel51, Inc.
voxel51.com

Tyler Ganter, tyler@voxel51.com
'''
import os

import eta.core.utils as etau


def parse_timestamp_from_path(path):
    # Example input: "2020-03-21_1584781705273_48_09:08:25.png"
    s = os.path.splitext(os.path.basename(path))[0]
    return etau.parse_isotime(s[:10] + " " + s[-8:])

def parse_epoch_timestamp_from_path(path):
    # Example input: "2020-03-21_1584781705273_48_09:08:25.png"
    s = os.path.splitext(os.path.basename(path))[0]
    return int(s[11:24])
