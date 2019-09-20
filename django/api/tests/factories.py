from django.test import TestCase
from segfault.utility import LabeledTestInput
from ..factories import UserFactory, RoomFactory


class RoomFactoryTest(TestCase):

    def test_users_list_param(self):
        test_cases = [
            LabeledTestInput([UserFactory() for _ in range(10)], 10),
            LabeledTestInput([], 0),
            LabeledTestInput(None, 0)
        ]
        for case in test_cases:
            room = RoomFactory(users=case.value)
            self.assertEqual(room.users.all().count(), case.label)
