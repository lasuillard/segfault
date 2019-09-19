import os
from segfault.utility import LabeledTestInput, generate_random_string, generate_simple_file
from django.test import TestCase


class UtilityTest(TestCase):

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

    def test_generate_simple_file(self):
        test_cases = [
            LabeledTestInput(('sample_text.jpg', 484), ('sample_text.jpg', 484)),
            LabeledTestInput(('wrong_file.wtf', -41), ('wrong_file.wtf', 0)),
        ]
        for case in test_cases:
            file = generate_simple_file(name=case.value[0], size=case.value[1])
            self.assertEqual(file.name, case.label[0])
            self.assertEqual(file.size, case.label[1])
