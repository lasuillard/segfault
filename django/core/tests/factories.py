from django.contrib.auth import get_user_model
from django.test import TestCase
from core.models import (
    Avatar, Fragment, Tag, Answer, Comment, Vote, Room, Chat, Notification
)
from core.utility import get_factories_for_model

User = get_user_model()


class ModelFactoryTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.models = [Avatar, Fragment, Tag, Answer, Comment, Vote, Room, Chat, Notification]
        super().setUpClass()

    def test_core_at_least_one_factory_for_non_abstract_models(self):
        for model in self.models:
            factories = get_factories_for_model(model, search_modules=['core.factories'])
            self.assertGreater(len(factories), 0)
