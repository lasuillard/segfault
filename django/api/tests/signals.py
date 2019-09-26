from django.contrib.auth import get_user_model
from django.test import TestCase
from core.models import Avatar

User = get_user_model()


class SignalTest(TestCase):

    def test_signal_auto_create_avatar_on_user_created(self):
        user = User.objects.create()
        self.assertIsInstance(user.avatar, Avatar)
        user.delete()
