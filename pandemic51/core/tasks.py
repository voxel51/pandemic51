'''
Celery Tasks

'''
import celery

import pandemic51.core.config as pcfg

app = celery.Celery("pandemic51.tasks")
app.config_from_object("pandemic51.core.celery_config")


@celery.signals.celeryd_init.connect()
def run_on_startup(sender=None, conf=None, **kwargs):
    ''' Execute these other tasks on startup, either as one time or very
    infrequent tasks that should run after system comes online
    '''
    pass


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Setup job refresh task
    # sender.add_periodic_task(mcfg.PLATFORM_JOB_POLL_RATE, refresh_all_jobs.s(),
    #                          name='refresh all jobs')
    pass

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(
        pcfg.STREAM_DOWNLOAD_INTERVAL,
        test.s('hello'))


@app.task
def test(arg):
    print(arg)

@app.task
def test(arg):
    print(arg)
