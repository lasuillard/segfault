from django.test import TestCase
from django.contrib.auth import get_user_model
from core.utility import get_serializers_for_model

User = get_user_model()


class SerializerTest(TestCase):

    def test_user_serializers_not_contain_credentials(self):
        user_serializers = get_serializers_for_model(model=User, abstract=True)
        for serializer in user_serializers:
            self.assertNotIn('password', serializer.Meta.fields)
