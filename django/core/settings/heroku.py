import django_heroku
from .base import *

DEBUG = True

URL_FRONT = '/'

ALLOWED_HOSTS += ['https://capstone-project-segfault.herokuapp.com/', ]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    'https://capstone-project-segfault.herokuapp.com/',
]

# Channel for Web Socket
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.environ.get('REDIS_URL'), ]
        }
    }
}

django_heroku.settings(locals())
