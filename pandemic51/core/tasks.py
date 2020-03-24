'''
Celery Tasks

'''
import celery

import pandemic51.core.config as p51c
from pandemic51.core.streaming import download_and_store


app = celery.Celery("pandemic51.tasks")
app.config_from_object("pandemic51.core.celery_config")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    for stream_name in p51c.STREAMS:
        sender.add_periodic_task(
            p51c.STREAM_DOWNLOAD_INTERVAL, das_task.s(stream_name))


@app.task
def das_task(stream_name):
    '''"Download And Store (DAS) task'''
    download_and_store(stream_name, out_dir=p51c.IMAGE_DIR)
