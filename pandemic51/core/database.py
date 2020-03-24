'''

'''
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
def get_stream_uuid(stream_name, *args, cnx):
    with cnx.cursor() as cursor:
        sql = "select uuid from streams where name='{}';".format(stream_name)
        cursor.execute(sql)
        result = cursor.fetchall()

    return result[0][0] if result else None


@with_connection
def add_stream_history(stream_name, image_path, timestamp, *args, cnx):
    stream_uuid = get_stream_uuid(stream_name, cnx=cnx)

    with cnx.cursor() as cursor:
        image_path = os.path.abspath(image_path)

        formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        sql = '''
        INSERT INTO stream_history(stream_uuid, datetime, data_path)
        VALUES('{}', '{}', '{}');
        '''.format(stream_uuid, formatted_timestamp, image_path)

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

    return result


@with_connection
def add_stream_labels(id, labels_path, *args, cnx):
    with cnx.cursor() as cursor:
        sql = '''
        UPDATE stream_history SET labels_path='{}' where id={};
        '''.format(labels_path, id)
        cursor.execute(sql)

    cnx.commit()
