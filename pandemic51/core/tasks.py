'''
Celery tasks.

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
import celery

import pandemic51.config as panc
import pandemic51.core.detections as pand
import pandemic51.core.streaming as pans


app = celery.Celery("pandemic51.core.tasks")
app.config_from_object("pandemic51.celery_config")


@celery.signals.celeryd_init.connect()
def run_on_startup(sender=None, conf=None, **kwargs):
    '''Execute these tasks on startup, either as one time or very infrequent
    tasks that should run after system comes online.
    '''
    compute_detections_task.delay()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    '''Setup periodic Celery tasks.'''
    for stream_name in panc.STREAMS:
        sender.add_periodic_task(
            panc.DOWNLOAD_STREAM_INTERVAL, download_stream_task.s(stream_name))

    sender.add_periodic_task(
        panc.COMPUTE_DETECTIONS_INTERVAL, compute_detections_task.s())


@app.task(time_limit=60*5)
def download_stream_task(stream_name):
    '''Downloads and stores images for the given stream.

    Args:
        stream_name: the stream name
    '''
    pans.download_and_store(stream_name, outdir=panc.IMAGES_DIR)


@app.task()
def compute_detections_task():
    '''Computes detections for all new images.'''
    pand.detect_objects_in_unprocessed_images()
