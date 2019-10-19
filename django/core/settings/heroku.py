import django_heroku
from .base import *

DEBUG = os.environ.get('DEBUG', False)

URL_FRONT = '/'

ALLOWED_HOSTS += ['https://capstone-project-segfault.herokuapp.com/', 'localhost']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = DEBUG
CORS_ORIGIN_WHITELIST = []
CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
CORS_ALLOW_HEADERS = [
    'X-Requested-With',
    'Content-Type',
    'Accept',
    'Origin',
    'Authorization',
    'X-CSRFTOKEN'
]

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
