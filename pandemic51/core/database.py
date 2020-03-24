'''

'''
import os

import pymysql

import pandemic51.core.config as p51c


def connect_database():
    return pymysql.connect(
        user=p51c.SQL_USERNAME_ENVVAR,
        password=os.environ.get(p51c.SQL_PASSWORD_ENVVAR),
        host=p51c.SQL_HOST,
        db=os.environ.get(p51c.SQL_DATABASE_NAME_ENVVAR)
    )


def get_stream_uuid(stream_name, cnx=None):
    close = False
    if not cnx:
        cnx = connect_database()
        close = True

    with cnx.cursor() as cursor:
        sql = "select uuid from streams where name='{}';".format(stream_name)
        cursor.execute(sql)
        result = cursor.fetchall()

    if close:
        cnx.close()

    return result[0][0] if result else None


def add_stream_history(stream_name, image_path, timestamp, cnx=None):
    close = False
    if not cnx:
        cnx = connect_database()
        close = True

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

    if close:
        cnx.close()
