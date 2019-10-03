import django_heroku
from .base import *

DEBUG = False

URL_FRONT = '/'

ALLOWED_HOSTS += ['https://capstone-project-segfault.herokuapp.com/', ]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = []

# Channel for Web Socket
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.environ.get('REDIS_URL'), ]
        },
    }
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
        # 'LOCATION':
    }
}

WSGI_APPLICATION = 'core.wsgi.heroku.application'
ASGI_APPLICATION = 'core.routing.application'

django_heroku.settings(locals())
