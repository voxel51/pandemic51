'''

'''
import os

import eta.core.serial as etas

streams_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "STREAMS.json")
STREAMS = etas.load_json(streams_path)


SQL_USERNAME_ENVVAR = 'P51_SQL_USERNAME'
SQL_PASSWORD_ENVVAR = 'P51_SQL_PASSWORD'
SQL_DATABASE_NAME_ENVVAR = 'P51_SQL_DATABASE_NAME'

# If running locally, use the TCP connections
# Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
# so that your application can use 127.0.0.1:3306 to connect to your
# Cloud SQL instance
SQL_HOST = '127.0.0.1'
