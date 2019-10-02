from collections import namedtuple
from django.contrib.auth import get_user_model
from django.test import TestCase
from core.factories import UserFactory
from ..utility import (
    convert_tag_str_to_model,
    get_factories_for_model,
    get_serializers_for_model,
    generate_random_string,
    get_or_create_random_model_instances,
)

User = get_user_model()


class UtilityTest(TestCase):

    def test_convert_tag_str_to_model(self):
        # good test case
        tags = ['qr/631fx', '21^_3h90e1$', 'asfUG+;']
        converted_tags = map(lambda ct: ct.name, convert_tag_str_to_model(tags))
        self.assertTrue(all(map(lambda t: t in converted_tags, tags)))
        # bad test case
        tags = [3, 'afxx_5', -518]
        with self.assertRaises(ValueError) as _:
            converted_tags = map(lambda ct: ct.name, convert_tag_str_to_model(tags))

    def test_get_serializers_for_model(self):
        # specified model
        serializers = get_serializers_for_model(model=User, abstract=True, search_modules=['api.v1.serializers'])
        for serializer in serializers:
            self.assertTrue(issubclass(serializer.Meta.model, User))

    def test_get_factories_for_model(self):
        # specified model
        factories = get_factories_for_model(model=User, abstract=True, search_modules=['core.factories'])
        for factory in factories:
            self.assertTrue(issubclass(getattr(factory, '_meta').model, User))

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
        # minus count
        generated = get_or_create_random_model_instances(User, UserFactory, num=-4)
        self.assertEqual(len(generated), 0)
