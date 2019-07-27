import os
import random
import string
import statistics

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, TestCase
from django.db import models
from django.contrib.auth import get_user_model
from api.models import (
    Avatar, DEFAULT_PROFILE_IMAGES,
    Fragment,
    Answer,
    Comment,
    Vote, VOTE_CHOICES,
    ChatRoom,
    Chat,
)

User = get_user_model()


def generate_random_string(length, charset=None):
    if charset is None:
        charset = string.ascii_letters + string.digits

    return ''.join([random.choice(charset) for _ in range(length)])


def create_tester(count=1):
    if count < 1:
        return None
    elif count == 1:
        return User.objects.create(username=generate_random_string(length=16))

    return [create_tester(count=1) for _ in range(count)]


def create_simple_file(name, content_type='text/plain', size=1024):
    return SimpleUploadedFile(name=name, content=(b'\x00' * size), content_type=content_type)


class ToolTestCase(TestCase):
    """
        test cases for global variables and functions used in test cases
    """
    def test_create_tester(self):
        tester = create_tester(count=1)
        self.assertIsInstance(tester, User)

        testers = create_tester(count=7)
        self.assertIsInstance(testers, list)
        self.assertEqual(len(testers), 7)

        testers = create_tester(count=0)
        self.assertEqual(testers, None)

        testers = create_tester(count=(-3))
        self.assertEqual(testers, None)

    def test_generate_random_string(self):
        # tuple: (length, expected length of output)
        cases = [
            (1, 1), (25, 25), (-3, 0), (0, 0)
        ]
        for case in cases:
            self.assertEqual(case[1], len(generate_random_string(length=case[0])))

    def test_create_simple_file(self):
        # tuple: (size, expected size of output
        cases = [
            (2, 2), (65535, 65535), (-128, 0), (0, 0)
        ]
        for case in cases:
            file = create_simple_file(name=generate_random_string(32), size=case[0])
            self.assertIsInstance(file, SimpleUploadedFile)
            self.assertEqual(file.size, case[1])


class AvatarTestCase(TestCase):

    @staticmethod
    def generate_random_avatar(user=None, profile_image=None):
        if user is None:
            user = create_tester()

        if profile_image is None:
            return Avatar.objects.create(user=user)

        elif profile_image is 'random':  # create random image
            profile_image = create_simple_file(
                name=generate_random_string(length=16) + '.jpg',
                content_type='image/jpeg',
                size=65536,
            )

        return Avatar.objects.create(user=user, profile_image=profile_image)

    def test_avatar_instance_creation(self):
        avatar = self.generate_random_avatar()
        self.assertIsInstance(avatar, Avatar)
        # display_name's default is user's name
        self.assertEqual(avatar.display_name, avatar.user.username)
        # profile_image's default is a random choice of default image set
        self.assertIn(avatar.profile_image.name, DEFAULT_PROFILE_IMAGES)

    def test_avatar_instance_modification(self):
        avatar = self.generate_random_avatar()
        """
            case: create image
        """
        avatar.profile_image = create_simple_file(name='test_image.jpg', content_type='image/jpeg', size=1024)
        avatar.save()
        # image should be created properly
        self.assertTrue(os.path.exists(avatar.profile_image.path))
        """
            case: change image
        """
        old_path = avatar.profile_image.path
        avatar.profile_image = create_simple_file(name='test_image_2.jpg', content_type='image/jpeg', size=1024)
        avatar.save()
        new_path = avatar.profile_image.path
        # image should not be equal (uuid4)
        self.assertNotEqual(old_path, new_path)
        # old image should be deleted from local disk
        self.assertFalse(os.path.exists(old_path))
        # new image created properly
        self.assertTrue(os.path.exists(new_path))
        """
            case: delete image
        """
        old_path = new_path
        avatar.profile_image.delete(save=True)
        # image should be deleted
        self.assertFalse(os.path.exists(old_path))

    def test_avatar_instance_destruction(self):
        avatar = self.generate_random_avatar()
        """
            case: delete instance pointing default image
        """
        path = avatar.profile_image.path
        avatar.delete()
        # default image should not be deleted
        self.assertTrue(os.path.exists(path))
        """
            case: delete instance using user custom image
        """
        avatar = self.generate_random_avatar(profile_image='random')
        path = avatar.profile_image.path
        avatar.delete()
        # custom image should be deleted
        self.assertFalse(os.path.exists(path))

    def test_avatar_magic_methods(self):
        """
            test magic methods
        """
        avatar = self.generate_random_avatar()
        # __str__ should include primary key for identification
        self.assertIn(str(avatar.pk), avatar.__str__())


class FragmentTestCase(TestCase):

    @staticmethod
    def generate_random_fragment(user=None):
        if user is None:
            user = create_tester()

        return Fragment.objects.create(
            user=user,
            title=generate_random_string(length=64),
            content=generate_random_string(length=2048),
        )

    def test_fragment_instance_creation(self):
        fragment = self.generate_random_fragment()
        self.assertIsInstance(fragment, Fragment)

    def test_fragment_instance_modification(self):
        pass

    def test_fragment_instance_destruction(self):
        pass

    def test_fragment_magic_methods(self):
        fragment = self.generate_random_fragment()
        # __str__ should include primary key in result string
        self.assertIn(str(fragment.pk), fragment.__str__())


