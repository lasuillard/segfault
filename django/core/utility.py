import random
import string
from importlib import import_module
from collections import namedtuple
from inspect import isclass
import factory
from rest_framework import serializers

"""
    For testing purposes mainly
"""
LabeledTestInput = namedtuple('LabeledTestInput', 'value label')


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
        search_modules = ['api.factories', ]

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


def generate_random_string(length, charset=None):
    """
    return a string with given length of randomly selected from charset

    :param length: length of string
    :param charset: set of characters to select a random character
    :return: string
    """
    if charset is None:
        charset = string.ascii_letters + string.digits

    return ''.join([random.choice(charset) for _ in range(length)])
