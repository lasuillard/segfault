import random
from django.contrib.auth import get_user_model
from django.db.models import signals
import factory
from segfault.utility import generate_random_string
from .models import Avatar, AVATAR_DEFAULT_IMAGE, Fragment, Answer, Comment, Vote, VOTE_CHOICES, Room, Chat

User = get_user_model()


@factory.django.mute_signals(signals.post_save)
class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.LazyFunction(lambda: generate_random_string(length=16))


@factory.django.mute_signals(signals.pre_save, signals.post_delete)
class AvatarFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Avatar
        django_get_or_create = ['user', ]

    user = factory.SubFactory(UserFactory)


class FragmentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Fragment
        django_get_or_create = ['user', ]

    user = factory.SubFactory(UserFactory)
    title = factory.LazyFunction(lambda: generate_random_string(length=32))
    content = factory.LazyFunction(lambda: generate_random_string(length=1024))
    tags = factory.LazyFunction(lambda: [generate_random_string(8) for _ in range(random.randint(0, 6))])


class AnswerFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Answer
        django_get_or_create = ['user', 'target', ]

    user = factory.SubFactory(UserFactory)
    target = factory.SelfAttribute('..target')
    content = factory.LazyFunction(lambda: generate_random_string(length=1024))


class CommentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Comment
        django_get_or_create = ['user', ]

    user = factory.SubFactory(UserFactory)
    target = factory.SelfAttribute('..target')
    parent = factory.SelfAttribute('..parent')
    content = factory.LazyFunction(lambda: generate_random_string(length=128))


class VoteFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Vote
        django_get_or_create = ['user', ]

    user = factory.SubFactory(UserFactory)
    target = factory.SelfAttribute('..target')
    rating = factory.LazyFunction(lambda: random.choice(VOTE_CHOICES))


class RoomFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Room
        django_get_or_create = ['host', ]

    name = factory.LazyFunction(lambda: generate_random_string(length=8))
    host = factory.SubFactory(UserFactory)

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.users.add(user)


class ChatFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Chat

    user = factory.SelfAttribute('..user')
    room = factory.SelfAttribute('..room')
    content = factory.LazyFunction(lambda: generate_random_string(length=64))
