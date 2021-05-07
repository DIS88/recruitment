set DJANGO_SETTING_MODULE=settings.local
@REM celery - app recruitment beat --scheduler django_celery_beat.schedulers:DatabaseScheduler
celery -A recruitment beat --scheduler django_celery_beat.schedulers:DatabaseScheduler