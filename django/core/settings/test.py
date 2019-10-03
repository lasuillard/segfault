from .dev import *

# Django Channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'test': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'log/django-test.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'core': {
            'level': 'DEBUG',
            'handlers': ['test'],
        },
        'auth': {
            'level': 'DEBUG',
            'handlers': ['test'],
        },
        'api': {
            'level': 'DEBUG',
            'handlers': ['test'],
        },
        'ws': {
            'level': 'DEBUG',
            'handlers': ['test'],
        },
    },
}
