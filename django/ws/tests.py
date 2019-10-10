import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status
from channels.testing import WebsocketCommunicator
from asgiref.sync import sync_to_async
from core.routing import application
from core.factories import UserFactory, AvatarFactory, RoomFactory, NotificationFactory
from core.utility import generate_random_string

User = get_user_model()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestChatWebSocket:

    @staticmethod
    def get_communicator(user=None, room=None, token=None):
        user = AvatarFactory().user if user is None else user
        room = RoomFactory().pk if room is None else room
        token = Token.objects.create(user=user).key if token is None else token
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/ws/chat/{room}/',
            subprotocols=['access_token', token]
        )
        communicator.scope['url_route'] = {'kwargs': {'room_id': room}}
        communicator.context = {
            'user': user,
            'room': room,
            'token': token
        }
        return communicator

    async def test_chat_websocket_valid_user_connection_ok(self):
        # try to connect
        communicator = self.get_communicator()
        connected, subprotocol = await communicator.connect()
        # is websocket connected?
        assert connected
        # is communicator responded with access_token(OK)?
        assert subprotocol == 'access_token'
        # is user correct?
        assert communicator.context['user'] == communicator.scope['user']
        # teardown
        await communicator.disconnect()

    async def test_chat_websocket_connect_with_invalid_token_fails(self):
        # try to connect with invalid token
        communicator = self.get_communicator(token='sdfah_^%#@^')
        connected, subprotocol = await communicator.connect()
        # is connection failed?
        assert not connected
        # is subprotocol responded with status code?
        assert subprotocol == status.HTTP_401_UNAUTHORIZED

    async def test_chat_websocket_connect_to_room_does_not_exist_fails(self):
        # try to connect to room does not exist
        communicator = self.get_communicator(room=0)
        connected, subprotocol = await communicator.connect()
        # is connection failed?
        assert not connected
        # is subprotocol responded with status code?
        assert subprotocol == status.HTTP_400_BAD_REQUEST

    async def test_chat_websocket_behavior_send_message(self):
        # two communicator in a room
        room = RoomFactory()
        sender = self.get_communicator(room=room.pk)
        await sender.connect()
        receiver = self.get_communicator(room=room.pk)
        await receiver.connect()
        # send message
        await sender.send_json_to(data={
            'content': 'Hello'
        })
        # is message came well?
        data = await receiver.receive_json_from(timeout=1)
        assert data['content'] == 'Hello'
        # teardown
        await sender.disconnect()
        await receiver.disconnect()

    async def test_chat_websocket_behavior_send_malformed_message_receive_error(self):
        # two communicator in a room
        room = RoomFactory()
        sender = self.get_communicator(room=room.pk)
        await sender.connect()
        receiver = self.get_communicator(room=room.pk)
        await receiver.connect()
        # send malformed message
        await sender.send_json_to(data={
            '_a_unsupported_key_': '_an_awesome_malformed_data_',
            'content': 'i am valid'
        })
        # sender will get error message
        response = await sender.receive_json_from(timeout=1)
        assert 'error' in response
        # server will never broadcast malformed data. is it?
        assert await receiver.receive_nothing(timeout=1)
        # teardown
        await sender.disconnect()
        await receiver.disconnect()

    async def test_chat_websocket_behavior_send_invalid_message_receive_error(self):
        # two communicator in a room
        room = RoomFactory()
        sender = self.get_communicator(room=room.pk)
        await sender.connect()
        receiver = self.get_communicator(room=room.pk)
        await receiver.connect()
        # send message
        await sender.send_json_to(data={
            'content': generate_random_string(length=65536)
        })
        # sender will receive error message
        response = await sender.receive_json_from(timeout=1)
        assert 'error' in response
        # others will get nothing
        assert await receiver.receive_nothing(timeout=1)
        # teardown
        await sender.disconnect()
        await receiver.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestNotificationWebSocket:

    @staticmethod
    def get_communicator(user=None, token=None):
        user = AvatarFactory().user if user is None else user
        token = Token.objects.create(user=user).key if token is None else token
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/ws/notification/',
            subprotocols=['access_token', token]
        )
        communicator.context = {
            'user': user,
            'token': token
        }
        return communicator

    async def test_chat_websocket_valid_user_success_connection(self):
        # try to connect
        communicator = self.get_communicator()
        connected, subprotocol = await communicator.connect()
        # is websocket connected?
        assert connected
        # is communicator responded with access_token(OK)?
        assert subprotocol == 'access_token'
        # is user correct?
        assert communicator.context['user'] == communicator.scope['user']
        # teardown
        await communicator.disconnect()

    async def test_notification_websocket_connect_with_invalid_token_fails(self):
        # try to connect with invalid token
        communicator = self.get_communicator(token='adg51^&R_+h')
        connected, subprotocol = await communicator.connect()
        # is connection failed?
        assert not connected
        # is subprotocol responded with status code?
        assert subprotocol == status.HTTP_401_UNAUTHORIZED

    async def test_notification_websocket_behavior_server_send_message(self):
        # connect
        communicator = self.get_communicator()
        await communicator.connect()
        # make new notification for user
        notification = NotificationFactory(users=[communicator.context['user'], ])
        # server send message to user
        await sync_to_async(notification.send)(fcm_push=False)
        # is message arrived?
        response = await communicator.receive_json_from(timeout=1)
        assert response['title'] == notification.title
        assert response['body'] == notification.body
        assert 'data' in response
        # teardown
        await communicator.disconnect()

    async def test_notification_websocket_behavior_is_receive_only(self):
        # connect
        communicator = self.get_communicator()
        await communicator.connect()
        # send any message to server
        await communicator.send_json_to(data={'_a_field_i_want_show_you_': '_whatever_i_send_you_never_see_it_'})
        # server will never respond any messages because it is receive-only
        assert communicator.receive_nothing(timeout=5)
        # teardown
        await communicator.disconnect()
