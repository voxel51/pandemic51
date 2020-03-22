'''

'''
import os

import pymysql


def get_sql_connection():
    db_user = os.environ.get('P51_SQL_USERNAME')
    db_password = os.environ.get('P51_SQL_PASSWORD')
    db_name = os.environ.get('P51_SQL_DATABASE_NAME')

    # If running locally, use the TCP connections
    # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
    # so that your application can use 127.0.0.1:3306 to connect to your
    # Cloud SQL instance
    host = '127.0.0.1'
    cnx = pymysql.connect(user=db_user, password=db_password,
                          host=host, db=db_name)

    return cnx


def get_time_from_db():
    with get_sql_connection() as cnx:
        with cnx.cursor() as cursor:
            cursor.execute('SELECT NOW() as now;')
            result = cursor.fetchall()
            current_time = result[0][0]

    return current_time