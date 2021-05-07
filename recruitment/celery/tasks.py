#!coding=utf-8
from celery import Celery

#backend存储地址， broker（经纪人）存储任务系统的代理
app = Celery('task', backend='redis://127.0.0.1/', broker="redis://127.0.0.1")

@app.task
def add(x, y):
    return x + y