import os
import statistics
import random
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import TestCase
from segfault.utility import LabeledTestInput, generate_random_string
from ..factories import (
    get_factories_for_model,
    UserFactory, AvatarFactory, FragmentFactory, AnswerFactory,
    CommentFactory, VoteFactory, RoomFactory, ChatFactory
)
from ..models import (
    Avatar, Fragment, Answer, Commentable, Comment, Votable, Vote, Room, Chat
)

User = get_user_model()


class AvatarTest(TestCase):

    def tearDown(self):
        for avatar in Avatar.objects.all():
            avatar.delete()

    def test_avatar_created_with_default(self):
        avatar = AvatarFactory(profile_image=None, display_name=None)
        # when display_name is not given, then defaulted by username
        self.assertEqual(avatar.display_name, avatar.user.username)
        # the avatar is given default image when not specified
        self.assertEqual(avatar.profile_image.name, Avatar.AVATAR_DEFAULT_IMAGE)

    def test_avatar_blank_display_name(self):
        avatar = AvatarFactory()
        # blank the display_name
        avatar.display_name = ''
        avatar.save()
        # display_name goes to default value when not given.
        self.assertEqual(avatar.display_name, avatar.user.username)

    def test_avatar_set_profile_image(self):
        avatar = AvatarFactory()
        # image should be created properly in media folder
        self.assertEqual(os.path.basename(os.path.dirname(avatar.profile_image.path)), 'media')
        # and also the file should exist
        self.assertTrue(os.path.exists(avatar.profile_image.path))

    def test_avatar_delete_profile_image_on_change(self):
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
        self.assertTrue(os.path.exists(old_file_path))
        # change to new image
        avatar.profile_image = sample_image_two
        avatar.save()
        new_file_path = avatar.profile_image.path
        self.assertTrue(os.path.exists(new_file_path))
        # is old image file deleted?
        self.assertFalse(os.path.exists(old_file_path))
        # new file saved in storage?
        self.assertTrue(os.path.exists(new_file_path))

    def test_avatar_delete_profile_image_on_delete(self):
        avatar = AvatarFactory()
        # set image
        avatar.profile_image = SimpleUploadedFile(
            name=f'{ generate_random_string(length=16) }.jpg',
            content=b'\x00' * random.randint(0, 65536),
            content_type='image/jpeg'
        )
        avatar.save()
        old_file_path = avatar.profile_image.path
        self.assertTrue(os.path.exists(old_file_path))
        # is old image deleted from disk?
        avatar.delete()
        self.assertFalse(os.path.exists(old_file_path))

    def test_avatar_magic_method_str_includes_instance_id(self):
        avatar = AvatarFactory()
        # the instance should represent itself well
        self.assertIn(str(avatar.pk), avatar.__str__())


class FragmentTest(TestCase):

    def test_fragment_get_answer_count(self):
        test_cases = [LabeledTestInput(3, 3), LabeledTestInput(0, 0)]
        for case in test_cases:
            fragment = FragmentFactory()
            _answers = AnswerFactory.create_batch(target=fragment, size=case.value)
            # method should return actual answer count related with fragment
            self.assertEqual(fragment.get_answer_count(), case.label)

    def test_fragment_magic_method_str_includes_instance_id(self):
        fragment = FragmentFactory()
        self.assertIn(str(fragment.pk), fragment.__str__())


class AnswerTest(TestCase):

    def test_answer_magic_method_str_includes_instance_id(self):
        answer = AnswerFactory()
        self.assertIn(str(answer.pk), answer.__str__())


class CommentTest(TestCase):

    def test_commentable_get_child_object(self):
        # Commentable itself is for abstraction
        self.assertIsNone(Commentable().get_child_object())
        for factory in get_factories_for_model(Commentable, abstract=True):
            instance = factory()
            # Child classes should be instance of Commentable
            self.assertIsInstance(instance, Commentable)
            # get_child_object method returns its child object(itself)
            self.assertEqual(instance.get_child_object(), instance)

    def test_commentable_get_comment_count(self):
        test_cases = [LabeledTestInput(8, 8), LabeledTestInput(0, 0)]
        for factory in get_factories_for_model(Commentable, abstract=True):
            for case in test_cases:
                instance = factory()
                _comments = CommentFactory.create_batch(target=instance, size=case.value)
                self.assertEqual(instance.get_comment_count(), case.label)

    def test_commentable_magic_method_str_includes_child_instance_id(self):
        for factory in get_factories_for_model(Commentable, abstract=True):
            instance = factory()
            self.assertIn(str(instance.pk), instance.get_child_object().__str__())

    def test_comment_magic_method_str_includes_instance_id(self):
        comment = CommentFactory()
        self.assertIn(str(comment.pk), comment.__str__())


class VoteTest(TestCase):

    def test_votable_get_child_object(self):
        # Votable itself is for abstraction
        self.assertIsNone(Votable().get_child_object())
        for factory in get_factories_for_model(Votable, abstract=True):
            instance = factory()
            # Child classes should be instance of Votable
            self.assertIsInstance(instance, Votable)
            # get_child_object method returns its child object(itself)
            self.assertEqual(instance.get_child_object(), instance)

    def test_votable_get_vote_count(self):
        test_cases = [LabeledTestInput(22, 22), LabeledTestInput(0, 0)]
        for factory in get_factories_for_model(Votable, abstract=True):
            for case in test_cases:
                instance = factory()
                _votes = VoteFactory.create_batch(target=instance, size=case.value)
                self.assertEqual(instance.get_vote_count(), case.label)

    def test_votable_get_average_rating(self):
        for factory in get_factories_for_model(Votable, abstract=True):
            instance = factory()
            _votes = VoteFactory.create_batch(target=instance, size=100)
            self.assertAlmostEqual(
                instance.get_average_rating(),
                statistics.mean([v.rating for v in _votes]),
                delta=0.001
            )

    def test_votable_magic_method_str_includes_child_instance_id(self):
        for factory in get_factories_for_model(Votable, abstract=True):
            instance = factory()
            self.assertIn(str(instance.pk), instance.get_child_object().__str__())

    def test_vote_magic_method_str_includes_instance_id(self):
        vote = VoteFactory()
        self.assertIn(str(vote.pk), vote.__str__())


class RoomTest(TestCase):

    def test_get_all_users(self):
        test_cases = [LabeledTestInput(10, 11), LabeledTestInput(0, 1)]
        for case in test_cases:
            # count = users + 1(host)
            users = [UserFactory() for _ in range(case.value)]
            room = RoomFactory(users=users)
            self.assertEqual(len(room.get_all_users()), case.label)

    def test_room_magic_method_str_includes_instance_id(self):
        room = RoomFactory()
        self.assertIn(str(room.pk), room.__str__())


class ChatTest(TestCase):

    def test_chat_magic_method_str_includes_instance_id(self):
        chat = ChatFactory()
        self.assertIn(str(chat.pk), chat.__str__())
