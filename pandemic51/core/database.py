'''
Database interaction.

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
from collections import defaultdict
from datetime import datetime, timedelta
import os

import numpy as np
import pymysql

import eta.core.utils as etau

import pandemic51.core.config as p51c


def connect_database():
    return pymysql.connect(
        user=p51c.P51_SQL_USERNAME,
        password=p51c.P51_SQL_PASSWORD,
        host=p51c.SQL_HOST,
        db=p51c.P51_SQL_DATABASE_NAME
    )


def with_connection(func):
    '''Decorator that creates a database connection and closes it upon call
    completion if a connection is not provided by the function.

    Expects the function to take `*args` and `cnx` like this:
        @with_connection
        def your_function(..., *args, cnx):
            ...
    '''
    def wrapper(*args, cnx=None, **kwargs):
        close = False
        if not cnx:
            cnx = connect_database()
            close = True

        result = func(*args, cnx=cnx, **kwargs)

        if close:
            cnx.close()

        return result

    return wrapper


@with_connection
def add_stream_history(
        stream_name, dt, image_path, labels_path=None, *args, cnx):
    '''

    Args:
        stream_name: name of the video source stream
        dt: datetime object of when the image was captured
        image_path: path to the image file on disk
        labels_path: path to the labels file on disk
    '''
    with cnx.cursor() as cursor:
        image_path = os.path.abspath(image_path)

        formatted_timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')

        if labels_path is not None:
            sql = '''
                INSERT INTO stream_history(stream_name, datetime, data_path, labels_path)
                VALUES('{}', '{}', '{}', '{}');
                '''.format(
                stream_name, formatted_timestamp, image_path, labels_path)
        else:
            sql = '''
                INSERT INTO stream_history(stream_name, datetime, data_path)
                VALUES('{}', '{}', '{}');
                '''.format(stream_name, formatted_timestamp, image_path)

        cursor.execute(sql)

    cnx.commit()


@with_connection
def query_unprocessed_images(*args, cnx):
    '''Get all columns of `stream_history` where `labels_path` is unpopulated.

    Returns:
        a tuple of (id, data_path) tuples
    '''
    with cnx.cursor() as cursor:
        sql = '''
        select id, data_path from stream_history where labels_path is NULL;
        '''
        cursor.execute(sql)
        result = cursor.fetchall()

    return list(result)


@with_connection
def add_stream_labels(id, labels_path, *args, cnx):
    with cnx.cursor() as cursor:
        sql = '''
        UPDATE stream_history SET labels_path='{}' where id={};
        '''.format(labels_path, id)
        cursor.execute(sql)

    cnx.commit()


@with_connection
def query_stream_history(stream_name=None, reformat_as_dict=False, cnx=None):
    '''Returns the stream history for the specified stream(s).

    Args:
        stream_name: the stream name to query. By default, all streams are
            returned
        reformat_as_dict: whether or not to reformat the query result as a
            dictionary keyed on `stream_name`
        cnx: a connection to the database, if one is already made

    Returns:
        if NOT reformat_as_dict:
            a tuple of row tuples of the database table `stream_history`:
                (id, stream_name, datetime, data_path, labels_path, sdi)
        if reformat_as_dict:
            a dictionary of format:
                {
                    "<STREAM 1 NAME>": {
                        "id": [list, of, SQL, row, IDs],
                        "datetime": [list, of, datetime, objects],
                        "data_path": [...],
                        "labels_path": [...],
                        "sdi": [list, of, sdi, floats]
                    },
                    "<STREAM 2 NAME>": {
                        ...,
                        "datetime": [list, of, datetime, objects],
                        ...,
                        "sdi": [list, of, sdi, floats]
                    },
                    ...
                }
    '''
    with cnx.cursor() as cursor:
        stream_search = (
                " where stream_name = '%s'" % stream_name
                if stream_name else ""
        )

        sql = '''
        select id, stream_name, datetime, data_path, labels_path, sdi
        from stream_history%s ORDER BY datetime;
        ''' % stream_search
        cursor.execute(sql)
        result = cursor.fetchall()

    if not reformat_as_dict:
        return result

    # reformat the result
    result_dict = defaultdict(lambda: defaultdict(list))
    for id, stream_name, datetime, data_path, labels_path, sdi in result:
        result_dict[stream_name]["id"].append(id)
        result_dict[stream_name]["datetime"].append(datetime)
        result_dict[stream_name]["data_path"].append(data_path)
        result_dict[stream_name]["labels_path"].append(labels_path)
        result_dict[stream_name]["sdi"].append(sdi)

    return result_dict


def plot(stream_name, reformat_as_dict=False, cnx=None):
    '''
    Args:
        stream_name: if provided, only query a single stream is queried
        reformat_as_dict: whether or not to reformat the query result as a
            dictionary keyed on `stream_name`
        cnx: a connection to the database, if one is already made

    Returns:
        if NOT reformat_as_dict:
            a tuple of row tuples of the database table `stream_history`:
                (id, stream_name, datetime, data_path, labels_path, sdi)
        if reformat_as_dict:
            a dictionary of format:
                {
                    "<STREAM 1 NAME>": {
                        "id": [list, of, SQL, row, IDs],
                        "datetime": [list, of, datetime, objects],
                        "data_path": [...],
                        "labels_path": [...],
                        "sdi": [list, of, sdi, floats]
                    },
                    "<STREAM 2 NAME>": {
                        ...,
                        "datetime": [list, of, datetime, objects],
                        ...,
                        "sdi": [list, of, sdi, floats]
                    },
                    ...
                }
    '''
    with cnx.cursor() as cursor:
        stream_search = (
                " where stream_name = '%s'" % stream_name
                if stream_name else ""
        )

        sql = '''
        select unix_timestamp(datetime) as time, sdi
        from stream_history%s and sdi is not null ORDER BY datetime;
        ''' % stream_search
        cursor.execute(sql)
        result = cursor.fetchall()

    result = [(datetime.utcfromtimestamp(t), sdi) for t, sdi in result]

    MIN_DATE = etau.parse_isotime("2020-02-15")

    output_result = [{"time": t, "sdi": None} for t, sdi in result
                     if not MIN_DATE or t > MIN_DATE]

    # Number of days of data to apply avg_fcn over
    window_size = 3

    # Top % of window that will be used to average over
    top = 0.1

    # Minimum number of samples that need to be in the window in order to
    # compute sdi. This is to remove large gaps
    min_window_count = 5

    # l-p norm
    p = 2
    
    avg_fcn = lambda x: np.linalg.norm(x, ord=p) / (len(x) ** (1 / p))
    
    for ind, d in enumerate(output_result):
        time = d["time"]
        output_result[ind]["time"] = time.timestamp()
        window = [v for t, v in result
                  if t <= time and t > time - timedelta(days=window_size)]
        if len(window) < min_window_count:
            continue

        num_top = int(len(window)*top)
        top_window = sorted(window)[-num_top:] 
        new_sdi = avg_fcn(top_window)

        output_result[ind]["sdi"] = new_sdi 

    output_result = [d for d in output_result if d["sdi"]]

    return output_result


@with_connection
def populate_object_count(id, count, *args, cnx):
    with cnx.cursor() as cursor:
        sql = '''
        UPDATE stream_history SET sdi='{}' where id={};
        '''.format(count, id)
        cursor.execute(sql)

    cnx.commit()
