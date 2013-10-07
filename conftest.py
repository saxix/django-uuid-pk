import os
import sys
from django.conf import settings


def pytest_configure(config):
    if not settings.configured:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'django_uuid_pk.tests.settings'



def runtests(args=None):
    import pytest

    if not args:
        args = []

    if not any(a for a in args[1:] if not a.startswith('-')):
        args.append('django_uuid_pk/tests')

    sys.exit(pytest.main(args))


if __name__ == '__main__':
    runtests(sys.argv)
