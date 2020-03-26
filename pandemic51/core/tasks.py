'''
Celery tasks.

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
import os

import celery

import pandemic51.core.config as panc
import pandemic51.core.density as pand
import pandemic51.core.streaming as pans


app = celery.Celery("pandemic51.core.tasks")
app.config_from_object("pandemic51.core.celery_config")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    for stream_name in panc.STREAMS:
        sender.add_periodic_task(
            panc.STREAM_DOWNLOAD_INTERVAL, das_task.s(stream_name))
        sender.add_periodic_task(panc.DENSITY_COMPUTE_INTERVAL, dofui_task.s())
        sender.add_periodic_task(panc.DENSITY_COMPUTE_INTERVAL, ccfde_task.s())


@app.task()
def das_task(stream_name):
    '''"Task for downloading and storing images.'''
    tmpdirbase = os.path.join(panc.DATA_DIR, "tmp")
    pans.download_and_store(
        stream_name, out_dir=panc.IMAGES_DIR, tmpdirbase=tmpdirbase)


@app.task()
def dofui_task():
    '''"Task for detecting objects for all unprocessed images.'''
    pand.detect_objects_in_unprocessed_images()


@app.task()
def ccfde_task():
    '''Task for computing object counts for all non-null DB entries.'''
    pand.compute_object_counts_for_db_entries()
