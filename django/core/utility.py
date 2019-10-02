import random
import string
import factory
from importlib import import_module
from inspect import isclass
from django.db import models
from rest_framework import serializers
from core.models import Tag


def convert_tag_str_to_model(tags):
    """
    Return string mapping to Tag model instance, create if does not exists.

    :param tags: pure string array,
    :return: list of Tag instances.
    """
    if any(map(lambda t: not isinstance(t, str), tags)):
        raise ValueError('tags should be pure array of string.')

    tags_already_exists = Tag.objects.filter(name__in=tags)
    for tag in tags_already_exists:
        tags.remove(tag.name)
    tags_newly_created = map(lambda t: Tag.objects.create(name=t), tags)
    return [*tags_already_exists, *tags_newly_created]


def get_serializers_for_model(model, abstract=False, search_modules=None):
    """
    Return serializers found from modules in 'search_modules' related with model.
    This is mainly for testing.

    :param model: model to find serializers related with
    :param abstract: child class of model will be also in consideration
    :param search_modules: list of module to find serializers
    :return: list of serializer
    """
    if search_modules is None:
        search_modules = ['api.v1.serializers', ]

    factory_modules = [
        import_module(module_name) for module_name in search_modules
    ]
    _serializers = []
    for module in factory_modules:
        module_dict = module.__dict__.items()
        for (k, v) in module_dict:
            if isclass(v) and issubclass(v, serializers.Serializer):
                if hasattr(v, 'Meta'):
                    model_for = getattr(v, 'Meta').model
                    if model == model_for or (abstract and issubclass(model_for, model)):
                        _serializers.append(v)

    return _serializers


def get_factories_for_model(model, abstract=False, search_modules=None):
    """
    Return factories found from modules in 'search_modules' related with model.
    This is for mainly testing.

    :param model: model to find factories related with
    :param abstract: child class of model will be also in consideration
    :param search_modules: list of module to find factories
    :return: list of factory
    """
    if search_modules is None:
        search_modules = ['core.factories', ]

    factory_modules = [
        import_module(module_name) for module_name in search_modules
    ]
    factories = []
    for module in factory_modules:
        module_dict = module.__dict__.items()
        for (k, v) in module_dict:
            if isclass(v) and issubclass(v, factory.django.DjangoModelFactory):
                model_for = getattr(v, '_meta').model
                if model == model_for or (abstract and issubclass(model_for, model)):
                    factories.append(v)

    return factories


def generate_random_string(length=12, charset=None):
    """
    return a string with given length of randomly selected from charset

    :param length: length of string
    :param charset: set of characters to select a random character
    :return: string
    """
    length = 0 if length < 0 else length
    if charset is None:
        charset = string.ascii_letters + string.digits

    return ''.join([random.choice(charset) for _ in range(length)])


def get_or_create_random_model_instances(model, model_factory, num=1):
    """
    Populate given length of list with items. fill lacks if existing models are not enough.

    :param model: Django Model class.
    :param model_factory: Factory-boy DjangoModelFactory class.
    :param num: count of instances
    :return: list of model instances
    """
    if not issubclass(model, models.Model):
        raise TypeError('model must be subclass of django.db.models.Model')
    if not issubclass(model_factory, factory.django.DjangoModelFactory):
        raise TypeError('model_factory must be subclass of factory.django.DjangoModelFactory')

    try:
        selected = list(set(random.choices(model.objects.all(), k=num)))
    except IndexError:
        # there's nothing to select
        selected = []

    if len(selected) < num:
        additional = [model_factory() for _ in range(num - len(selected))]
    else:
        additional = []

    return [*selected, *additional]
