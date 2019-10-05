import os
import statistics
import random
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import TestCase
from ..utility import is_uuid4, get_factories_for_model, generate_random_string
from ..models import (
    Avatar, Commentable, Votable
)
from ..factories import (
    UserFactory, AvatarFactory, FragmentFactory, TagFactory, AnswerFactory,
    CommentFactory, VoteFactory, RoomFactory, ChatFactory, NotificationFactory
)

User = get_user_model()


class AvatarTest(TestCase):

    def tearDown(self):
        # all avatar instances should be deleted for images related with it
        Avatar.objects.all().delete()

    def test_avatar_created_with_default(self):
        """
        when default values are given with None, it should be handled with some default values.
        """
        avatar = AvatarFactory(profile_image=None, display_name=None)
        # when display_name is not given, then defaulted by username
        self.assertEqual(avatar.display_name, avatar.user.username)
        # the avatar is given default image when not specified
        self.assertEqual(avatar.profile_image.name, Avatar.AVATAR_DEFAULT_IMAGE)

    def test_avatar_blank_display_name(self):
        """
        display_name defaults to user's username
        """
        avatar = AvatarFactory()
        # blank the display_name
        avatar.display_name = ''
        avatar.save()
        # display_name goes to default value when not given.
        self.assertEqual(avatar.display_name, avatar.user.username)

    def test_avatar_set_profile_image(self):
        """
        test avatar profile image storage handling(location, name)
        """
        avatar = AvatarFactory()
        avatar.profile_image = SimpleUploadedFile(
            name=f'{ generate_random_string(length=16) }.jpg',
            content=b'\x00' * random.randint(1, 65536),
            content_type='image/jpeg'
        )
        avatar.save()
        file = avatar.profile_image
        # stored at media/avatar folder?
        self.assertEqual(os.path.basename(os.path.dirname(file.path)), 'avatar')
        self.assertEqual(os.path.basename(os.path.dirname(os.path.dirname(file.path))), 'media')
        # is file exists?
        self.assertTrue(os.path.exists(file.path))
        # and is uuid4 format?
        filename = os.path.splitext(os.path.basename(file.name))[0]
        self.assertTrue(is_uuid4(filename))

    def test_avatar_delete_profile_image_on_change(self):
        """
        test for profile image handling on image change
        """
        avatar = AvatarFactory()
        # create sample images for change
        [file_before, file_after] = [
            SimpleUploadedFile(
                name=f'{ generate_random_string(length=16) }.jpg',
                content=b'\x00' * random.randint(1, 65536),
                content_type='image/jpeg'
            ) for _ in range(2)
        ]
        # set first image
        avatar.profile_image = file_before
        avatar.save()
        old_file_path = avatar.profile_image.path
        self.assertTrue(os.path.exists(old_file_path))
        # change to new image
        avatar.profile_image = file_after
        avatar.save()
        new_file_path = avatar.profile_image.path
        self.assertTrue(os.path.exists(new_file_path))
        # is old image file deleted?
        self.assertFalse(os.path.exists(old_file_path))
        # new file saved in storage?
        self.assertTrue(os.path.exists(new_file_path))

    def test_avatar_delete_profile_image_on_delete(self):
        """
        test custom profile images are deleted when avatar instance deleted.
        """
        avatar = AvatarFactory()
        avatar.profile_image = SimpleUploadedFile(
            name=f'{ generate_random_string(length=16) }.jpg',
            content=b'\x00' * random.randint(1, 65536),
            content_type='image/jpeg'
        )
        avatar.save()
        old_file_path = avatar.profile_image.path
        # is file created?
        self.assertTrue(os.path.exists(old_file_path))
        # is old image deleted from disk?
        avatar.delete()
        self.assertFalse(os.path.exists(old_file_path))

    def test_avatar_get_channel_group_returns_uuid4_as_string(self):
        """
        user's notification web socket identifier(channel_group) should be unique
        """
        avatar = AvatarFactory()
        channel_group = avatar.get_channel_group()
        # is string?
        self.assertIsInstance(channel_group, str)
        # is uuid4 format?
        self.assertTrue(is_uuid4(channel_group))

    def test_avatar_magic_method_str_includes_instance_id(self):
        avatar = AvatarFactory()
        self.assertIn(str(avatar.pk), avatar.__str__())


class FragmentTest(TestCase):

    def test_fragment_get_answer_count(self):
        fragment = FragmentFactory()
        AnswerFactory.create_batch(target=fragment, size=3)
        self.assertEqual(fragment.get_answer_count(), 3)

    def test_fragment_magic_method_str_includes_instance_id(self):
        fragment = FragmentFactory()
        self.assertIn(str(fragment.pk), fragment.__str__())


class TagTest(TestCase):

    def test_get_content_count(self):
        # simple case
        tag = TagFactory()
        FragmentFactory.create_batch(tags=tag, size=3)
        self.assertEqual(tag.get_content_count(), 3)
        # fragments using more than one tags
        tag = TagFactory()
        FragmentFactory.create_batch(tags=[tag, *TagFactory.create_batch(size=3), ], size=5)
        self.assertEqual(tag.get_content_count(), 5)

    def test_tag_magic_method_str_includes_instance_id(self):
        tag = TagFactory()
        self.assertIn(str(tag.pk), tag.__str__())


class AnswerTest(TestCase):

    def test_answer_magic_method_str_includes_instance_id(self):
        answer = AnswerFactory()
        self.assertIn(str(answer.pk), answer.__str__())


