import random
import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.db.models import signals
from core.utility import get_factories_for_model, generate_random_string, get_or_create_random_model_instances
from core.models import (
    Avatar, Fragment, Tag, Answer, Commentable, Comment, Votable, Vote, Room, Chat, Notification
)

User = get_user_model()


@factory.django.mute_signals(signals.post_save)
class UserFactory(factory.django.DjangoModelFactory):
    # Avatar is created with user by signal

    class Meta:
        model = User

    username = factory.LazyFunction(lambda: generate_random_string(length=16))


class AvatarFactory(factory.django.DjangoModelFactory):
    # For special purposes: testing, etc.

    class Meta:
        model = Avatar
        django_get_or_create = ['user', ]

    user = factory.SubFactory(UserFactory)
    profile_image = factory.LazyFunction(
        lambda: SimpleUploadedFile(
            name=f'{ generate_random_string(length=16) }.jpg',
            content=b'\x00' * random.randint(0, 65536),
            content_type='image/jpeg'
        )
    )
    display_name = factory.LazyFunction(lambda: generate_random_string(length=16))
    introduce_message = factory.LazyFunction(lambda: generate_random_string(length=64))


class FragmentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Fragment

    user = factory.SubFactory(UserFactory)
    title = factory.LazyFunction(lambda: generate_random_string(length=32))
    content = factory.LazyFunction(lambda: generate_random_string(length=1024))

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if isinstance(extracted, Tag):
            self.tags.add(extracted)
        elif isinstance(extracted, list):
            self.tags.set(extracted)
        else:
            for _ in range(random.randint(1, 10)):
                self.tags.add(TagFactory())


class TagFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Tag

    name = factory.LazyFunction(lambda: generate_random_string(length=16))
    is_official = factory.LazyFunction(lambda: random.choice([True, False]))


class AnswerFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Answer

    user = factory.SubFactory(UserFactory)
    target = factory.SubFactory(FragmentFactory)
    content = factory.LazyFunction(lambda: generate_random_string(length=512))


class CommentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Comment

    user = factory.SubFactory(UserFactory)
    target = factory.LazyFunction(
        lambda: random.choice(get_factories_for_model(Commentable, abstract=True))()
    )
    parent = factory.LazyAttribute(
        lambda o: random.choice([None, *Comment.objects.filter(target=o.target)]) if random.random() > 0.5 else None
    )
    content = factory.LazyFunction(lambda: generate_random_string(length=128))


class VoteFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Vote

    user = factory.SubFactory(UserFactory)
    target = factory.LazyFunction(
        lambda: random.choice(get_factories_for_model(Votable, abstract=True))()
    )
    rating = factory.LazyFunction(lambda: random.choice([v[0] for v in Vote.VOTE_CHOICES]))


class RoomFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Room

    name = factory.LazyFunction(lambda: generate_random_string(length=8))
    user = factory.SubFactory(UserFactory)


class ChatFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Chat

    user = factory.SubFactory(UserFactory)
    room = factory.SubFactory(RoomFactory)
    content = factory.LazyFunction(lambda: generate_random_string(length=64))


class NotificationFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Notification

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            return

        if isinstance(extracted, User):
            self.users.add(extracted)
        elif isinstance(extracted, list):
            self.users.set(extracted)
        else:
            for _ in range(random.randint(1, 10)):
                self.users.add(UserFactory())

    title = factory.LazyFunction(lambda: generate_random_string(length=32))
    body = factory.LazyFunction(lambda: generate_random_string(length=96))
