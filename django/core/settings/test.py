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
            'format': '%(asctime)s %(levelname)-8s %(name)s.%(module)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'test': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'log/test.log',
            'mode': 'w',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['test'],
        },
    },
}
