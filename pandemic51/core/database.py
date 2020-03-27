'''
Database interaction.

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
from collections import defaultdict
import os

import pymysql

import pandemic51.core.config as panc
import pandemic51.core.pdi as panp


def connect_database():
    '''Creates a database connection.

    Returns:
        a db connection
    '''
    return pymysql.connect(
        user=panc.P51_SQL_USERNAME,
        password=panc.P51_SQL_PASSWORD,
        host=panc.SQL_HOST,
        db=panc.P51_SQL_DATABASE_NAME,
    )


def with_connection(func):
    '''Decorator that creates a database connection and closes it upon call
    completion if a connection is not provided by the function.

    Expects the function to have an optional keyword argument `cnx`.

    Example use:

        ```
        @with_connection
        def your_function(..., cnx=None, ...):
            ...
        ```
    '''
    def wrapper(*args, cnx=None, **kwargs):
        should_close = False
        if not cnx:
            cnx = connect_database()
            should_close = True

        result = func(*args, cnx=cnx, **kwargs)

        if should_close:
            cnx.close()

        return result

    return wrapper


@with_connection
def add_stream_history(
        stream_name, dt, image_path, labels_path=None, cnx=None):
    '''Adds the given stream history to the database.

    Args:
        stream_name: name of the video source stream
        dt: datetime object of when the image was captured
        image_path: path to the image file on disk
        labels_path: optional path to the labels file on disk
        cnx: a db connection. By default, a temporary connection is created
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
def query_unprocessed_images(cnx=None):
    '''Get all columns of `stream_history` where `labels_path` is unpopulated.

    Args:
        cnx: a db connection. By default, a temporary connection is created

    Returns:
        a tuple of (id, labels_path) tuples
    '''
    with cnx.cursor() as cursor:
        sql = '''
        select id, data_path from stream_history where labels_path is NULL;
        '''
        cursor.execute(sql)
        result = cursor.fetchall()

    return list(result)


@with_connection
def add_stream_labels(id, labels_path, cnx=None):
    '''Adds the labels for the given stream to the DB.

    Args:
        id: the stream ID
        labels_path: the path to the labels
        cnx: a db connection. By default, a temporary connection is created
    '''
    with cnx.cursor() as cursor:
        sql = '''
        UPDATE stream_history SET labels_path='{}' where id={};
        '''.format(labels_path, id)
        cursor.execute(sql)

    cnx.commit()


@with_connection
def add_stream_anno_img(id, anno_img_path, *args, cnx):
    with cnx.cursor() as cursor:
        sql = '''
        UPDATE stream_history SET anno_img_path='{}' where id={};
        '''.format(anno_img_path, id)
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
        cnx: a db connection. By default, a temporary connection is created

    Returns:
        if NOT reformat_as_dict:
            a tuple of row tuples of the database table `stream_history`:
                (id, stream_name, datetime, data_path, labels_path, count)
        if reformat_as_dict:
            a dictionary of format:
                {
                    "<STREAM NAME>": {
                        "id": [list, of, SQL, row, IDs],
                        "datetime": [...],
                        "data_path": [...],
                        "labels_path": [...],
                        "count": [...],
                    },
                    ...
                }
    '''
    with cnx.cursor() as cursor:
        if stream_name:
            stream_search = " where stream_name = '%s'" % stream_name
        else:
            stream_search = ""

        sql = '''
        select id, stream_name, datetime, data_path, labels_path, sdi
        from stream_history%s ORDER BY datetime;
        ''' % stream_search
        cursor.execute(sql)
        result = cursor.fetchall()

    if not reformat_as_dict:
        return result

    # Reformat result as a dictionary
    result_dict = defaultdict(lambda: defaultdict(list))
    for id, stream_name, datetime, data_path, labels_path, count in result:
        result_dict[stream_name]["id"].append(id)
        result_dict[stream_name]["datetime"].append(datetime)
        result_dict[stream_name]["data_path"].append(data_path)
        result_dict[stream_name]["labels_path"].append(labels_path)
        result_dict[stream_name]["count"].append(count)

    return result_dict


@with_connection
def query_stream_sdi(stream_name, *args, cnx=None):
    '''Returns a time-series of SDI values for the given stream.

    Args:
        stream_name: the stream name
        cnx: a db connection. By default, a temporary connection is created

    Returns:
        a list of {"time": timestamp, "pdi": <physical distance index>} values
    '''
    with cnx.cursor() as cursor:
        sql = '''
        select unix_timestamp(datetime) as time, sdi
        from stream_history where stream_name = '%s' and sdi is not null ORDER BY datetime;
        ''' % stream_name
        cursor.execute(sql)
        result = cursor.fetchall()

    times, counts = zip(*result)
    pdis = panp.compute_pdi(times, counts)

    return [{"time": t, "pdi": p} for t, p in zip(times, pdis)]


@with_connection
def populate_object_count(id, count, cnx=None):
    '''Sets the object count for the given ID in the database.

    Args:
        id: the stream ID
        count: the object count
        cnx: a db connection. By default, a temporary connection is created
    '''
    with cnx.cursor() as cursor:
        sql = '''
        UPDATE stream_history SET sdi='{}' where id={};
        '''.format(count, id)
        cursor.execute(sql)

    cnx.commit()
