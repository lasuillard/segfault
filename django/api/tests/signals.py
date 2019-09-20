import os
import random
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import TestCase
from segfault.utility import generate_random_string
from ..factories import UserFactory, AvatarFactory
from ..models import Avatar

User = get_user_model()


class SignalTest(TestCase):

    def test_auto_create_avatar_on_user_created(self):
        user = User.objects.create()
        self.assertIsInstance(user.avatar, Avatar)
        user.delete()

    def test_delete_profile_image_on_change(self):
        avatar = AvatarFactory()
        # create sample images for change
        [sample_image_one, sample_image_two] = [
            SimpleUploadedFile(
                name=f'{ generate_random_string(length=16) }.jpg',
                content=b'\x00' * random.randint(0, 65536),
                content_type='image/jpeg'
            ) for _ in range(2)
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

    def test_auto_delete_profile_image_on_delete(self):
        avatar = AvatarFactory()
        # set image
        avatar.profile_image = SimpleUploadedFile(
            name=f'{ generate_random_string(length=16) }.jpg',
            content=b'\x00' * random.randint(0, 65536),
            content_type='image/jpeg'
        )
        avatar.save()
        old_file_path = avatar.profile_image.path
        # is old image deleted from disk?
        avatar.delete()
        self.assertFalse(os.path.exists(old_file_path))

