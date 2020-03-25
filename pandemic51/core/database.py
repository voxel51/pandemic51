'''

'''
from collections import defaultdict
import os

import pymysql

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
def add_stream_history(stream_name, image_path, dt, *args, cnx):
    '''

    Args:
        stream_name: name of the video source stream
        image_path: path to the image file on disk
        dt: datetime object of when the image was captured
    '''
    with cnx.cursor() as cursor:
        image_path = os.path.abspath(image_path)

        formatted_timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')

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
def query_sdi(stream_name=None, cnx=None):
    '''
    Args:
        stream_name:
        cnx:

    Returns:
         a dictionary of:
            key:
            value:
    '''
    with cnx.cursor() as cursor:
        stream_search = (
                " where stream_name = '%s'" % stream_name
                if stream_name else ""
        )

        sql = '''
        select stream_name, datetime, sdi from stream_history%s
         ORDER BY datetime;
        ''' % stream_search
        cursor.execute(sql)
        result = cursor.fetchall()

    result_dict = defaultdict(lambda: defaultdict(list))

    for stream_name, datetime, sdi in result:
        result_dict[stream_name]["datetime"].append(datetime)
        result_dict[stream_name]["sdi"].append(sdi)

    return result_dict
