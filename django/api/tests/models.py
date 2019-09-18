import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.contrib.auth import get_user_model
from segfault.utility import generate_random_string
from api.models import (
    Avatar, AVATAR_DEFAULT_IMAGE,
    Fragment,
    Answer,
    Comment,
    Vote, VOTE_CHOICES,
    ChatRoom,
    Chat,
)

User = get_user_model()


class AvatarTest(TestCase):

    def test_avatar_created_with_default(self):
        """
            Test avatar instance is created with appropriate default
        """
        tester = User.objects.create(username=generate_random_string(16))
        avatar = tester.avatar
        # when display_name is not given, then defaulted by username
        self.assertEqual(avatar.display_name, tester.username)
        # the avatar is given default image when not specified
        self.assertEqual(avatar.profile_image.name, AVATAR_DEFAULT_IMAGE)
        tester.delete()

    def test_avatar_blank_display_name(self):
        tester = User.objects.create(username=generate_random_string(16))
        avatar = tester.avatar
        # blank the display_name
        avatar.display_name = ''
        avatar.save()
        self.assertEqual(avatar.display_name, tester.username)

    def test_avatar_set_profile_image(self):
        """
            Test new image for avatar and the image is stored at media storage
        """
        tester = User.objects.create(username=generate_random_string(16))
        avatar = tester.avatar
        # set avatar image
        avatar.profile_image = SimpleUploadedFile(
            name='sample_image.jpg', content=b'\x00' * 1024, content_type='image/jpeg'
        )
        avatar.save()
        # image should be created properly in media folder
        self.assertEqual(os.path.basename(os.path.dirname(os.path.dirname(avatar.profile_image.path))), 'media')
        # and also the file should exist
        self.assertTrue(os.path.exists(avatar.profile_image.path))
        tester.delete()

    def test_avatar_profile_image_has_uuid4_format(self):
        """
            Custom user profile images has name of uuid4 format
        """
        pass

    def test_avatar_signal_auto_create_avatar_on_user_created(self):
        """
            Avatar instances are created along with user instance creation
        """
        tester = User.objects.create(username=generate_random_string(16))
        avatar = tester.avatar
        # is avatar well created?
        self.assertIsInstance(avatar, Avatar)
        tester.delete()

    def test_avatar_signal_auto_delete_profile_image_on_change(self):
        """
            Test new image for avatar. its behavior depends on signal (and test includes it in fact!)
        """
        tester = User.objects.create(username=generate_random_string(16))
        avatar = tester.avatar
        # create sample images for change
        [sample_image_one, sample_image_two] = [
            SimpleUploadedFile(name=f'sample_image_{i}.jpg', content=b'\x00' * 1024, content_type='image/jpeg')
            for i in range(2)
        ]
        # set first image
        avatar.profile_image = sample_image_one
        avatar.save()
        old_file_path = avatar.profile_image.path
        # change to new image
        avatar.profile_image = sample_image_two
        avatar.save()
        new_file_path = avatar.profile_image.path
        # is old image file deleted?
        self.assertFalse(os.path.exists(old_file_path))
        # new file saved in storage?
        self.assertTrue(os.path.exists(new_file_path))
        tester.delete()

    def test_avatar_signal_auto_delete_profile_image_on_delete(self):
        """
            Delete user custom image when avatar instance deleted
        """
        tester = User.objects.create(username=generate_random_string(16))
        avatar = tester.avatar
        # set image
        avatar.profile_image = SimpleUploadedFile(
            name='sample_image.jpg', content=b'\x00' * 1024, content_type='image/jpeg'
        )
        avatar.save()
        old_file_path = avatar.profile_image.path
        # is old image deleted from disk?
        avatar.delete()
        self.assertFalse(os.path.exists(old_file_path))
        tester.delete()

    def test_avatar_magic_method_str_includes_instance_id(self):
        """
            __str__ should include object primary key for identification
        """
        tester = User.objects.create(username=generate_random_string(16))
        avatar = tester.avatar
        # the instance should represent itself well
        self.assertIn(str(avatar.pk), avatar.__str__())
        tester.delete()


class AnswerTest(TestCase):

    def test_answer_magic_method_str_includes_instance_id(self):
        tester = User.objects.create(username=generate_random_string(16))
        fragment = Fragment.objects.create(
            user=tester, title=generate_random_string(64), content=generate_random_string(1024)
        )
        answer = Answer.objects.create(user=tester, target=fragment, content=generate_random_string(1024))
        self.assertIn(str(answer.pk), answer.__str__())

