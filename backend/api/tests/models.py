import os
import uuid
import string
import random


from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.contrib.auth import get_user_model
from api.models import (
    Avatar,
    Fragment,
    Answer,
    Comment,
    Vote,
    ChatRoom,
    Chat,
)


User = get_user_model()


def create_tester(*args, **kwargs):
    return User.objects.create(username=create_random_string(16), *args, **kwargs)


def create_random_string(length, charset=None):
    if charset is None:
        charset = string.ascii_letters + string.digits

    return ''.join([random.choice(charset) for _ in range(length)])


def validate_uuid_format(uuid_to_test):
    try:
        uuid_obj = uuid.UUID(uuid_to_test)
    except ValueError:
        return False

    return str(uuid_obj) == uuid_to_test


class ToolTest(TestCase):

    def test_create_tester(self):
        tester = create_tester()
        self.assertTrue(isinstance(tester, User))

    def test_create_random_string(self):
        length = 16
        self.assertEqual(length, len(create_random_string(16)))

    def test_validate_uuid_format(self):
        uuid_to_test = uuid.uuid4()
        self.assertTrue(validate_uuid_format(str(uuid_to_test)))


class AvatarTest(TestCase):

    def create_avatar(self, user=None, profile_image=None, display_name=None, introduce_message=None):
        if user is None:
            user = create_tester()

        return Avatar.objects.create(
            user=user,
            profile_image=profile_image,
            display_name=display_name,
            introduce_message=introduce_message,
        )

    def test_avatar_creation(self):
        pass

    def test_avatar_profile_image(self):
        avatar = self.create_avatar(
            profile_image=SimpleUploadedFile(
                name='test_image.jpeg',
                content=b'\x00\x01\x02\x03',
                content_type='image/jpeg'
            )
        )
        path = avatar.profile_image.path
        self.assertTrue(os.path.exists(path))
        self.assertTrue(validate_uuid_format(os.path.basename(path).split('.')[0]))
        # test for change image
        old_path = path
        avatar.profile_image = SimpleUploadedFile(
            name='test_image_changed.jpeg',
            content=b'\x00\x01\x02\x03',
            content_type='image/jpeg'
        )
        avatar.save()
        new_path = avatar.profile_image.path
        self.assertNotEqual(old_path, new_path)
        self.assertFalse(os.path.exists(old_path))
        self.assertTrue(os.path.exists(new_path))
        self.assertTrue(validate_uuid_format(os.path.basename(new_path).split('.')[0]))
        # test for deletion
        avatar.delete()
        self.assertFalse(os.path.exists(path))

    def test_avatar_display_name(self):
        avatar = self.create_avatar(display_name='Tester 1')
        self.assertTrue(isinstance(avatar, Avatar))
        self.assertTrue(bool(avatar.display_name in avatar.__str__()))

    def test_avatar_introduce_message(self):
        avatar = self.create_avatar(introduce_message='')
        self.assertTrue(isinstance(avatar, Avatar))
        self.assertEqual(avatar.user.username, avatar.display_name)
