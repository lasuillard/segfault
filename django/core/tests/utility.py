from uuid import uuid4
from collections import namedtuple
from django.contrib.auth import get_user_model
from django.test import TestCase
from core.factories import UserFactory
from ..utility import (
    is_uuid4,
    get_factories_for_model,
    get_serializers_for_model,
    generate_random_string,
    get_or_create_random_model_instances,
)

User = get_user_model()


class Dummy:
    pass


class UtilityTest(TestCase):

    def test_is_uuid4(self):
        # test uuid4 string
        string = str(uuid4())
        self.assertTrue(is_uuid4(string))
        # test a string
        string = 'Hello World!'
        self.assertFalse(is_uuid4(string))

    def test_get_serializers_for_model(self):
        # specified model
        serializers = get_serializers_for_model(model=User, search_modules=['api.v1.serializers'], abstract=True)
        for serializer in serializers:
            self.assertTrue(issubclass(serializer.Meta.model, User))

        # no modules given
        serializers = get_serializers_for_model(model=User, search_modules=None, abstract=True)
        self.assertIsNone(serializers)

    def test_get_factories_for_model(self):
        # specified model
        factories = get_factories_for_model(model=User, search_modules=['core.factories'], abstract=True)
        for factory in factories:
            self.assertTrue(issubclass(getattr(factory, '_meta').model, User))

        # no modules given
        factories = get_factories_for_model(model=User, search_modules=None, abstract=True)
        self.assertIsNone(factories)

    def test_generate_random_string_with_default_charset(self):
        DataSet = namedtuple('DataSet', 'length charset label')
        test_cases = [
            DataSet(169, '1a5^[cgh_', 169),
            DataSet(0, '41@%_+234vx%31', 0),
            DataSet(-4, 'ggu85_*412', 0),
        ]
        for case in test_cases:
            result = generate_random_string(length=case.length, charset=case.charset)
            # generated string has expected length
            self.assertEqual(len(result), case.label)
            # all characters are from given charset
            self.assertTrue(all(map(lambda c: c in case.charset, result)))

    def test_get_or_create_random_model_instances(self):
        # normal cases
        initial_users = UserFactory.create_batch(size=3)
        generated = get_or_create_random_model_instances(User, UserFactory, num=10)
        self.assertEqual(len(generated), 10)
        for user in generated:
            self.assertIsInstance(user, User)
        self.assertTrue(all(map(lambda u: u in generated, initial_users)))
        # for zero length
        generated = get_or_create_random_model_instances(User, UserFactory, num=0)
        self.assertEqual(len(generated), 0)
        # minus count should return list of zero length
        generated = get_or_create_random_model_instances(User, UserFactory, num=-4)
        self.assertEqual(len(generated), 0)
        # when nothing to select
        User.objects.all().delete()
        generated = get_or_create_random_model_instances(User, UserFactory, num=3)
        self.assertEqual(len(generated), 3)
        # invalid model class
        with self.assertRaises(TypeError) as _:
            get_or_create_random_model_instances(Dummy, UserFactory, num=3)
        # invalid factory class
        with self.assertRaises(TypeError) as _:
            get_or_create_random_model_instances(User, Dummy, num=3)
