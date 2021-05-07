from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.base')

# app = Celery('recruitment') 这个会默认连接amqp://guest:**@localhost:5672//
app = Celery('pro', backend='redis://localhost:6379/1', broker='redis://localhost:6379/0')

#表示在settings.py下以CELERY开头的都是配置项
app.config_from_object('django.conf:settings', namespace='CELERY')


#检测每个应用下的tasks.py
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))


from recruitment.tasks import add

app.conf.beat_schedule = {
    'add-every-6-seconds': {
        'task': 'recruitment.tasks.add',
        'schedule': 6.0,
        'args': (66, 55, )
    },
}


from celery.schedules import crontab
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='hello every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )



# import json
# from django_celery_beat.models import PeriodicTask, IntervalSchedule

# #先创建定时策略
# schedule, created = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS,)

# ##再创建任务
# task = PeriodicTask.objects.create(interval=schedule, name='say1 hi04310', 
#                     task='recruitment.celery.test', 
#                     args=json.dumps(['welcome']),)


@app.task
def test(arg):
    print(arg)
# from __future__ import absolute_import, unicode_literals

# import os

# from celery import Celery, shared_task

# # set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.base')

# app = Celery('recruitment')

# # Using a string here means the worker doesn't have to serialize
# # the configuration object to child processes.
# # - namespace='CELERY' means all celery-related configuration keys
# #   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Load task modules from all registered Django app configs.
# app.autodiscover_tasks()


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))