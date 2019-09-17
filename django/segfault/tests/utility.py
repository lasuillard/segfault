from segfault import utility
from django.test import TestCase


class UtilityTest(TestCase):

    def test_generate_random_string_with_default_charset(self):
        """
            This function must return string that fulfills expected length
        """
        # (length_input, length_output_expected)
        test_cases = [(4, 4), (0, 0), (-4, 0)]
        for case in test_cases:
            result = utility.generate_random_string(length=case[0])
            self.assertEqual(len(result), case[1])

    def test_generate_random_string_with_custom_charset(self):
        charset = '1a5[^<F'
        test_cases = [(4, 4), (0, 0), (-4, 0)]
        for case in test_cases:
            result = utility.generate_random_string(length=case[0], charset=charset)
            self.assertTrue(all(map(lambda c: c in charset, result)))
            self.assertEqual(len(result), case[1])

