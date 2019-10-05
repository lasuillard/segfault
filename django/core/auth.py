import logging
from django.db import close_old_connections
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from channels.auth import AuthMiddlewareStack

logger = logging.getLogger(__name__)


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        subprotocols = scope['subprotocols']
        try:
            index = subprotocols.index('access_token')
            key = subprotocols[index + 1]  # expects [..., 'access_token', token, ...]
            token = Token.objects.get(key=key)
            scope['user'] = token.user
            close_old_connections()
        except ValueError:
            scope['user'] = AnonymousUser()
            logger.debug('Authorization failed due to malformed subprotocol: {}'.format(subprotocols))
        except Token.DoesNotExist:
            scope['user'] = AnonymousUser()
            logger.debug('Authorization failed due to invalid token: {}'.format(key))

        return self.inner(scope)


def token_auth(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))


TokenAuthMiddlewareStack = token_auth
