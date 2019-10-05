import random
import string
import factory
from uuid import UUID
from importlib import import_module
from inspect import isclass
from django.db import models
from rest_framework import serializers


class TimeStampedModel(models.Model):
    date_created = models.DateTimeField(
        verbose_name='Creation date',
        auto_now_add=True,
        editable=False,
    )
    date_modified = models.DateTimeField(
        verbose_name='Modification date',
        auto_now=True,
        editable=False
    )

    class Meta:
        abstract = True


def is_uuid4(uuid_string):
    """
    test whether given string is uuid4 format or not
    """
    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        return False

    return uuid_string == str(val)


def get_serializers_for_model(model, search_modules, abstract=False):
    """
    return serializers found from modules in 'search_modules' related with model
    """
    if not search_modules:
        return None

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


def get_factories_for_model(model, search_modules, abstract=False):
    """
    return factories found from modules in 'search_modules' related with model
    """
    if not search_modules:
        return None

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
    """
    length = 0 if length < 0 else length
    if charset is None:
        charset = string.ascii_letters + string.digits

    return ''.join([random.choice(charset) for _ in range(length)])


def get_or_create_random_model_instances(model, model_factory, num=1):
    """
    populate given length of list with items. fill lacks if existing models are not enough
    """
    if not issubclass(model, models.Model):
        raise TypeError('model must inherit django.db.models.Model class')
    if not issubclass(model_factory, factory.DjangoModelFactory):
        raise TypeError('model_factory must be a subclass of factory.DjangoModelFactory')
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
