from unittest import SkipTest
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from core.models import (
    Avatar, Fragment, Answer, Comment, Vote, Room, Chat, Notification
)
from core.factories import (
    UserFactory, AvatarFactory, FragmentFactory, AnswerFactory, CommentFactory, VoteFactory,
    RoomFactory, ChatFactory, NotificationFactory
)

User = get_user_model()
"""
Methods-actions mapping for DRF

GET: list, retrieve
POST: create
PUT: update
PATCH: partial_update
DELETE: destroy
"""
VIEWSET_ACTIONS = ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy']
VIEWSET_PERMISSIONS = ['anonymous', 'authenticated', 'owner', 'admin']


class ViewSetTestSetup(TestCase):

    def setUp(self):
        self._url_list = reverse(f'{self.view_name}-list')
        self._url_detail = lambda args, kwargs: reverse(f'{self.view_name}-detail', args=args, kwargs=kwargs)

        super(ViewSetTestSetup, self).setUp()

    @property
    def tag(self):
        return self.__class__.__name__

    @staticmethod
    def get_client(permission):
        client = APIClient()
        if permission in ['authenticated', 'owner']:
            client.user = UserFactory()
            client.force_authenticate(client.user)
        elif permission == 'admin':
            client.user = UserFactory(is_staff=True)
            client.force_authenticate(client.user)

        return client

    def get_item(self, permission, **kwargs):
        if permission == 'owner':
            return self.factory(user=kwargs['client'].user)

        return self.factory()

    def get_data(self, permission, action):
        pass

    def get_url(self, action, args=None, kwargs=None):
        if action in ['list', 'create']:
            return self._url_list
        elif action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return self._url_detail(args=args, kwargs=kwargs)

    @staticmethod
    def get_response(client, action, url, data=None):
        if action in ['list', 'retrieve']:
            return client.get(url, format='json')

        try:
            if action == 'create':
                return client.post(url, data=data, format='json')
            elif action == 'update':
                return client.put(url, data=data, format='json')
            elif action == 'partial_update':
                return client.patch(url, data=data, format='json')
            elif action == 'destroy':
                return client.delete(url, data=data, format='json')

        except ValueError:
            pass


class ViewSetActionTestMixin(ViewSetTestSetup):

    @classmethod
    def setUpClass(cls):
        if cls == ViewSetActionTestMixin:
            raise SkipTest(f"{__class__.__name__}: Don't test mixins.")
        else:
            super(ViewSetActionTestMixin, cls).setUpClass()

    def test_model_viewset_allowed_actions(self):
        for (action, permissions) in self.permissions_for_actions.items():
            for permission in permissions:
                client = self.get_client(permission)
                data = self.get_data(permission, action)
                if action in ['list', 'create']:
                    url = self.get_url(action)
                else:
                    item = self.get_item(permission, client=client)
                    url = self.get_url(action, kwargs={'pk': item.pk})

                response = self.get_response(client, action, url, data=data)
                if not hasattr(response, 'status_code'):
                    continue

                self.assertIn(response.status_code, [200, 201, 204], msg=f'{self.tag}-{action}-{permission}')

    def test_model_viewset_not_allowed_actions(self):
        item = self.factory()
        actions_not_allowed = [
            action for action in VIEWSET_ACTIONS if action not in self.permissions_for_actions.keys()
        ]
        for action in actions_not_allowed:
            client = self.get_client(permission='admin')
            url = self.get_url(action, kwargs={'pk': item.pk})

            response = self.get_response(client, action, url)
            if not hasattr(response, 'status_code'):
                continue

            self.assertEqual(response.status_code, 405,
                             msg=f'{self.tag}-{action}')


class ViewSetQueryTestMixin(ViewSetTestSetup):
    pass


class UserViewSetTest(ViewSetActionTestMixin, TestCase):
    view_name = 'api:v1:user'
    model = User
    factory = UserFactory
    permissions_for_actions = {
        'list': ['admin'],
        'retrieve': ['owner']
    }

    def get_item(self, permission, **kwargs):
        if permission == 'owner':
            return kwargs['client'].user

        return self.factory()


