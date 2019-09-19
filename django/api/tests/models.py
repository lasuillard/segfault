import os
from django.test import TestCase
from django.contrib.auth import get_user_model
from segfault.settings.base import MEDIA_ROOT
from segfault.utility import LabeledTestInput, generate_random_string, generate_simple_file
from ..factories import (
    AvatarFactory,
    FragmentFactory,
    AnswerFactory,
    CommentFactory,
    VoteFactory,
    RoomFactory,
    ChatFactory
)
from ..models import (
    AVATAR_DEFAULT_IMAGE, Avatar, Fragment, Answer, Commentable, Comment, Votable, Vote, Room, Chat
)

User = get_user_model()


class AvatarTest(TestCase):

    def tearDown(self):
        """
            Delete all avatar media dummy files
        """
        dir = os.path.join(MEDIA_ROOT, 'avatar')
        for file in os.listdir(dir):
            path = os.path.join(dir, file)
            os.remove(path)

    def test_avatar_created_with_default(self):
        """
            Test avatar instance is created with appropriate default
        """
        avatar = AvatarFactory()
        # when display_name is not given, then defaulted by username
        self.assertEqual(avatar.display_name, avatar.user.username)
        # the avatar is given default image when not specified
        self.assertEqual(avatar.profile_image.name, AVATAR_DEFAULT_IMAGE)

    def test_avatar_blank_display_name(self):
        """
            When display name is blank, it will be user's username by default
        """
        avatar = AvatarFactory()
        # blank the display_name
        avatar.display_name = ''
        avatar.save()
        self.assertEqual(avatar.display_name, avatar.user.username)

    def test_avatar_set_profile_image(self):
        """
            Test new image for avatar and the image is stored at media storage
        """
        avatar = AvatarFactory()
        # set avatar image
        avatar.profile_image = generate_simple_file(
            name='sample_image.jpg', size=8192, content_type='image/jpeg'
        )
        avatar.save()
        # image should be created properly in media folder
        self.assertEqual(os.path.basename(os.path.dirname(os.path.dirname(avatar.profile_image.path))), 'media')
        # and also the file should exist
        self.assertTrue(os.path.exists(avatar.profile_image.path))

    def test_avatar_magic_method_str_includes_instance_id(self):
        """
            __str__ should include object primary key for identification
        """
        avatar = AvatarFactory()
        # the instance should represent itself well
        self.assertIn(str(avatar.pk), avatar.__str__())


class FragmentTest(TestCase):

    def test_fragment_get_answer_count(self):
        """
            Should return exactly same count it has
        """
        test_cases = [LabeledTestInput(3, 3), LabeledTestInput(0, 0)]
        for case in test_cases:
            fragment = FragmentFactory()
            _answers = AnswerFactory.create_batch(target=fragment, size=case.value)
            self.assertEqual(fragment.get_answer_count(), case.label)


class AnswerTest(TestCase):

    def test_answer_magic_method_str_includes_instance_id(self):
        """
            __str__ should include object primary key for identification
        """
        answer = AnswerFactory(target=FragmentFactory())
        self.assertIn(str(answer.pk), answer.__str__())


class CommentTest(TestCase):

    def test_commentable_subclasses(self):
        """
            Some models are required to be 'Commentable'
        """
        # Fragment should be
        self.assertIsInstance(FragmentFactory(), Commentable)
        # Answer should be
        self.assertIsInstance(AnswerFactory(target=FragmentFactory()), Commentable)

    def test_commentable_get_child_object(self):
        """
            For 'Commentable' objects, get_child_object should return its real class extending its abstraction.
        """
        # Commentable is just for abstraction
        self.assertIsNone(Commentable().get_child_object())
        # Fragment is subclass
        fragment = FragmentFactory()
        self.assertEqual(fragment, super(Commentable, fragment).get_child_object())
        # Answer is subclass
        answer = AnswerFactory(target=FragmentFactory())
        self.assertEqual(answer, super(Commentable, answer).get_child_object())

    def test_commentable_get_comment_count(self):
        """
            Count should be equal to real comments related
        """
        test_cases = [LabeledTestInput(8, 8), LabeledTestInput(0, 0)]
        for case in test_cases:
            fragment = FragmentFactory()
            _comments = CommentFactory.create_batch(target=fragment, parent=None, size=case.value)
            self.assertEqual(fragment.get_comment_count(), case.label)

    def test_commentable_magic_method_str_includes_child_instance_id(self):
        """
            __str__ should include object primary key for identification
        """
        fragment = FragmentFactory()
        self.assertIn(str(fragment.pk), super(Commentable, fragment).get_child_object().__str__())

    def test_comment_magic_method_str_includes_instance_id(self):
        """
            __str__ should include object primary key for identification
        """
        comment = CommentFactory(target=FragmentFactory(), parent=None)
        self.assertIn(str(comment.pk), comment.__str__())


class VoteTest(TestCase):

    def test_votable_get_child_object(self):
        pass

    def test_votable_get_vote_count(self):
        pass

    def test_votable_get_average_rating(self):
        pass

    def test_votable_magic_method_str_includes_child_instance_id(self):
        pass

    def test_vote_magic_method_str_includes_instance_id(self):
        pass


class RoomTest(TestCase):
    pass


class ChatTest(TestCase):
    pass
