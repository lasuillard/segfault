import os
from django.test import TestCase
from segfault.utility import generate_simple_file
from ..factories import AvatarFactory
from ..models import Avatar


class SignalTest(TestCase):

    def test_auto_create_avatar_on_user_created(self):
        """
            Avatar instances are created along with user instance creation
        """
        avatar = AvatarFactory()
        # is avatar well created?
        self.assertIsInstance(avatar, Avatar)

    def test_delete_profile_image_on_change(self):
        """
            Test new image for avatar. its behavior depends on signal (and test includes it in fact!)
        """
        avatar = AvatarFactory()
        # create sample images for change
        [sample_image_one, sample_image_two] = [
            generate_simple_file(name=f'sample_image_{i}.jpg', size=8192, content_type='image/jpeg')
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

    def test_auto_delete_profile_image_on_delete(self):
        """
            Delete user custom image when avatar instance deleted
        """
        avatar = AvatarFactory()
        # set image
        avatar.profile_image = generate_simple_file(
            name='sample_image.jpg', size=8192, content_type='image/jpeg'
        )
        avatar.save()
        old_file_path = avatar.profile_image.path
        # is old image deleted from disk?
        avatar.delete()
        self.assertFalse(os.path.exists(old_file_path))

