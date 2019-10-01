import random
from unittest import SkipTest, skip
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import (
    Avatar, Fragment, Tag, Answer, Comment, Vote, Room, Chat, Notification
)
from core.factories import (
    UserFactory, AvatarFactory, FragmentFactory, TagFactory, AnswerFactory, CommentFactory,
    VoteFactory, RoomFactory, ChatFactory, NotificationFactory
)
from core.utility import generate_random_string

User = get_user_model()

VIEWSET_ACTIONS = ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy']
VIEWSET_PERMISSIONS = ['anonymous', 'authenticated', 'owner', 'admin']

"""
Viewset tests permissions and actions also.

method-action mapping for DRF
- GET: list, retrieve
- POST: create
- PUT: update
- PATCH: partial_update
- DELETE: destroy
"""


class ViewSetTestSetup(TestCase):

    @classmethod
    def setUpClass(cls):
        # required attributes:
        for attr in ['view_name']:
            if not hasattr(cls, attr):
                raise AttributeError(f'Required attribute {attr} does not exists.')
        super().setUpClass()

    def setUp(self):
        self._url_list = reverse(f'{self.view_name}-list')
        self._url_detail = lambda args, kwargs: reverse(f'{self.view_name}-detail', args=args, kwargs=kwargs)
        super().setUp()

    @property
    def tag(self):
        return self.__class__.__name__

    @staticmethod
    def get_client(permission):
        """
        Return client that is authenticated with user who has specific permission
        """
        client = APIClient()
        if permission in ['authenticated', 'owner']:
            client.user = UserFactory()
            client.force_authenticate(client.user)
        elif permission == 'admin':
            client.user = UserFactory(is_staff=True)
            client.force_authenticate(client.user)
        else:
            client.user = AnonymousUser()

        # unspecified permission: anonymous by default
        return client

    def get_item(self, permission, action, client):
        """
        Returns the instance of model to be used for testing API requests.
        in detail, it is used for creation of resource url
        """
        if permission == 'owner':
            return self.factory(user=client.user)

        return self.factory()

    def get_data(self, permission, action):
        """
        It is a data, that is used to create item via API request.
        """
        raise NotImplementedError('get_data must be implemented.')

    def get_url(self, action, args=None, kwargs=None):
        """
        DRF action mapping for url-list, url-detail.
        """
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
            # the case when requested ownership-resources with anonymous user client.
            return None


class ViewSetActionTestMixin(ViewSetTestSetup):

    @classmethod
    def setUpClass(cls):
        if cls == ViewSetActionTestMixin:
            raise SkipTest(f"{__class__.__name__}: Don't test mixins.")
        else:
            super().setUpClass()

        # required attributes:
        for attr in ['model', 'factory', 'permissions_for_actions']:
            if not hasattr(cls, attr):
                raise AttributeError(f'Required attribute {attr} does not exists.')

    def get_data(self, permission, action):
        pass

    def test_model_viewset_allowed_actions(self):
        for (action, permissions) in self.permissions_for_actions.items():
            for permission in VIEWSET_PERMISSIONS:
                client = self.get_client(permission)
                data = self.get_data(permission, action)
                if action in ['list', 'create']:
                    url = self.get_url(action)
                else:
                    item = self.get_item(permission, action, client=client)
                    url = self.get_url(action, kwargs={'pk': item.pk})

                # request with client for resource url
                response = self.get_response(client, action, url, data=data)
                if response is None:
                    # anonymous user access handling
                    self.assertIn(action, ['create', 'update', 'partial_update', 'destroy'],
                                  msg=f'{self.tag}-{action}-{permission}; {response.data}')
                    self.assertIn(permission, ['anonymous'],
                                  msg=f'{self.tag}-{action}-{permission}; {response.data}')
                    continue

                # test!
                if permission in permissions:
                    self.assertIn(
                        response.status_code,
                        [status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_204_NO_CONTENT],
                        msg=f'{self.tag}-{action}-{permission}; {response.data}')
                else:
                    self.assertEqual(
                        response.status_code,
                        status.HTTP_403_FORBIDDEN,
                        msg=f'{self.tag}-{action}-{permission}; {response.data}')

    def test_model_viewset_not_allowed_actions(self):
        item = self.factory()
        actions_not_allowed = [
            action for action in VIEWSET_ACTIONS if action not in self.permissions_for_actions.keys()
        ]
        for action in actions_not_allowed:
            client = self.get_client(permission='admin')
            url = self.get_url(action, kwargs={'pk': item.pk})

            response = self.get_response(client, action, url)
            if response is None:
                self.assertIn(action, ['create', 'update', 'partial_update', 'destroy'],
                              msg=f'{self.tag}-{action}; {response.data}')
                continue

            self.assertEqual(
                response.status_code,
                status.HTTP_405_METHOD_NOT_ALLOWED,
                msg=f'{self.tag}-{action}; {response.data}')


