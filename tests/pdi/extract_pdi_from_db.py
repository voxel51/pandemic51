'''
Script that extracts test PDI data from the database for a stream.

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
import eta.core.serial as etas

import pandemic51.core.database as pand


STREAM_NAME = "time_square"
OUTPATH = "test.json"


output_result = pand.query_stream_pdi(STREAM_NAME)

d = {
    "time": [a["time"] for a in output_result],
    "pdi": [a["pdi"] for a in output_result]
}

print("Writing test data to '%s'" % OUTPATH)
etas.write_json(d, OUTPATH)
