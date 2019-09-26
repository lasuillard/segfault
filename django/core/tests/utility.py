from django.contrib.auth import get_user_model
from django.test import TestCase
from core.utility import (
    LabeledTestInput,
    get_factories_for_model,
    get_serializers_for_model,
    generate_random_string
)
from api.v1.serializers import UserSerializer, UserDetailSerializer
from core.factories import UserFactory

User = get_user_model()


class UtilityTest(TestCase):

    def test_get_serializers_for_model(self):
        serializers = get_serializers_for_model(model=User, abstract=True, search_modules=['api.v1.serializers'])
        self.assertIn(UserSerializer, serializers)
        self.assertIn(UserDetailSerializer, serializers)

    def test_get_factories_for_model(self):
        factories = get_factories_for_model(model=User, abstract=True, search_modules=['api.factories'])
        self.assertIn(UserFactory, factories)

    def test_generate_random_string_with_default_charset(self):
        """
            This function must return string that fulfills expected length
        """
        # (length_input, length_output_expected)
        test_cases = [LabeledTestInput(4, 4), LabeledTestInput(0, 0), LabeledTestInput(-4, 0)]
        for case in test_cases:
            result = generate_random_string(length=case.value)
            self.assertEqual(len(result), case.label)

    def test_generate_random_string_with_custom_charset(self):
        charset = '1a5[^<F'
        test_cases = [LabeledTestInput(4, 4), LabeledTestInput(0, 0), LabeledTestInput(-4, 0)]
        for case in test_cases:
            result = generate_random_string(length=case.value, charset=charset)
            self.assertTrue(all(map(lambda c: c in charset, result)))
            self.assertEqual(len(result), case.label)