class UserViewSetTest(ViewSetActionTestMixin, TestCase):
    view_name = 'api:v1:user'
    model = User
    factory = UserFactory
    permissions_for_actions = {
        'list': ['admin'],
        'retrieve': ['owner', 'admin']
    }

    def get_item(self, permission, action, client):
        if permission == 'owner':
            return client.user

        return self.factory()

    def get_data(self, permission, action):
        return {}


class AvatarViewSetTest(ViewSetActionTestMixin, TestCase):
    view_name = 'api:v1:avatar'
    model = Avatar
    factory = AvatarFactory
    permissions_for_actions = {
        'list': VIEWSET_PERMISSIONS,
        'retrieve': VIEWSET_PERMISSIONS,
        'update': ['owner', 'admin'],
        'partial_update': ['owner', 'admin']
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
        'update': ['owner', 'admin'],
        'partial_update': ['owner', 'admin'],
        'destroy': ['owner', 'admin']
    }

    def get_data(self, permission, action):
        return {
            'title': 'TEST',
            'content': 'TEST',
            'tags': [generate_random_string(length=32) for _ in range(random.randint(1, 6))]
        }


class TagViewSetTest(ViewSetActionTestMixin, TestCase):
    view_name = 'api:v1:tag'
    model = Tag
    factory = TagFactory
    permissions_for_actions = {
        'list': VIEWSET_PERMISSIONS,
        'create': ['admin'],
        'retrieve': VIEWSET_PERMISSIONS,
        'update': ['admin'],
        'partial_update': ['admin'],
        'destroy': ['admin']
    }

    def get_item(self, permission, action, client):
        return self.factory()

    def get_data(self, permission, action):
        return {
            'name': generate_random_string(length=32),
            'is_official': True
        }


class AnswerViewSetTest(ViewSetActionTestMixin, TestCase):
    view_name = 'api:v1:answer'
    model = Answer
    factory = AnswerFactory
    permissions_for_actions = {
        'list': VIEWSET_PERMISSIONS,
        'create': ['authenticated', 'owner', 'admin'],
        'retrieve': VIEWSET_PERMISSIONS,
        'update': ['owner', 'admin'],
        'partial_update': ['owner', 'admin'],
        'destroy': ['owner', 'admin']
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
        'update': ['owner', 'admin'],
        'partial_update': ['owner', 'admin'],
        'destroy': ['owner', 'admin']
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
        'update': ['owner', 'admin'],
        'partial_update': ['owner', 'admin'],
        'destroy': ['owner', 'admin']
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
        'update': ['owner', 'admin'],
        'partial_update': ['owner', 'admin'],
        'destroy': ['owner', 'admin']
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
        'update': ['owner', 'admin'],
        'partial_update': ['owner', 'admin'],
        'destroy': ['owner', 'admin']
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
        'retrieve': ['owner', 'admin'],
        'destroy': ['owner', 'admin']
    }

    def get_item(self, permission, action, client):
        if permission == 'owner':
            return self.factory(users=[client.user, ])

        return self.factory()

    def get_data(self, permission, action):
        return {
            'name': 'TEST'
        }
