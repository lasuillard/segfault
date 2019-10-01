import pytest
from rest_framework.authtoken.models import Token
from channels.testing import WebsocketCommunicator
from core.routing import application
from core.factories import UserFactory, AvatarFactory, RoomFactory


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestChatWebSocket:

    @staticmethod
    def get_communicator(room, token):
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/ws/chat/{room.pk}/',
            subprotocols=['access_token', token.key]
        )
        communicator.scope['url_route'] = {'kwargs': {'room_id': room.pk}}
        return communicator

    async def test_chat_websocket_valid_user_connection(self):
        # setup
        user = UserFactory()
        token = Token.objects.create(user=user)
        room = RoomFactory()

        # connection establishment
        communicator = self.get_communicator(room, token)
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

    async def test_chat_websocket_invalid_user_fails_connection(self):
        pass

    async def test_chat_websocket_behavior_send_message(self):
        pass


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestNotificationWebSocket:

    @staticmethod
    def get_communicator(room, token):
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/ws/notification/',
            subprotocols=['access_token', token.key]
        )
        communicator.scope['url_route'] = {'kwargs': {'room_id': room.pk}}
        return communicator

    async def test_chat_websocket_valid_user_connection(self):
        # setup
        user = UserFactory()
        avatar = AvatarFactory(user=user)
        token = Token.objects.create(user=user)

        # connection establishment
        communicator = self.get_communicator(user, token)
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

    async def test_notification_websocket_invalid_user_fails_connection(self):
        pass

    async def test_notification_websocket_behavior_send_message(self):
        pass
