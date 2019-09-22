import random
from inspect import isclass
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.db.models import signals
import factory
from segfault.utility import generate_random_string
from .models import Avatar, Fragment, Answer, Commentable, Comment, Votable, Vote, Room, Chat

User = get_user_model()


def get_factories_for_model(model, abstract=False):
    """
        Return factories related with model.
        when abstract is True, it returns factories of subclasses's
    """
    g = globals().items()
    factories = []
    for (k, v) in g:
        if isclass(v) and issubclass(v, factory.django.DjangoModelFactory):
            model_for = getattr(v, '_meta').model
            if model == model_for or (abstract and issubclass(model_for, model)):
                factories.append(v)

    return factories


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
    tags = factory.LazyFunction(lambda: [generate_random_string(8) for _ in range(random.randint(0, 6))])


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
    host = factory.SubFactory(UserFactory)

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            return

        if isinstance(extracted, list):
            for user in extracted:
                self.users.add(user)
        elif extracted is not None:
            for _ in range(random.randint(0, 20)):
                self.users.add(UserFactory())


class ChatFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Chat

    user = factory.SubFactory(UserFactory)
    room = factory.SubFactory(RoomFactory)
    content = factory.LazyFunction(lambda: generate_random_string(length=64))
