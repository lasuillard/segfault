import random
import string
from collections import namedtuple
from django.core.files.uploadedfile import SimpleUploadedFile


"""
    For testing purposes mainly
"""
LabeledTestInput = namedtuple('LabeledTestInput', 'value label')


def generate_random_string(length, charset=None):
    if charset is None:
        charset = string.ascii_letters + string.digits

    return ''.join([random.choice(charset) for _ in range(length)])


def generate_simple_file(name, size=1024, content_type='text/plain'):
    if name is None:
        name = f'{ generate_random_string(length=32) }.txt'

    return SimpleUploadedFile(name=name, content=b'\x00' * size, content_type=content_type)
