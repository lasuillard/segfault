from django.contrib.auth import get_user_model
from django.test import TestCase
from ..utility import (
    LabeledTestInput,
    convert_tag_str_to_model,
    get_factories_for_model,
    get_serializers_for_model,
    generate_random_string
)
from ..factories import UserFactory, TagFactory

User = get_user_model()


class UtilityTest(TestCase):

    def test_convert_tag_str_to_model(self):
        # good test case
        tags = ['Test', 'Test_2', 'Test_3']
        converted_tags = map(lambda ct: ct.name, convert_tag_str_to_model(tags))
        self.assertTrue(all(map(lambda t: t in converted_tags, tags)))
        # bad test case
        assert not 'Code me!'

    def test_get_serializers_for_model(self):
        serializers = get_serializers_for_model(model=User, abstract=True, search_modules=['api.v1.serializers'])
        for serializer in serializers:
            self.assertTrue(issubclass(serializer.Meta.model, User))

    def test_get_factories_for_model(self):
        factories = get_factories_for_model(model=User, abstract=True, search_modules=['core.factories'])
        for factory in factories:
            self.assertTrue(issubclass(getattr(factory, '_meta').model, User))

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
