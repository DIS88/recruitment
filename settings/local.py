from .base import *

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "host.docker.internal", "*",]

## 务必修改以下值，确保运行时系统安全:
SECRET_KEY = 'django-insecure-)8ebp1)#mv-bcr$k2zn_h45^751u@&&$r@yz_!n@1lx0rj#bsh'


## 如果仅使用数据库中的账号，以下 LDAP 配置可忽略
## 替换这里的配置为正确的域服务器配置，同时可能需要修改 base.py 中的 LDAP 服务器相关配置:

INTERNAL_IPS =('127.0.0.1', 'host.docker.internal')


INSTALLED_APPS += (
    # other apps for production site
    # 'debug_toolbar',
)


# STATIC_URL = '/static/'

# CACHES = {
#     "default":{
#         "BACKEND": 'django_redis.cache.RedisCache',
#         "LOCATION": "redis://127.0.0.1:6379",
#         "TIMEOUT": 300,
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             # "PASSWORD": "mysecret",
#             "SOCKET_CONNECT_TIMEOUT": 5, #seconds
#             "SOCKET_TIMEOUT": 5, 
#         }
#     }
# }
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# sentry_sdk.init(
#     dsn="http://4337885bf7fd49fb9fa035852f857d1e@127.0.0.1:9000/2",
#     integrations=[DjangoIntegration()],

#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production.
#     traces_sample_rate=1.0,

#     # If you wish to associate users to errors (assuming you are using
#     # django.contrib.auth) you may enable sending PII data.(personal identification info)
#     send_default_pii=True 
# )



## 钉钉群的 WEB_HOOK， 用于发送钉钉消息
DINGTALK_WEB_HOOK = "https://oapi.dingtalk.com/robot/send?access_token=a7bcba3950f49e3385a93073bcb02d6163e19ee6d50ea9fe0ca5ab92542d4c6c"

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Shanghai"
CELERY_MAX_TASKS_PER_CHILD = 10
CELERY_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_word.log")
CELERYBEAT_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_beat.log")