class CommentTest(TestCase):

    def test_commentable_get_child_object(self):
        # for parent class alone will return None
        self.assertIsNone(Commentable().get_child_object())
        for factory in get_factories_for_model(Commentable, search_modules=['core.factories'], abstract=True):
            instance = factory()
            # child classes should be instance of Commentable
            self.assertIsInstance(instance, Commentable)
            # get_child_object method returns its child object(itself)
            self.assertEqual(instance.get_child_object(), instance)

    def test_commentable_get_comment_count(self):
        for factory in get_factories_for_model(Commentable, search_modules=['core.factories'], abstract=True):
            # test for each child classes
            instance = factory()
            CommentFactory.create_batch(target=instance, size=3)
            self.assertEqual(instance.get_comment_count(), 3)

    def test_commentable_magic_method_str_includes_instance_id(self):
        commentable = Commentable.objects.create()
        self.assertIn(str(commentable.pk), commentable.__str__())

    def test_comment_magic_method_str_includes_instance_id(self):
        comment = CommentFactory()
        self.assertIn(str(comment.pk), comment.__str__())


class VoteTest(TestCase):

    def test_votable_get_child_object(self):
        # for parent class alone will return None
        self.assertIsNone(Votable().get_child_object())
        for factory in get_factories_for_model(Votable, search_modules=['core.factories'], abstract=True):
            instance = factory()
            # child classes should be instance of Votable
            self.assertIsInstance(instance, Votable)
            # get_child_object method returns its child object(itself)
            self.assertEqual(instance.get_child_object(), instance)

    def test_votable_get_vote_count(self):
        for factory in get_factories_for_model(Votable, search_modules=['core.factories'], abstract=True):
            # test for each child classes
            instance = factory()
            _votes = VoteFactory.create_batch(target=instance, size=3)
            self.assertEqual(instance.get_vote_count(), 3)

    def test_votable_get_average_rating(self):
        for factory in get_factories_for_model(Votable, search_modules=['core.factories'], abstract=True):
            # test for each child classes
            instance = factory()
            votes = VoteFactory.create_batch(target=instance, size=100)
            self.assertAlmostEqual(
                instance.get_average_rating(),
                statistics.mean([v.rating for v in votes]),
                delta=0.001
            )

    def test_votable_magic_method_str_includes_instance_id(self):
        votable = Votable.objects.create()
        self.assertIn(str(votable.pk), votable.__str__())

    def test_vote_magic_method_str_includes_instance_id(self):
        vote = VoteFactory()
        self.assertIn(str(vote.pk), vote.__str__())


class RoomTest(TestCase):

    def test_avatar_get_channel_group_returns_uuid4_as_string(self):
        """
        room's notification web socket identifier(channel_group) should be unique
        """
        room = RoomFactory()
        channel_group = room.get_channel_group()
        # is string?
        self.assertIsInstance(channel_group, str)
        # is uuid4 format?
        self.assertTrue(is_uuid4(channel_group))

    def test_room_magic_method_str_includes_instance_id(self):
        room = RoomFactory()
        self.assertIn(str(room.pk), room.__str__())


class ChatTest(TestCase):

    def test_chat_magic_method_str_includes_instance_id(self):
        chat = ChatFactory()
        self.assertIn(str(chat.pk), chat.__str__())


class NotificationTest(TestCase):

    def test_notification_mark_as_read(self):
        """
        notification marked as read will move user to _users_read field for history
        """
        user = UserFactory()
        notification = NotificationFactory(users=user)
        notification.mark_as_read(user)
        self.assertTrue(not notification.users.filter(pk=user.pk).exists())
        self.assertTrue(notification._users_read.filter(pk=user.pk).exists())

    def test_notification_send_only_for_websocket(self):
        """
        check whether Notification.send returns True(OK) in this test
        details of websocket will be tested at root/ws module
        """
        users = [avatar.user for avatar in AvatarFactory.create_batch(size=3)]
        # send
        notification = NotificationFactory(users=users)
        count_ws_sent, count_fcm_sent = notification.send(fcm_push=False)
        self.assertEqual(count_ws_sent, 3)
        self.assertEqual(count_fcm_sent, 0)

    def test_notification_send_fcm_push_also(self):
        """
        even when FCM push is in consideration, it is expected to return True
        when messaging is done with out error.
        """
        users = [avatar.user for avatar in AvatarFactory.create_batch(size=3)]
        # create dummy FCM device
        from fcm_django.models import FCMDevice
        _devices = [FCMDevice.objects.create(
            user=user,
            registration_id='_{}'.format(user.pk),
            type='web')
            for user in users]
        # some user has 2 devices
        FCMDevice.objects.create(user=random.choice(users), registration_id='__', type='web')
        # send
        notification = NotificationFactory(users=users)
        count_ws_sent, count_fcm_sent = notification.send(fcm_push=True)
        self.assertEqual(count_ws_sent, 3)
        self.assertEqual(count_fcm_sent, 4)

    def test_notification_send_fcm_push_also_for_users_with_no_devices(self):
        """
        even when FCM push is in consideration, it is expected to return True
        when messaging is done with out error.
        """
        users = [avatar.user for avatar in AvatarFactory.create_batch(size=3)]
        # send but user has no device
        notification = NotificationFactory(users=users)
        count_ws_sent, count_fcm_sent = notification.send(fcm_push=True)
        self.assertEqual(count_ws_sent, 3)
        self.assertEqual(count_fcm_sent, 0)

    def test_notification_magic_method_str_includes_instance_id(self):
        notification = NotificationFactory()
        self.assertIn(str(notification.pk), notification.__str__())
