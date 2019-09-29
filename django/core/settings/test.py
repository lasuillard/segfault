from .dev import *

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    }
}

# log
LOGGING['loggers'].pop('django')  # disabled because it makes too many db-query logs
LOGGING['handlers']['file']['filename'] = 'log/test.log'  # log to test.log, not debug.log
