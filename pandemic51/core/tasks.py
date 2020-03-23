'''
Celery Tasks

'''
import celery

app = celery.Celery("pandemic51.tasks")
app.config_from_object("pandemic51.celery_config")

@app.task
def add(x, y):
    return x + y

# import celery
# from celery.schedules import crontab
#
# import pandemic51.core.config as pcfg
#
# app = celery.Celery()
#
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
#
#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(30.0, test.s('world'), expires=10)
#
#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         test.s('Happy Mondays!'),
#     )
#
#
#     # sender.add_periodic_task(pcfg.PLATFORM_JOB_POLL_RATE, refresh_all_jobs.s(),
#     #                          name='refresh all jobs')
#
# @app.task
# def test(arg):
#     print(arg)