from .base import *

DEBUG = True

URL_FRONT = f"http://{ os.environ.get('NUXT_HOST', 'localhost') }:{ os.environ.get('NUXT_PORT', '3000') }"

ALLOWED_HOSTS = '*'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = [
    URL_FRONT,
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME', 'segfault'),
        'USER': os.environ.get('DATABASE_USERNAME', 'dbuser'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', '9306'),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('DATABASE_PORT', '5432'),
    }
}

# Channel for Web Socket
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [
                (os.environ.get('REDIS_HOST', 'localhost'), os.environ.get('REDIS_PORT', 6379))
            ]
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

# Logger
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'debug': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['debug'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'log/dev.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True
        },
        'django.request': {
            'handlers': ['console'],
            'propagate': False
        },
        'core': {
            'handlers': ['console', 'file'],
            'propagate': True
        },
        'api': {
            'handlers': ['console', 'file'],
            'propagate': True
        },
        'ws': {
            'handlers': ['console', 'file'],
            'propagate': True
        },
    },
}
