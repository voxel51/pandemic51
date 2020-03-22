'''

'''
import os

import pymysql


class DatabaseConnection(object):

    def __init__(self):
        self._db_user = os.environ.get('P51_SQL_USERNAME')
        self._db_password = os.environ.get('P51_SQL_PASSWORD')
        self._db_name = os.environ.get('P51_SQL_DATABASE_NAME')

        # If running locally, use the TCP connections
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        self._host = '127.0.0.1'

    def __enter__(self):
        self.cnx = pymysql.connect(
            user=self._db_user,
            password=self._db_password,
            host=self._host,
            db=self._db_name
        )

        return self

    def __exit__(self, *args):
        self.cnx.close()

    @property
    def cursor(self):
        return self.cnx.cursor


def get_time_from_db():
    # with get_sql_connection() as cnx:

    with DatabaseConnection() as dbconn:
        with dbconn.cursor() as cursor:
            cursor.execute('SELECT NOW() as now;')
            result = cursor.fetchall()
            current_time = result[0][0]

    return current_time

def add_snapshot(timestamp, img_path):
    pass


if __name__ == '__main__':
    t = get_time_from_db()

    print(t)

    '''
    PARAMS
    - list streams
    - specify sampling interval
    - specify initial time
    '''

    '''
    CODE
    - get all "desired" timestamps
    - get images for all of these (that are missing)
    '''

    '''
    CELERY TASKS
    1) download streams and convert to images and save
    2) process images and store preds (and SDI) to database
    '''



