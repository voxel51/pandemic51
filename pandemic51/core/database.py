'''
Database interaction.

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
from collections import defaultdict
import os

import pymysql

import pandemic51.config as panc
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

    Expects the function to take `*args` and `cnx` like this:

    Example use:

        ```
        @with_connection
        def your_function(..., *args, cnx):
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
                insert into `stream_history`
                (`stream_name`, `datetime`, `data_path`, `labels_path`)
                values (%s, %s, %s, %s);
                '''
            cursor.execute(
                sql,
                (stream_name, formatted_timestamp, image_path, labels_path))
        else:
            sql = '''
                insert into `stream_history`
                (`stream_name`, `datetime`, `data_path`)
                values (%s, %s, %s);
                '''
            cursor.execute(sql, (stream_name, formatted_timestamp, image_path))

    cnx.commit()


@with_connection
def query_unprocessed_images(*args, cnx):
    '''Gets all unprocessed images, i.e., those with no `labels_path` in the
    database.

    Args:
        cnx: a db connection. By default, a temporary connection is created

    Returns:
        a tuple of (id, image path) tuples
    '''
    with cnx.cursor() as cursor:
        sql = '''
            select `id`, `data_path`, `stream_name` from `stream_history`
            where `labels_path` is null;
            '''
        cursor.execute(sql)
        result = cursor.fetchall()

    return list(result)


@with_connection
def set_object_count(id, count, *args, cnx):
    '''Sets the object count for the given ID in the database.

    Args:
        id: db row ID
        count: the object count
        cnx: a db connection. By default, a temporary connection is created
    '''
    with cnx.cursor() as cursor:
        sql = "update `stream_history` set `count`=%s where `id`=%s;"
        cursor.execute(sql, (count, id))

    cnx.commit()


@with_connection
def add_stream_labels(id, labels_path, *args, cnx):
    '''Adds the given labels to the database.

    Args:
        id: db row ID
        labels_path: the path to the labels
        cnx: a db connection. By default, a temporary connection is created
    '''
    with cnx.cursor() as cursor:
        sql = "update `stream_history` set `labels_path`=%s where id=%s;"
        cursor.execute(sql, (labels_path, id))

    cnx.commit()


@with_connection
def add_stream_anno_img(id, anno_img_path, *args, cnx):
    '''Adds the annotation image path to the database.

    Args:
        id: db row ID
        anno_img_path: the path to the annotated image
        cnx: a db connection. By default, a temporary connection is created
    '''
    with cnx.cursor() as cursor:
        sql = "update `stream_history` set `anno_img_path`=%s where `id`=%s;"
        cursor.execute(sql, (anno_img_path, id))

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
        if `reformat_as_dict == False`:
            (
                (
                    id, stream_name, datetime, data_path,
                    labels_path, count, anno_img_path
                ),
                ...
            )

        if `reformat_as_dict == True`:
            {
                "<stream-name>": {
                    "id": [...],
                    "datetime": [...],
                    "data_path": [...],
                    "labels_path": [...],
                    "count": [...],
                    "anno_img_path": [...],
                },
                ...
            }
    '''
    with cnx.cursor() as cursor:
        if stream_name:
            stream_search = " where `stream_name`=%s"
            args = stream_name
        else:
            stream_search = ""
            args = None

        sql = '''
            select `id`, `stream_name`, `datetime`, `data_path`, `labels_path`,
            `count`, `anno_img_path`
            from `stream_history`%s order by `datetime`;
            ''' % stream_search
        cursor.execute(sql, args)
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
        result_dict[stream_name]["anno_img_path"].append(count)

    return result_dict


@with_connection
def query_stream_pdi(stream_name, *args, cnx):
    '''Returns a time-series of PDI values for the given stream.

    Args:
        stream_name: the stream name
        cnx: a db connection. By default, a temporary connection is created

    Returns:
        [
            {
                "time": time,
                "pdi": pdi,
                "url": url,
            },
            ...
        ]
    '''
    with cnx.cursor() as cursor:
        sql = '''
            select unix_timestamp(`datetime`), `count`, `anno_img_path`
            from `stream_history`
            where `stream_name`=%s
            and `count` is not null
            and `anno_img_path` is not null
            order by `datetime`;
            '''
        cursor.execute(sql, stream_name)
        result = cursor.fetchall()

    times, counts, urls = zip(*result)
    times, pdis, urls = panp.compute_pdi(times, counts, urls)

    return [{"time": t, "pdi": p, "url": u}
            for t, p, u in zip(times, pdis, urls)]


@with_connection
def query_all_pdi(*args, cnx):
    '''Returns the PDI values for all available streams.

    Args:
        cnx: a db connection. By default, a temporary connection is created

    Returns:
        {
            "<stream-name>": {
                "time": [...],
                "pdi": [...],
            },
            ...
        }
    '''
    with cnx.cursor() as cursor:
        sql = '''
            select `stream_name`, unix_timestamp(`datetime`), `count`
            from `stream_history` where `count` is not null
            order by `datetime`;
            '''
        cursor.execute(sql)
        result = cursor.fetchall()

    data = defaultdict(lambda: defaultdict(list))
    for stream_name, time, count in result:
        data[stream_name]["time"].append(time)
        data[stream_name]["count"].append(count)

    all_pdis = {}
    for stream_name, d in data.items():
        times, pdis = panp.compute_pdi(d["time"], d["count"])
        all_pdis[stream_name] = {"time": times, "pdi": pdis}

    return all_pdis


@with_connection
def query_snapshots(*args, cnx):
    '''Returns a snapshot of the current streams.

    Args:
        cnx: a db connection. By default, a temporary connection is created

    Returns:
        [
            {
                "stream_name": s,
                "time": t,
                "url": u,
            },
            ...
        ]
    '''
    with cnx.cursor() as cursor:
        sql = '''
            select `stream_name`, unix_timestamp(`datetime`), url from (
                select s.stream_name, s.datetime, s.anno_img_path url
                from `stream_history` s
                inner join (
                    select `stream_name`, max(`datetime`) t
                    from `stream_history` where `anno_img_path` is not null
                    group by `stream_name`
                ) i on s.stream_name = i.stream_name and s.datetime = i.t
            ) r;
            '''
        cursor.execute(sql)
        result = cursor.fetchall()

    return [{"stream_name": s, "time": t, "url": u} for s, t, u in result]
