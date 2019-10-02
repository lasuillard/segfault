import dj_database_url
from .base import *

DEBUG = True

URL_FRONT = f"http://{ os.environ.get('NUXT_HOST', 'localhost') }:{ os.environ.get('NUXT_PORT', '3000') }"

ALLOWED_HOSTS = '*'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [
    URL_FRONT,
]

# Database
DATABASES = {
    'default': dj_database_url.config(default='postgres://dbuser:9306@localhost:5432/segfault')
}

# Channel for Web Socket
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.environ.get('REDIS_URL', 'redis://localhost:6379'), ]
        }
    }
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
        # 'LOCATION':
    }
}