class AvatarViewSetTest(ViewSetActionTestMixin, TestCase):
    view_name = 'api:v1:avatar'
    model = Avatar
    factory = AvatarFactory
    permissions_for_actions = {
        'list': ['admin'],
        'retrieve': VIEWSET_PERMISSIONS,
        'update': ['owner'],
        'partial_update': ['owner']
    }

    def get_data(self, permission, action):
        return {
            'display_name': 'TEST',
            'introduce_message': 'TEST',
        }


class FragmentViewSetTest(ViewSetActionTestMixin, TestCase):
    view_name = 'api:v1:fragment'
    model = Fragment
    factory = FragmentFactory
    permissions_for_actions = {
        'list': VIEWSET_PERMISSIONS,
        'create': ['authenticated', 'owner', 'admin'],
        'retrieve': VIEWSET_PERMISSIONS,
        'update': ['owner'],
        'partial_update': ['owner'],
        'destroy': ['owner']
    }

    def get_data(self, permission, action):
        return {
            'title': 'TEST',
            'content': 'TEST'
        }


class AnswerViewSetTest(ViewSetActionTestMixin, TestCase):
    view_name = 'api:v1:answer'
    model = Answer
    factory = AnswerFactory
    permissions_for_actions = {
        'list': VIEWSET_PERMISSIONS,
        'create': ['authenticated', 'owner', 'admin'],
        'retrieve': VIEWSET_PERMISSIONS,
        'update': ['owner'],
        'partial_update': ['owner'],
        'destroy': ['owner']
    }

    def get_data(self, permission, action):
        return {
            'target': FragmentFactory().pk,
            'content': 'TEST'
        }


class CommentViewSetTest(ViewSetActionTestMixin, TestCase):
    view_name = 'api:v1:comment'
    model = Comment
    factory = CommentFactory
    permissions_for_actions = {
        'list': VIEWSET_PERMISSIONS,
        'create': ['authenticated', 'owner', 'admin'],
        'retrieve': VIEWSET_PERMISSIONS,
        'update': ['owner'],
        'partial_update': ['owner'],
        'destroy': ['owner']
    }

    def get_data(self, permission, action):
        return {
            'target': FragmentFactory().pk,
            'content': 'TEST'
        }


class VoteViewSetTest(ViewSetActionTestMixin, TestCase):
    view_name = 'api:v1:vote'
    model = Vote
    factory = VoteFactory
    permissions_for_actions = {
        'list': VIEWSET_PERMISSIONS,
        'create': ['authenticated', 'owner', 'admin'],
        'retrieve': VIEWSET_PERMISSIONS,
        'update': ['owner'],
        'partial_update': ['owner'],
        'destroy': ['owner']
    }

    def get_data(self, permission, action):
        return {
            'target': FragmentFactory().pk,
            'rating': Vote.NEUTRAL
        }


class RoomViewSetTest(ViewSetActionTestMixin, TestCase):
    view_name = 'api:v1:room'
    model = Room
    factory = RoomFactory
    permissions_for_actions = {
        'list': VIEWSET_PERMISSIONS,
        'create': ['authenticated', 'owner', 'admin'],
        'retrieve': VIEWSET_PERMISSIONS,
        'update': ['owner'],
        'partial_update': ['owner'],
        'destroy': ['owner']
    }

    def get_data(self, permission, action):
        return {
            'name': 'TEST'
        }


class ChatViewSetTest(ViewSetActionTestMixin, TestCase):
    view_name = 'api:v1:chat'
    model = Chat
    factory = ChatFactory
    permissions_for_actions = {
        'list': VIEWSET_PERMISSIONS,
        'retrieve': VIEWSET_PERMISSIONS,
        'update': ['owner'],
        'partial_update': ['owner'],
        'destroy': ['owner']
    }

    def get_data(self, permission, action):
        return {
            'content': 'TEST'
        }


class NotificationViewSetTest(ViewSetActionTestMixin, TestCase):
    view_name = 'api:v1:notification'
    model = Notification
    factory = NotificationFactory
    permissions_for_actions = {
        'list': ['admin'],
        'retrieve': ['owner'],
    }

    def get_item(self, permission, **kwargs):
        return self.factory(users=[kwargs['client'].user, ])

    def get_data(self, permission, action):
        return {}
