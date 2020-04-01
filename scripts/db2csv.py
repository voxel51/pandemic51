'''
Convert database to a CSV file.

Only reads `stream_name`, `datetime` and `count`

Copyright 2017-2020, Voxel51, Inc.
voxel51.com

Tyler Ganter, tyler@voxel51.com
'''
import pandas as pd

import pandemic51.core.database as pand


if __name__ == "__main__":
    columns = [
        "id", "stream_name", "datetime", "data_path", "labels_path", "count"]
    data = pand.query_stream_history()
    df = pd.DataFrame(data, columns=columns)

    columns_to_keep = ["stream_name", "datetime", "count"]

    df = df.drop(columns=[col for col in columns if col not in columns_to_keep])

    print(df.head())
    print(df.tail())
