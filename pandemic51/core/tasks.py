'''
Celery Tasks

'''
import os

import celery
import tensorflow as tf

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
        sender.add_periodic_task(panc.DENSITY_COMPUTE_INTERVAL, cdfui_task.s())
        sender.add_periodic_task(panc.DENSITY_COMPUTE_INTERVAL, csfde_task.s())


@app.task()
def das_task(stream_name):
    '''"Download And Store (DAS) task'''
    tmpdirbase = os.path.join(panc.DATA_DIR, "tmp")
    pans.download_and_store(
        stream_name, out_dir=panc.IMAGE_DIR, tmpdirbase=tmpdirbase)


@app.task()
def cdfui_task():
    '''"Compute Density For Unprocessed Images (CDFUI) task'''
    # Calling this to address the following issue, which I think occurs on the
    # second call of `cdfui_task` and all later calls:
    #   ValueError: Variable efficientnet-b4/stem/conv2d/kernel already exists,
    #       disallowed. Did you mean to set reuse=True or reuse=tf.AUTO_REUSE in
    #       VarScope?
    tf.reset_default_graph()

    pand.compute_density_for_unprocessed_images()


@app.task()
def csfde_task():
    '''Compute SDI For Database Entries (CSFDE) task'''
    pand.compute_sdi_for_database_entries(
        null_only=True, sdi_metric=pand.simple_sdi)
