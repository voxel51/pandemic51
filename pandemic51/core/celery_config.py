'''
Celery config.

Copyright 2020, Voxel51, Inc.
voxel51.com
'''

broker_url = "pyamqp://guest@localhost//"
result_backend = "redis://"
include = ["pandemic51.core.tasks"]
