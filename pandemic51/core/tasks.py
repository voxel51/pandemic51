'''
Celery Tasks

'''
import os

import celery

import pandemic51.core.config as panc
from pandemic51.core.density import compute_density_for_unprocessed_images
from pandemic51.core.streaming import download_and_store


app = celery.Celery("pandemic51.core.tasks")
app.config_from_object("pandemic51.core.celery_config")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    for stream_name in panc.STREAMS:
        sender.add_periodic_task(
            panc.STREAM_DOWNLOAD_INTERVAL, das_task.s(stream_name))
        # sender.add_periodic_task(panc.DENSITY_COMPUTE_INTERVAL, cdfui_task.s())


@app.task(name="task.das_task")
def das_task(stream_name):
    '''"Download And Store (DAS) task'''
    tmpdirbase = os.path.join(panc.DATA_DIR, "tmp")
    download_and_store(
        stream_name, out_dir=panc.IMAGE_DIR, tmpdirbase=tmpdirbase)


@app.task(name="task.cdfui_task")
def cdfui_task():
    '''"Compute Density For Unprocessed Images (CDFUI) task'''
    # compute_density_for_unprocessed_images()

    print("~" * 40)
    print("IMPORTING")
    import pandemic51.detectors.efficientdet as efficientdet
    print("~" * 40)
    print(efficientdet)
    print("~" * 40)
