import pytest
from rest_framework.authtoken.models import Token
from channels.testing import WebsocketCommunicator
from core.routing import application
from core.factories import UserFactory, AvatarFactory, RoomFactory


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestChatWebSocket:

    async def test_chat_websocket_connection(self):
        # setup
        user = UserFactory()
        token = Token.objects.create(user=user)
        room = RoomFactory()

        # connection establishment
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/ws/chat/{room.pk}/',
            subprotocols=['access_token', token.key]
        )
        communicator.scope['url_route'] = {'kwargs': {'room_id': room.id}}
        connected, subprotocol = await communicator.connect()
        scope = communicator.scope

        # is websocket connected?
        assert connected
        # is communicator responded with access_token(OK)?
        assert subprotocol == 'access_token'
        # is user correct?
        assert user == scope['user']

        # teardown
        await communicator.disconnect()

    async def test_chat_websocket_behavior(self):
        pass


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestNotificationWebSocket:

    async def test_chat_websocket_connection(self):
        # setup
        user = UserFactory()
        avatar = AvatarFactory(user=user)
        token = Token.objects.create(user=user)

        # connection establishment
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/ws/notification/',
            subprotocols=['access_token', token.key]
        )
        connected, subprotocol = await communicator.connect()
        scope = communicator.scope

        # is websocket connected?
        assert connected
        # is communicator responded with access_token(OK)?
        assert subprotocol == 'access_token'
        # is user correct?
        assert user == scope['user']

        # teardown
        await communicator.disconnect()