class AnswerTestCase(TestCase):

    @staticmethod
    def generate_random_answer(user=None, fragment=None):
        if user is None:
            user = create_tester()

        if fragment is None:
            fragment = FragmentTestCase.generate_random_fragment()

        return Answer.objects.create(
            user=user,
            target=fragment,
            content=generate_random_string(length=1024),
        )

    def test_answer_instance_creation(self):
        answer = self.generate_random_answer()
        self.assertIsInstance(answer, Answer)

    def test_answer_instance_modification(self):
        pass

    def test_answer_instance_destruction(self):
        pass

    def test_answer_magic_methods(self):
        answer = self.generate_random_answer()
        # __str__ should include instance's primary key
        self.assertIn(str(answer.pk), answer.__str__())


# includes test for commentables also
class CommentTestCase(TestCase):

    @staticmethod
    def generate_commentables():
        return [
            FragmentTestCase.generate_random_fragment(),
            AnswerTestCase.generate_random_answer(),
        ]

    @staticmethod
    def generate_random_comment(parent=None, user=None, target=None):
        if user is None:
            user = create_tester()

        if target is None:
            # child classes of commentable
            target = random.choice(CommentTestCase.generate_commentables())

        return Comment.objects.create(
            parent=parent,
            user=user,
            target=target,
            content=generate_random_string(length=256),
        )

    def test_comment_instance_creation(self):
        comment = self.generate_random_comment()
        self.assertIsInstance(comment, Comment)

    def test_comment_instance_modification(self):
        pass

    def test_comment_instance_destruction(self):
        pass

    def test_comment_magic_methods(self):
        comment = self.generate_random_comment()
        # __str__ should include instance's primary key
        self.assertIn(str(comment.pk), comment.__str__())

    def test_commentable_get_child_object(self):
        for commentable in self.generate_commentables():
            self.assertEqual(commentable, commentable.get_child_object())


# includes test for votable
class VoteTestCase(TestCase):

    @staticmethod
    def generate_votables():
        return [
            FragmentTestCase.generate_random_fragment(),
            AnswerTestCase.generate_random_answer(),
        ]

    @staticmethod
    def generate_random_vote(user=None, target=None, rating=None):
        if user is None:
            user = create_tester()

        if target is None:
            # child classes of votable
            target = random.choice(VoteTestCase.generate_votables())

        if rating is None:
            rating = random.choice(VOTE_CHOICES)[0]

        return Vote.objects.create(
            user=user,
            target=target,
            rating=rating,
        )

    def test_vote_instance_creation(self):
        vote = self.generate_random_vote()
        self.assertIsInstance(vote, Vote)

    def test_vote_instance_modification(self):
        pass

    def test_vote_instance_destruction(self):
        pass

    def test_vote_magic_methods(self):
        vote = self.generate_random_vote()
        # __str__ should include pk
        self.assertIn(str(vote.pk), vote.__str__())

    def test_votable_get_child_object(self):
        for votable in self.generate_votables():
            self.assertEqual(votable, votable.get_child_object())

    def test_votable_get_average_rating(self):
        for votable in self.generate_votables():
            votes = []
            for _ in range(100):
                vote = self.generate_random_vote(target=votable)
                votes.append(vote.rating)

            self.assertAlmostEqual(statistics.mean(votes), votable.get_average_rating(), delta=0.01)


class ChatRoomTestCase(TestCase):

    @staticmethod
    def generate_random_chatroom(user=None, users=None):
        if user is None:
            user = create_tester()

        if users is None:
            users = 10

        if isinstance(users, User):
            users = [User]

        elif isinstance(users, list):
            users = users

        elif isinstance(users, int):
            users = create_tester(users)

        obj = ChatRoom.objects.create(user=user)
        for _user in users:
            obj.users.add(_user)

        return obj

    def test_chatroom_instance_creation(self):
        chatroom = self.generate_random_chatroom()
        self.assertIsInstance(chatroom, ChatRoom)

    def test_chatroom_instance_modification(self):
        pass

    def test_chatroom_instance_destruction(self):
        pass

    def test_chatroom_magic_methods(self):
        chatroom = self.generate_random_chatroom()
        # __str__ include pk
        self.assertIn(str(chatroom.pk), chatroom.__str__())

    def test_chatroom_get_all_attendants(self):
        user = create_tester()
        users = create_tester(17)
        chatroom = self.generate_random_chatroom(user=user, users=users)
        attendants = chatroom.get_all_attendants()
        self.assertIn(user, attendants)
        for _user in users:
            self.assertIn(_user, attendants)

        self.assertEqual(len(attendants), 18)


class ChatTestCase(TestCase):

    @staticmethod
    def generate_random_chat(user=None, room=None):
        if user is None:
            user = create_tester()

        if room is None:
            room = ChatRoomTestCase.generate_random_chatroom()

        return Chat.objects.create(user=user, room=room, content=generate_random_string(length=128))

    def test_chat_instance_creation(self):
        chat = self.generate_random_chat()
        self.assertIsInstance(chat, Chat)

    def test_chat_instance_modification(self):
        pass

    def test_chat_instance_destruction(self):
        pass

    def test_chat_magic_methods(self):
        chat = self.generate_random_chat()
        # __str__ check including pk
        self.assertIn(str(chat.pk), chat.__str__())
