import random
import string


def generate_random_string(length, charset=None):
    if charset is None:
        charset = string.ascii_letters + string.digits

    return ''.join([random.choice(charset) for _ in range(length)])
