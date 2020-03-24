'''
Celery Tasks

'''
import celery

import pandemic51.core.config as p51c


app = celery.Celery("pandemic51.tasks")
app.config_from_object("pandemic51.core.celery_config")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    # sender.add_periodic_task(
    #     pcfg.STREAM_DOWNLOAD_INTERVAL,
    #     test.s('hello'))

    sender.add_periodic_task(
        p51c.STREAM_DOWNLOAD_INTERVAL, poll_stream.s("time_square"))
    sender.add_periodic_task(
        p51c.STREAM_DOWNLOAD_INTERVAL, poll_stream.s("chicago"))


@app.task
def test(arg):
    print(arg)


@app.task
def poll_stream(stream_name):
    import os
    from pandemic51.core.streaming import download_and_store

    print("~" * 40)
    print(stream_name)
    print("~" * 40)

    out_dir = os.environ.get("IMAGE_DIR")

    download_and_store(stream_name, out_dir=out_dir)
