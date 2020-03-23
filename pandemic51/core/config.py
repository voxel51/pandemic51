'''

'''


STREAMS = {
    "time_square": {
        "base_path": "https://d3o4twxzdiwvsf.cloudfront.net/fecnetwork/hdtimes10.flv",
        "chunk": "chunklist.m3u8"
    },
    "chicago": {
        "base_path": "https://videos-3.earthcam.com/fecnetwork/13220.flv",
        "chunk": "chunklist_w1227547844.m3u8"
    }
}

SQL_USERNAME_ENVVAR = 'P51_SQL_USERNAME'
SQL_PASSWORD_ENVVAR = 'P51_SQL_PASSWORD'
SQL_DATABASE_NAME_ENVVAR = 'P51_SQL_DATABASE_NAME'

# If running locally, use the TCP connections
# Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
# so that your application can use 127.0.0.1:3306 to connect to your
# Cloud SQL instance
SQL_HOST = '127.0.0.1'
