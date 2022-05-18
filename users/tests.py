from django.test import TestCase

import string
import random

from .models import User


def create_user(username=None, password=None, **kwargs):
    if username is None:
        username = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
    if password is None:
        password = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
    return User.objects.create_user(username, password, **kwargs)
