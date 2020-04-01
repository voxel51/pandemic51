'''
Convert database to a CSV file.

Only saves `stream_name`, `timestamp` and `count`

Copyright 2017-2020, Voxel51, Inc.
voxel51.com

Tyler Ganter, tyler@voxel51.com
'''
import pandas as pd

import pandemic51.core.database as pand


# load the database table to a DataFrame object
columns = ["id", "stream_name", "datetime", "data_path", "labels_path",
           "count"]
data = pand.query_stream_history()
df = pd.DataFrame(data, columns=columns)

# transform the datetime to an integer timestamp series
df["timestamp"] = df["datetime"].transform(lambda t: int(t.timestamp()))

# drop unwanted columns
columns_to_keep = ["stream_name", "timestamp", "count"]
df = df.drop(columns=[col for col in columns if col not in columns_to_keep])

# write to CSV
df.to_csv("counts.csv", index=False)
