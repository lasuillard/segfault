from django.contrib.auth import get_user_model
from django.test import TestCase
from ..models import Avatar

User = get_user_model()


class SignalTest(TestCase):

    def test_signal_auto_create_avatar_on_user_created(self):
        # test for avatar is created when user is created
        user = User.objects.create()
        self.assertIsInstance(user.avatar, Avatar)
        user.delete()
